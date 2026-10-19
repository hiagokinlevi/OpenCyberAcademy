"""Read-only OpenCyber Academy REST and stateless MCP API for Cloudflare Python Workers."""

from __future__ import annotations

import asyncio
import hashlib
import html
import json
import re
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from pydantic import BaseModel, Field

from access import identity as access_identity
from course_directory import render_course_directory, render_course_focus
from locales import ACTIVE_INTERFACES, LANGUAGES, language_for_host, site_for_language
from practice_engine import InvalidPractice, validate_practice
from public_usage import collect as collect_public_usage, counts as public_usage_counts
from quiz_engine import InvalidBank, feedback, public_question, score_answer, validate_bank
from seo_pages import lesson_path, render_lesson_page, render_planned_lesson_page
from student_auth import (SESSION_LIFETIME, _limit, basic_credentials, create_session,
                          mcp_student_identity, password_account, router as student_auth_router, student_identity)
from student_activity import (course_performance, record as record_activity, rows as activity_rows,
                              summary as activity_summary)
from tabletop import render_case as render_tabletop_case, render_index as render_tabletop_index


app = FastAPI(title="OpenCyber Academy public learning API", version="0.1.0", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.include_router(student_auth_router)
GITHUB_RAW = "https://raw.githubusercontent.com/hiagokinlevi/OpenCyberAcademy/main/"
GITHUB_VIEW = "https://github.com/hiagokinlevi/OpenCyberAcademy/blob/main/"
CATALOG_PATH = Path(__file__).resolve().parents[1] / "public" / "catalog.json"
TEST_INDEX_PATH = CATALOG_PATH.with_name("test-index.json")
APPROVED_BOOKS_PATH = CATALOG_PATH.with_name("approved-books.json")
ANCHOR = re.compile(r'^<a id="ch-(\d{2,4})"></a>\s*$', re.M)
LESSON_ANCHOR = re.compile(r'^<a id="lesson-(\d{2,4})"></a>\s*$', re.M)
WEEK_DAY_ANCHOR = re.compile(r'^<a id="week-(\d{2,4})-day-(\d{2})"></a>\s*$', re.M)
CHAPTER_LESSONS_MARKER = "<!-- open-cyber-academy:chapter-lessons -->"
EXERCISE = re.compile(r'\bEX(\d{3,4})\b')
EXERCISE_HEADING = re.compile(r'^#{3,6}\s+EX(\d{3,4})\b', re.M)
EXERCISE_PROMPT = re.compile(r'^[ \t]*(?:#{3,6}[ \t]+|[-*][ \t]+)?(?:\*\*)?EX(\d{3,4})\b', re.M)
ANSWER = re.compile(r'^###\s+EX(\d{3,4})\b.*$|^\*\*EX(\d{3,4})(?:\s+[—-]|\.)[^\n]*$', re.M)
APPENDIX_HEADING = re.compile(
    r'^##\s+(?:(?:final\s+appendix|apêndice\s+final|apendice\s+final|apéndice\s+final)\s+[—–:-]\s+)?'
    r'(?:worked\s+(?:results|answers)|answer\s+key|gabarito|respostas|resoluções|resultados(?:\s+resueltos)?|soluciones|resoluciones)\b',
    re.M | re.I,
)
REFERENCES_HEADING = re.compile(r'^##\s+(?:references|referências|referencias)\b', re.M | re.I)
MCP_VERSION = "2025-06-18"
EDITORIAL_POLICY_URI = "open-cyber-academy://editorial-policy"
ALLOWED_ORIGINS = {site_for_language(language) for language in LANGUAGES} | {"https://www.opencyber.academy", "http://localhost:4321", "http://localhost:8787", "http://127.0.0.1:8787"}
MAX_SOURCE_CHARS = 24_000_000
PUBLIC_ORIGINS = {site_for_language(language) for language in LANGUAGES} | {"https://www.opencyber.academy"}
_live_test_index: dict[str, Any] | None = None
_live_test_index_until = 0.0
_live_test_index_lock = asyncio.Lock()


class LessonProgress(BaseModel):
    level: str = Field(pattern=r"^[a-z0-9-]+$", max_length=50)
    area: str = Field(pattern=r"^[a-z0-9-]+$", max_length=80)
    language: str = Field(pattern=r"^[a-z]{2}$")
    chapter: int = Field(ge=1, le=9999)
    status: str = Field(pattern=r"^(in_progress|completed)$")


class ExerciseAttempt(LessonProgress):
    exercise_id: str = Field(pattern=r"^EX[0-9]{3,4}$")
    answer: str = Field(default="", max_length=20_000)
    status: str = Field(pattern=r"^(attempted|completed)$")
    unit_kind: str = Field(default="lesson", pattern=r"^(lesson|chapter)$")


class TestStart(BaseModel):
    level: str = Field(pattern=r"^[a-z0-9-]+$", max_length=50)
    area: str = Field(pattern=r"^[a-z0-9-]+$", max_length=80)
    language: str = Field(pattern=r"^[a-z]{2}$")
    chapter: int = Field(ge=1, le=9999)


class TestAnswer(BaseModel):
    attempt_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,80}$")
    index: int = Field(ge=0, le=9)
    selected: str | None = Field(default=None, pattern=r"^[a-e]$")


class CertificateClaim(BaseModel):
    level: str = Field(pattern=r"^[a-z0-9-]+$", max_length=50)
    area: str = Field(pattern=r"^[a-z0-9-]+$", max_length=80)
    language: str = Field(pattern=r"^[a-z]{2}$")


class LearningActivity(TestStart):
    kind: str = Field(pattern=r"^(lesson_opened|lesson_read)$")
    seconds: int = Field(default=0, ge=0, le=3600)


class StudentAnalysis(TestStart):
    note: str = Field(min_length=1, max_length=10_000)


class PublicUsageEvent(BaseModel):
    visitor: str = Field(pattern=r"^[a-f0-9]{32}$")
    event: str = Field(pattern=r"^(view|read|exercise)$")
    path: str = Field(min_length=1, max_length=301)
    exercise_id: str = Field(default="", pattern=r"^(?:|EX[0-9]{3,4})$")
    edition: str = Field(default="", pattern=r"^(?:|[a-z]{2})$")


@app.middleware("http")
async def canonical_domain(request: Request, call_next):
    host = request.headers.get("host", "")
    if host == "www.opencyber.academy":
        return RedirectResponse("https://opencyber.academy" + request.url.path + ("?" + request.url.query if request.url.query else ""), status_code=308)
    host_language = language_for_host(host)
    match = re.fullmatch(r"/courses/[^/]+/[^/]+/(?:lessons|chapters)/([a-z]{2})/\d+/?", request.url.path)
    if host_language and match and match.group(1) in LANGUAGES and match.group(1) != host_language:
        return RedirectResponse(site_for_language(match.group(1)) + request.url.path, status_code=308)
    response = await call_next(request)
    if request.url.path.startswith(("/api/", "/mcp")):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Robots-Tag"] = "noindex"
    if request.url.path.startswith(("/private/", "/student/", "/auth/")):
        response.headers["X-Robots-Tag"] = "noindex"
        response.headers["Cache-Control"] = "no-store"
    return response


async def identity(request: Request) -> dict:
    if request.url.path.startswith("/student/"):
        return await student_identity(request)
    return await access_identity(request)


def same_origin(request: Request) -> None:
    origin = request.headers.get("origin", "")
    if origin not in PUBLIC_ORIGINS:
        raise HTTPException(403, "A progress update must come from the OpenCyber Academy site")


def database(request: Request):
    env = request.scope.get("env")
    db = getattr(env, "DB", None)
    if db is None:
        raise HTTPException(503, "Student progress storage is not configured")
    return db


def d1_rows(result: Any) -> list[dict]:
    if isinstance(result, dict):
        return result.get("results", [])
    from js import JSON  # type: ignore[import-not-found]
    return json.loads(str(JSON.stringify(result))).get("results", [])


def d1_changes(result: Any) -> int:
    if isinstance(result, dict):
        return int(result.get("meta", {}).get("changes", 0))
    from js import JSON  # type: ignore[import-not-found]
    return int(json.loads(str(JSON.stringify(result))).get("meta", {}).get("changes", 0))


async def catalog(request: Request) -> dict[str, Any]:
    """The static catalog lists all courses; selected books are fetched live."""
    if override := getattr(app.state, "catalog_override", None):
        return override
    env = request.scope.get("env")
    if env is not None:
        response = await env.ASSETS.fetch("https://assets.local/catalog.json")
        if int(response.status) != 200:
            raise HTTPException(503, "Catalog asset is unavailable")
        return json.loads(str(await response.text()))
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


async def public_asset_json(request: Request, filename: str, local_path: Path) -> dict[str, Any]:
    env = request.scope.get("env")
    if env is not None:
        response = await env.ASSETS.fetch(f"https://assets.local/{filename}")
        if int(response.status) != 200:
            raise HTTPException(503, f"{filename} is unavailable")
        return json.loads(str(await response.text()))
    return json.loads(local_path.read_text(encoding="utf-8"))


async def test_index(request: Request) -> dict[str, Any]:
    bundled = await public_asset_json(request, "test-index.json", TEST_INDEX_PATH)
    if request.scope.get("env") is None:
        return bundled
    # GitHub is the editorial source. Refresh the published bank list without
    # requiring a site deploy for each independently published question bank.
    global _live_test_index, _live_test_index_until
    if _live_test_index is not None and time.time() < _live_test_index_until:
        return _live_test_index
    async with _live_test_index_lock:
        if _live_test_index is not None and time.time() < _live_test_index_until:
            return _live_test_index
        try:
            from js import Object, fetch  # type: ignore[import-not-found]
            from pyodide.ffi import to_js  # type: ignore[import-not-found]
            response = await fetch(
                "https://api.github.com/repos/hiagokinlevi/OpenCyberAcademy/git/trees/main?recursive=1",
                to_js({"headers": {"User-Agent": "OpenCyberAcademy-public-reader",
                                   "Accept": "application/vnd.github+json"}}, dict_converter=Object.fromEntries),
            )
            if int(response.status) != 200:
                raise ValueError("GitHub tree is unavailable")
            tree = json.loads(str(await response.text()))
            if tree.get("truncated") or not isinstance(tree.get("tree"), list):
                raise ValueError("GitHub tree is incomplete")
            published = {(key, int(item["chapter"])): item for key, chapters in bundled["courses"].items()
                         for item in chapters}
            known_courses = {(item["level"], item["area"]) for item in (await catalog(request))["courses"]}
            book_blobs = {item["path"]: item.get("sha") for item in tree["tree"]
                          if item.get("path", "").endswith("/book/MANUSCRIPT.md")}
            courses: dict[str, list[dict[str, Any]]] = {}
            for item in tree["tree"]:
                match = re.fullmatch(r"web/question-banks/([a-z0-9-]+)/([a-z0-9-]+)/([a-z]{2})/(\d{3})\.json", item.get("path", ""))
                if not match or item.get("type") != "blob":
                    continue
                level, area, language, number = match.groups()
                if (level, area) not in known_courses or language not in LANGUAGES:
                    continue
                chapter = int(number)
                key = f"{level}/{area}/{language}"
                old = published.get((key, chapter))
                manuscript = f"levels/{level}/{area}/{language}/book/MANUSCRIPT.md"
                book_unchanged = bundled.get("book_git_sha", {}).get(key) == book_blobs.get(manuscript)
                if old and old.get("git_sha") == item.get("sha") and book_unchanged:
                    entry = old
                else:
                    try:
                        bank, digest = await chapter_test_bank(request, level, area, language, chapter, check_source=True)
                    except HTTPException:
                        continue  # A changed or incomplete chapter cannot become available.
                    entry = {"chapter": chapter, "bank_sha256": digest,
                             "source_sha256": bank["source_sha256"], "git_sha": item["sha"]}
                courses.setdefault(key, []).append(entry)
            for chapters in courses.values():
                chapters.sort(key=lambda entry: entry["chapter"])
            result = {"version": 1, "questions_per_chapter": 10,
                      "courses": dict(sorted(courses.items())), "source_head": tree.get("sha"), "live_sync": "github"}
            _live_test_index = result
            _live_test_index_until = time.time() + 1800
            return result
        except Exception:
            _live_test_index = {**bundled, "live_sync": "bundled"}
            _live_test_index_until = time.time() + 300
            return _live_test_index


async def approved_books(request: Request) -> dict[str, Any]:
    return await public_asset_json(request, "approved-books.json", APPROVED_BOOKS_PATH)


def get_course(data: dict[str, Any], level: str, area: str, language: str) -> dict[str, Any]:
    if language not in data["languages"]:
        raise HTTPException(404, "Unknown language")
    for course in data["courses"]:
        if course["level"] == level and course["area"] == area:
            return course
    raise HTTPException(404, "Unknown course")


async def source_text(request: Request, path: str) -> str | None:
    """Read a fixed public GitHub path; 404 means this edition has only a plan."""
    # A lesson request renders both the lesson and its course navigation. Keep
    # those reads on the same source snapshot without caching across requests.
    cache = getattr(request.state, "source_text_cache", None)
    if cache is None:
        cache = request.state.source_text_cache = {}
    if path in cache:
        return cache[path]
    if override := getattr(app.state, "source_override", None):
        result = await override(path)
        cache[path] = result
        return result
    # Each read resolves main again. A unique query keeps intermediate CDN caches
    # from serving an older version after a lesson is edited in the repository.
    url = GITHUB_RAW + path + f"?source={time.time_ns()}"
    try:
        from js import fetch  # type: ignore[import-not-found]
    except ImportError:
        def local_fetch() -> str | None:
            try:
                with urlopen(url, timeout=12) as response:
                    data = response.read(MAX_SOURCE_CHARS + 1)
            except HTTPError as exc:
                if exc.code == 404:
                    return None
                raise
            if len(data) > MAX_SOURCE_CHARS:
                raise HTTPException(502, "Upstream book exceeds reading limit")
            return data.decode("utf-8")
        try:
            result = await asyncio.to_thread(local_fetch)
            cache[path] = result
            return result
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(502, "GitHub source temporarily unavailable") from exc
    try:
        response = await fetch(url)
        if int(response.status) == 404:
            return None
        if int(response.status) != 200:
            raise HTTPException(502, "GitHub source temporarily unavailable")
        text = str(await response.text())
        if len(text) > MAX_SOURCE_CHARS:
            raise HTTPException(502, "Upstream book exceeds reading limit")
        cache[path] = text
        return text
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(502, "GitHub source temporarily unavailable") from exc


async def editorial_policy(request: Request) -> str:
    """Serve the current public rule from main, rather than a stale deploy copy."""
    policy = await source_text(request, "BOOK_STANDARD.md")
    if policy is None:
        raise HTTPException(503, "Editorial policy is unavailable")
    return policy


def book_path(level: str, area: str, language: str, filename: str) -> str:
    return f"levels/{level}/{area}/{language}/book/{filename}"


def chapter_sections(markdown: str) -> dict[int, dict[str, str]]:
    anchors = list(ANCHOR.finditer(markdown))
    chapters: dict[int, dict[str, str]] = {}
    for index, match in enumerate(anchors):
        end = anchors[index + 1].start() if index + 1 < len(anchors) else len(markdown)
        body = markdown[match.start():end].strip()
        heading = re.search(r'^#{2,3}\s+(.+)$', body, re.M)
        if heading is None:
            continue
        if index == len(anchors) - 1:
            tail = body[heading.end():]
            endings = [found.start() for pattern in (APPENDIX_HEADING, REFERENCES_HEADING) if (found := pattern.search(tail))]
            if endings:
                body = body[:heading.end() + min(endings)].rstrip()
        chapters[int(match.group(1))] = {"title": heading.group(1).strip(), "markdown": body}
    return chapters


def lesson_sections(markdown: str) -> dict[int, dict[str, Any]]:
    """Return authored daily lessons and their enclosing weekly chapters."""
    lessons: dict[int, dict[str, Any]] = {}
    anchors = sorted(
        [(match, int(match.group(1)), None, f"lesson-{match.group(1)}") for match in LESSON_ANCHOR.finditer(markdown)]
        + [(match, (int(match.group(1)) - 1) * 5 + int(match.group(2)), int(match.group(1)),
            f"week-{match.group(1)}-day-{match.group(2)}") for match in WEEK_DAY_ANCHOR.finditer(markdown)
           if 1 <= int(match.group(2)) <= 5],
        key=lambda item: item[0].start(),
    )
    chapters = list(ANCHOR.finditer(markdown))
    appendix = APPENDIX_HEADING.search(markdown)
    for index, (match, number, declared_week, anchor) in enumerate(anchors):
        stops = [chap.start() for chap in chapters if chap.start() > match.start()]
        if index + 1 < len(anchors):
            stops.append(anchors[index + 1][0].start())
        if appendix and appendix.start() > match.start():
            stops.append(appendix.start())
        if declared_week is not None:
            end_marker = re.search(rf'^<a id="week-{declared_week:02d}-end"></a>\s*$', markdown[match.end():], re.M)
            if end_marker:
                stops.append(match.end() + end_marker.start())
        body = markdown[match.start():min(stops) if stops else len(markdown)].strip()
        heading = re.search(r'^#{3,4}\s+(.+)$', body, re.M)
        if heading is None:
            continue
        week = declared_week or next((int(chap.group(1)) for chap in reversed(chapters) if chap.start() < match.start()), None)
        exercises = set(EXERCISE_HEADING.findall(body))
        if declared_week is not None:
            exercises.update(re.findall(r'\[EX(\d{3,4})\]\(#exercise-ex\d{3,4}\)', body))
        lessons[number] = {
            "title": re.sub(r'^(?:Lesson|Aula|Lección|Day)\s+\d+\s+[—-]\s*', '', heading.group(1).strip()),
            "markdown": body, "chapter": week, "anchor": anchor,
            "exercise_ids": sorted(exercises),
        }
    return lessons


def worked_answers(book: str, chapter: str, exercise_ids: list[str] | None = None) -> str:
    numbers = set(exercise_ids) if exercise_ids is not None else set(EXERCISE.findall(chapter))
    supplementary = list(dict.fromkeys(re.findall(r'\]\(#(w\d+-answer-\d{2})\)', chapter)))
    if not numbers and not supplementary:
        return ""
    appendix = APPENDIX_HEADING.search(book)
    if not appendix:
        return ""
    answers = book[appendix.end():]
    matches = list(ANSWER.finditer(answers))
    pieces = []
    seen: set[str] = set()
    for index, match in enumerate(matches):
        digits = match.group(1) or match.group(2)
        if digits not in numbers or digits in seen:
            continue
        seen.add(digits)
        end = next((later.start() for later in matches[index + 1:]
                    if (later.group(1) or later.group(2)) != digits), len(answers))
        piece = answers[match.start():end]
        next_section = re.search(r'^#{2,3}\s+(?!EX\d{3,4}\b)', piece[match.end() - match.start():], re.M)
        if next_section:
            piece = piece[:match.end() - match.start() + next_section.start()]
        piece = re.sub(r'(?:\n\s*<a id="answer-ex\d{3,4}"></a>\s*)+$', '', piece)
        pieces.append(f'<a id="answer-ex{digits}"></a>\n' + piece.strip())
    for anchor in supplementary:
        match = re.search(rf'^<a id="{re.escape(anchor)}"></a>\s*$', answers, re.M)
        if not match:
            continue
        tail = answers[match.end():]
        end = re.search(r'^<a id="w\d+-answer-\d{2}"></a>\s*$|^##\s', tail, re.M)
        pieces.append((f'<a id="{anchor}"></a>' + tail[:end.start() if end else None]).strip())
    return "\n\n".join(pieces)


def exercise_prompts(book: str, exercise_ids: list[str]) -> str:
    """Bring a linked legacy prompt into an individual daily lesson."""
    if not exercise_ids:
        return ""
    appendix = APPENDIX_HEADING.search(book)
    teaching = book[:appendix.start()] if appendix else book
    pieces = []
    for digits in exercise_ids:
        match = re.search(
            rf'^(?:#{{3,6}}\s+|[-*]\s+)?(?:\*\*)?EX{re.escape(digits)}\b[^\n]*',
            teaching, re.M,
        )
        if match:
            prompt = match.group(0)
            # A heading-style exercise may continue over several paragraphs;
            # a bold or list entry normally contains its entire task on one line.
            if prompt.startswith("#"):
                tail = teaching[match.end():]
                stop = re.search(r'^#{2,6}\s|^<!-- open-cyber-academy:', tail, re.M)
                prompt += tail[:stop.start() if stop else None].rstrip()
            pieces.append(f'<a id="exercise-ex{digits}"></a>\n' + prompt)
    return "\n\n".join(pieces)


def course_schedule(subjects: str) -> tuple[str, dict[int, tuple[int, str]]]:
    """Read the published curricular periods and subject names from SUBJECTS.md."""
    period_kind = "Module"
    schedule: dict[int, tuple[int, str]] = {}
    for line in subjects.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in {"Week", "Study day", "Month", "Semester", "Term", "Year", "Module"}:
            period_kind = cells[0]
            continue
        chapter = re.search(r"\[(\d{2,4})\]\(book/PLAN\.md#ch-\d{2,4}\)", cells[1])
        if cells[0].isdigit() and chapter:
            schedule[int(chapter.group(1))] = (int(cells[0]), cells[2])
    return period_kind, schedule


async def course_details(request: Request, level: str, area: str, language: str) -> dict[str, Any]:
    item = get_course(await catalog(request), level, area, language)
    plan_path = book_path(level, area, language, "PLAN.md")
    manuscript_path = book_path(level, area, language, "MANUSCRIPT.md")
    book = await source_text(request, manuscript_path)
    plan = await source_text(request, plan_path)
    if plan is None:
        raise HTTPException(502, "Course plan is unavailable")
    try:
        subjects = await source_text(request, f"levels/{level}/{area}/{language}/SUBJECTS.md")
    except HTTPException:
        subjects = None
    period_kind, schedule = course_schedule(subjects or "")
    planned = chapter_sections(plan)
    authored = chapter_sections(book) if book is not None else {}
    planned_daily = lesson_sections(plan)
    authored_daily = lesson_sections(book) if book is not None else {}
    has_daily_lessons = bool(planned_daily or authored_daily)
    chapter_lessons = bool(book and CHAPTER_LESSONS_MARKER in book and not has_daily_lessons)
    indexed_daily = (planned.keys() | authored.keys()) if chapter_lessons else (planned_daily.keys() | authored_daily.keys())
    daily_schedule_ready = (has_daily_lessons or chapter_lessons) and len(indexed_daily) >= item["daily_lesson_target"]
    daily_target = max(item["daily_lesson_target"], *indexed_daily, 0)
    daily_slots: list[dict[str, Any]] = []
    for number in range(1, daily_target + 1):
        section = (authored.get(number) or planned.get(number)) if chapter_lessons else (authored_daily.get(number) or planned_daily.get(number))
        period = (number - 1) // 5 + 1 if chapter_lessons else (section.get("chapter") if section else (number - 1) // 5 + 1)
        published = number in (authored if chapter_lessons else authored_daily)
        source_anchor = f"ch-{number:02d}" if chapter_lessons and section else (section.get("anchor") if section else None)
        daily_slots.append({
            "chapter": number,
            "module": period,
            "title": re.sub(r'^(?:Chapter|Capítulo)\s+\d+\s+[—-]\s*', '', section["title"]) if chapter_lessons and section else section["title"] if section else (
                f"Dia de estudo {number} — conteúdo ainda não escrito" if language == "pt" else
                f"Día de estudio {number} — contenido aún no escrito" if language == "es" else
                f"Study day {number} — teaching not yet written"
            ),
            "published": published,
            "source_url": (GITHUB_VIEW + (manuscript_path if published else plan_path) + "#" + source_anchor)
            if source_anchor else None,
        })
    legacy_chapters = [
        {"chapter": number, "title": re.sub(r'^(?:Chapter|Capítulo)\s+\d+\s+[—-]\s*', '', (authored.get(number) or planned[number])["title"])
         if chapter_lessons else (authored.get(number) or planned[number])["title"],
         "published": number in authored, "module": schedule.get(number, (1, ""))[0],
         "source_url": GITHUB_VIEW + manuscript_path + f"#ch-{number:02d}" if number in authored else None}
        for number in sorted(planned.keys() | authored.keys())
    ]
    lessons = []
    modules: list[dict[str, Any]] = []
    source_planned = planned_daily if has_daily_lessons else planned
    source_authored = authored_daily if has_daily_lessons else authored
    for number in sorted(source_planned.keys() | source_authored.keys()):
        section = source_authored[number] if number in source_authored else source_planned[number]
        title = re.sub(r'^(?:Chapter|Capítulo)\s+\d+\s+[—-]\s*', '', section["title"]) if chapter_lessons else section["title"]
        if has_daily_lessons:
            period = section.get("chapter") or (number - 1) // 5 + 1
            subject = re.sub(r'^(?:Chapter|Capítulo)\s+\d+\s+[—-]\s*', '', (authored.get(period) or planned.get(period) or {"title": title})["title"])
        elif chapter_lessons:
            period = (number - 1) // 5 + 1
            subject = f"Study days {(period - 1) * 5 + 1}–{period * 5}"
        else:
            period, subject = schedule.get(number, (1, title))
        lessons.append({
            "chapter": number,
            "title": title,
            "subject": subject,
            "module": period,
            "published": number in source_authored,
            "source_url": GITHUB_VIEW + (manuscript_path if number in source_authored else plan_path) + "#" + (
                section.get("anchor", f"lesson-{number:02d}") if has_daily_lessons else f"ch-{number:02d}"),
        })
        if not modules or modules[-1]["number"] != period:
            modules.append({"number": period, "kind": "Week" if chapter_lessons else "Chapter" if has_daily_lessons else period_kind, "title": subject, "chapters": []})
        modules[-1]["chapters"].append(number)
    return {
        "course": item,
        "language": language,
        "lessons": lessons,
        "modules": modules,
        "daily_slots": daily_slots,
        "legacy_chapters": legacy_chapters,
        "published_chapters": len(authored),
        "planned_chapters": len(planned.keys() | authored.keys()),
        "published_lessons": len(authored) if chapter_lessons else len(authored_daily),
        "planned_lessons": daily_target,
        "has_daily_lessons": has_daily_lessons or chapter_lessons,
        "chapter_lessons": chapter_lessons,
        "daily_schedule_ready": daily_schedule_ready,
        "book_url": GITHUB_VIEW + manuscript_path if authored else None,
        "source_sha256": hashlib.sha256(book.encode("utf-8")).hexdigest() if book is not None else None,
        "source_branch": "main",
        "notice": "A published lesson may still need editorial review. A plan is not a lesson. Lesson length is not a quota.",
    }


async def lesson_details(request: Request, level: str, area: str, language: str, chapter: int, legacy: bool = False) -> dict[str, Any]:
    data = await catalog(request)
    course = get_course(data, level, area, language)
    if chapter < 1 or chapter > 9999:
        raise HTTPException(404, "Unknown chapter")
    path = book_path(level, area, language, "MANUSCRIPT.md")
    book = await source_text(request, path)
    if book is None:
        raise HTTPException(404, "This edition has no authored manuscript yet")
    daily = lesson_sections(book)
    sections = chapter_sections(book) if legacy or not daily else daily
    section = sections.get(chapter)
    if section is None:
        raise HTTPException(404, "This chapter is still a plan")
    chapters = sorted(sections)
    exercise_ids = section.get("exercise_ids", sorted(set(EXERCISE_PROMPT.findall(section["markdown"]))))
    markdown = section["markdown"]
    if daily and not legacy and not EXERCISE_HEADING.search(markdown):
        prompts = exercise_prompts(book, exercise_ids)
        if prompts:
            markdown += "\n\n### Exercise for this lesson\n\n" + prompts
    chapter_lesson = CHAPTER_LESSONS_MARKER in book and not daily
    course_code = f'OCA-{int(course["number"]):03d}'
    unit_kind = "A" if (daily and not legacy) or chapter_lesson else "C"
    unit_code = f'{course_code}-{unit_kind}{chapter:03d}'
    return {
        "course": {"level": level, "area": area, "language": language},
        "course_code": course_code,
        "unit_code": unit_code,
        "chapter": chapter,
        "title": re.sub(r'^(?:Chapter|Capítulo)\s+\d+\s+[—-]\s*', '', section["title"]) if chapter_lesson else section["title"],
        "markdown": markdown,
        "worked_answers": worked_answers(book, markdown, exercise_ids),
        "exercise_ids": exercise_ids,
        "week_chapter": section.get("chapter"),
        "content_kind": "chapter_lesson" if chapter_lesson else "legacy_chapter" if legacy or not daily else "daily_lesson",
        "chapter_lesson": chapter_lesson,
        "previous": max((n for n in chapters if n < chapter), default=None),
        "next": min((n for n in chapters if n > chapter), default=None),
        "source_url": GITHUB_VIEW + path + "#" + (section.get("anchor", f"lesson-{chapter:02d}") if daily and not legacy else f"ch-{chapter:02d}"),
        "markdown_url": f"/courses/{level}/{area}/{'chapters' if legacy or not daily else 'lessons'}/{language}/{chapter}.md",
        "source_sha256": hashlib.sha256(book.encode("utf-8")).hexdigest(),
        "content_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
        "source_branch": "main",
        "editorial_note": "Public teaching text; publication does not certify that the complete book passed editorial review.",
    }


@app.get("/api/practice/{level}/{area}/{route}/{language}/{number}")
async def api_lesson_practice(request: Request, level: str, area: str, route: str,
                              language: str, number: int) -> Response:
    """Serve source-pinned, reviewed five-choice exercises; no account is needed to practice."""
    if route not in {"lessons", "chapters"} or not all(re.fullmatch(r"[a-z0-9-]+", part)
                                                     for part in (level, area, language)):
        raise HTTPException(404, "Unknown lesson")
    lesson = await lesson_details(request, level, area, language, number, legacy=route == "chapters")
    if route == "lessons" and lesson["content_kind"] != "daily_lesson":
        raise HTTPException(404, "This edition uses chapter pages")
    path = f"web/practice-banks/{level}/{area}/{language}/{route}/{number:03d}.json"
    raw = await source_text(request, path)
    if raw is None:
        raise HTTPException(404, "No reviewed five-choice exercise is published for this unit")
    try:
        bank = validate_practice(raw, level, area, language, route, number,
                                 lesson["content_sha256"], lesson["exercise_ids"])
    except InvalidPractice as exc:
        raise HTTPException(409, str(exc)) from exc
    return JSONResponse(bank, headers={"Cache-Control": "no-store", "Content-Language": language})


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"service": "OpenCyber Academy", "status": "ok", "source": "https://github.com/hiagokinlevi/OpenCyberAcademy"}


@app.get("/api/insights")
async def public_insights(request: Request, path: str = "/", exercise: str = "", breakdown: bool = False,
                          edition: str = "") -> Response:
    language = language_for_host(request.headers.get("host", "")) or "en"
    data = await public_usage_counts(database(request), path=path, language=language,
                                     exercise_id=exercise, breakdown=breakdown, edition=edition)
    return JSONResponse(data, headers={"Cache-Control": "public, max-age=60", "X-Content-Type-Options": "nosniff"})


@app.post("/api/insights/collect", status_code=204)
async def public_insights_collect(request: Request, payload: PublicUsageEvent) -> Response:
    if request.headers.get("origin") not in ALLOWED_ORIGINS:
        raise HTTPException(403, "Use the Academy site to record public usage")
    if request.headers.get("sec-gpc") == "1" or request.headers.get("dnt") == "1":
        return Response(status_code=204)
    language = language_for_host(request.headers.get("host", "")) or "en"
    await collect_public_usage(database(request), visitor=payload.visitor, event=payload.event,
                               path=payload.path, language=language, exercise_id=payload.exercise_id,
                               edition=payload.edition)
    return Response(status_code=204, headers={"Cache-Control": "no-store"})


@app.get("/private/login")
async def private_login(next: str = "/account/") -> Response:
    # Compatibility for old links. Student sign-in now lives on the branded site.
    destination = next if next.startswith(("/tests/", "/courses/")) and not next.startswith("//") and "\\" not in next and len(next) < 1000 else None
    target = "/account/?next=" + quote(destination, safe="") if destination else "/account/"
    return RedirectResponse(target, status_code=302)


@app.get("/private/me")
@app.get("/student/me")
async def api_me(request: Request) -> Response:
    user = await identity(request)
    return JSONResponse({"email": user.get("email"), "username": user.get("username"),
                         "student_id": user["sub"]}, headers={"Cache-Control": "no-store"})


@app.get("/private/progress")
@app.get("/student/progress")
async def api_progress(request: Request) -> Response:
    user = await identity(request)
    db = database(request)
    lessons = await db.prepare("SELECT level, area, language, chapter, status, updated_at FROM lesson_progress WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500").bind(user["sub"]).all()
    exercises = await db.prepare("SELECT level, area, language, chapter, exercise_id, answer, status, updated_at FROM exercise_attempts WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500").bind(user["sub"]).all()
    return JSONResponse({"lessons": d1_rows(lessons), "exercises": d1_rows(exercises)}, headers={"Cache-Control": "no-store"})


@app.post("/private/progress/lesson")
@app.post("/student/progress/lesson")
async def api_progress_lesson(request: Request, payload: LessonProgress) -> Response:
    same_origin(request)
    user = await identity(request)
    await lesson_details(request, payload.level, payload.area, payload.language, payload.chapter)
    db = database(request)
    await db.prepare("INSERT INTO lesson_progress (user_id, level, area, language, chapter, status) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT (user_id, level, area, language, chapter) DO UPDATE SET status = excluded.status, updated_at = datetime('now')").bind(user["sub"], payload.level, payload.area, payload.language, payload.chapter, payload.status).run()
    await record_activity(db, user["sub"], "lesson_completed" if payload.status == "completed" else "lesson_opened",
                          payload.level, payload.area, payload.language, payload.chapter)
    return JSONResponse({"saved": True}, headers={"Cache-Control": "no-store"})


@app.post("/private/progress/exercise")
@app.post("/student/progress/exercise")
async def api_progress_exercise(request: Request, payload: ExerciseAttempt) -> Response:
    same_origin(request)
    user = await identity(request)
    lesson = await lesson_details(request, payload.level, payload.area, payload.language, payload.chapter,
                                  legacy=payload.unit_kind == "chapter")
    if payload.exercise_id.removeprefix("EX") not in lesson["exercise_ids"]:
        raise HTTPException(404, "Exercise is not in this lesson")
    db = database(request)
    await db.prepare("INSERT INTO exercise_attempts (user_id, level, area, language, chapter, exercise_id, answer, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (user_id, level, area, language, chapter, exercise_id) DO UPDATE SET answer = excluded.answer, status = excluded.status, updated_at = datetime('now')").bind(user["sub"], payload.level, payload.area, payload.language, payload.chapter, payload.exercise_id, payload.answer, payload.status).run()
    await record_activity(db, user["sub"], "exercise_answered", payload.level, payload.area,
                          payload.language, payload.chapter, exercise_id=payload.exercise_id)
    return JSONResponse({"saved": True}, headers={"Cache-Control": "no-store"})


@app.post("/student/activity")
async def api_learning_activity(request: Request, payload: LearningActivity) -> Response:
    same_origin(request)
    user = await student_identity(request)
    await lesson_details(request, payload.level, payload.area, payload.language, payload.chapter)
    if (payload.kind == "lesson_read") != (payload.seconds > 0):
        raise HTTPException(422, "Read time must be positive only for lesson_read")
    db = database(request)
    now = int(time.time())
    await _limit(db, f"activity:{user['sub']}:{now // 3600}", (now // 3600 + 1) * 3600, 180)
    await record_activity(db, user["sub"], payload.kind, payload.level, payload.area,
                          payload.language, payload.chapter, seconds=payload.seconds)
    return JSONResponse({"saved": True}, headers={"Cache-Control": "no-store"})


@app.post("/student/analysis")
async def api_save_analysis(request: Request, payload: StudentAnalysis) -> Response:
    same_origin(request)
    user = await student_identity(request)
    await lesson_details(request, payload.level, payload.area, payload.language, payload.chapter)
    db = database(request)
    await db.prepare(
        "INSERT INTO student_analysis (user_id, level, area, language, chapter, note) VALUES (?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(user_id, level, area, language, chapter) DO UPDATE SET note = excluded.note, updated_at = datetime('now')"
    ).bind(user["sub"], payload.level, payload.area, payload.language, payload.chapter, payload.note).run()
    await record_activity(db, user["sub"], "analysis_saved", payload.level, payload.area, payload.language, payload.chapter)
    return JSONResponse({"saved": True}, headers={"Cache-Control": "no-store"})


@app.get("/student/analysis")
async def api_get_analysis(request: Request, level: str, area: str, language: str, chapter: int) -> Response:
    user = await student_identity(request)
    get_course(await catalog(request), level, area, language)
    return JSONResponse({"analysis": await load_student_analysis(database(request), user["sub"], level, area, language, chapter)},
                        headers={"Cache-Control": "no-store"})


async def load_student_analysis(db: Any, user_id: str, level: str, area: str,
                                language: str, chapter: int) -> dict | None:
    notes = d1_rows(await db.prepare(
        "SELECT note, updated_at FROM student_analysis WHERE user_id = ? AND level = ? AND area = ? AND language = ? AND chapter = ?"
    ).bind(user_id, level, area, language, chapter).all())
    return notes[0] if notes else None


@app.get("/student/analyses")
async def api_list_analyses(request: Request) -> Response:
    user = await student_identity(request)
    notes = d1_rows(await database(request).prepare(
        "SELECT level, area, language, chapter, updated_at FROM student_analysis "
        "WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500"
    ).bind(user["sub"]).all())
    return JSONResponse({"analyses": notes}, headers={"Cache-Control": "no-store"})


@app.get("/student/stats")
async def api_student_stats(request: Request) -> Response:
    user = await student_identity(request)
    db = database(request)
    recent = activity_rows(await db.prepare(
        "SELECT kind, level, area, language, chapter, exercise_id, seconds, score, source, occurred_at "
        "FROM student_activity WHERE user_id = ? ORDER BY occurred_at DESC LIMIT 50"
    ).bind(user["sub"]).all())
    return JSONResponse({"summary": await activity_summary(db, user["sub"]),
                         "courses": await course_performance(db, user["sub"]), "recent": recent},
                        headers={"Cache-Control": "no-store"})


async def chapter_test_bank(request: Request, level: str, area: str, language: str, chapter: int,
                            check_source: bool = False) -> tuple[dict[str, Any], str]:
    get_course(await catalog(request), level, area, language)
    path = f"web/question-banks/{level}/{area}/{language}/{chapter:03d}.json"
    raw = await source_text(request, path)
    if raw is None:
        raise HTTPException(404, "No authored test is published for this chapter")
    try:
        bank, digest = validate_bank(raw, level, area, language, chapter)
    except InvalidBank as exc:
        raise HTTPException(503, f"Published test failed validation: {exc}") from exc
    if check_source:
        book = await source_text(request, book_path(level, area, language, "MANUSCRIPT.md"))
        if book is None:
            raise HTTPException(409, "The chapter has no published teaching")
        section = chapter_sections(book).get(chapter)
        if not section or hashlib.sha256(section["markdown"].encode("utf-8")).hexdigest() != bank["source_sha256"]:
            raise HTTPException(409, "The chapter changed; its test needs editorial review")
    return bank, digest


@app.get("/api/tests/catalog")
async def api_test_catalog(request: Request) -> dict[str, Any]:
    """Show coverage only. Answers are never delivered by this endpoint."""
    return await test_index(request)


@app.post("/private/tests/start")
@app.post("/student/tests/start")
async def api_test_start(request: Request, payload: TestStart) -> Response:
    same_origin(request)
    student = await identity(request)
    return JSONResponse(await start_test(request, payload, student), headers={"Cache-Control": "no-store"})


async def start_test(request: Request, payload: TestStart, student: dict, *, source: str = "site") -> dict:
    bank, digest = await chapter_test_bank(request, payload.level, payload.area, payload.language, payload.chapter, check_source=True)
    db = database(request)
    attempt_id = secrets.token_urlsafe(18)
    now_ms = int(time.time() * 1000)
    deadline_ms = now_ms + 11_000  # ten seconds for the learner plus one second for transit
    await db.prepare(
        "INSERT INTO chapter_test_attempts (id, user_id, level, area, language, chapter, bank_sha256, deadline_ms, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')"
    ).bind(attempt_id, student["sub"], payload.level, payload.area, payload.language, payload.chapter, digest, deadline_ms).run()
    await record_activity(db, student["sub"], "test_started", payload.level, payload.area, payload.language, payload.chapter,
                          source=source)
    return {"attempt_id": attempt_id, "chapter": payload.chapter, "question": public_question(bank, 0, deadline_ms, now_ms)}


@app.post("/private/tests/answer")
@app.post("/student/tests/answer")
async def api_test_answer(request: Request, payload: TestAnswer) -> Response:
    same_origin(request)
    student = await identity(request)
    return JSONResponse(await answer_test(request, payload, student), headers={"Cache-Control": "no-store"})


async def answer_test(request: Request, payload: TestAnswer, student: dict, *, source: str = "site") -> dict:
    db = database(request)
    result = await db.prepare(
        "SELECT * FROM chapter_test_attempts WHERE id = ? AND user_id = ?"
    ).bind(payload.attempt_id, student["sub"]).all()
    rows = d1_rows(result)
    if not rows:
        raise HTTPException(404, "Test attempt not found")
    attempt = rows[0]
    index = int(attempt["next_index"])
    if attempt["status"] != "active" or index != payload.index or index >= 10:
        raise HTTPException(409, "This question was already answered")
    bank, digest = await chapter_test_bank(request, attempt["level"], attempt["area"], attempt["language"], int(attempt["chapter"]))
    if digest != attempt["bank_sha256"]:
        raise HTTPException(409, "The test changed; start a new attempt")
    now_ms = int(time.time() * 1000)
    scored = score_answer(bank, index, payload.selected, now_ms <= int(attempt["deadline_ms"]))
    answers = json.loads(attempt["answers_json"])
    if len(answers) != index:
        raise HTTPException(409, "Test attempt state is inconsistent")
    answers.append(scored)
    new_score = int(attempt["score"]) + int(scored["correct"])
    next_index = index + 1
    next_deadline = now_ms + 11_000 if next_index < 10 else 0
    update = await db.prepare(
        "UPDATE chapter_test_attempts SET next_index = ?, score = ?, deadline_ms = ?, answers_json = ?, status = ?, updated_at = datetime('now') "
        "WHERE id = ? AND user_id = ? AND next_index = ? AND status = 'active' AND bank_sha256 = ?"
    ).bind(next_index, new_score, next_deadline, json.dumps(answers, ensure_ascii=False),
           "complete" if next_index == 10 else "active", payload.attempt_id, student["sub"], index, digest).run()
    if d1_changes(update) != 1:
        raise HTTPException(409, "Another answer already advanced this attempt")
    await record_activity(db, student["sub"], "test_answered", attempt["level"], attempt["area"],
                          attempt["language"], int(attempt["chapter"]), score=int(scored["correct"]), source=source)
    if next_index < 10:
        item = bank["questions"][index]
        review = {**scored, "answer": item["correct"], "explanation": item["explanation"], "source": item["source"]}
        return {"attempt_id": payload.attempt_id, "question": public_question(bank, next_index, next_deadline, now_ms),
                "review": review}
    return {"attempt_id": payload.attempt_id, "complete": True, "score": new_score, "total": 10,
            "perfect": new_score == 10, "feedback": feedback(bank, answers)}


@app.get("/private/tests/state")
@app.get("/student/tests/state")
async def api_test_state(request: Request, attempt_id: str = Query(pattern=r"^[A-Za-z0-9_-]{16,80}$")) -> Response:
    student = await identity(request)
    return JSONResponse(await test_state(request, attempt_id, student), headers={"Cache-Control": "no-store"})


async def test_state(request: Request, attempt_id: str, student: dict) -> dict:
    db = database(request)
    found = await db.prepare(
        "SELECT * FROM chapter_test_attempts WHERE id = ? AND user_id = ?"
    ).bind(attempt_id, student["sub"]).all()
    rows = d1_rows(found)
    if not rows:
        raise HTTPException(404, "Test attempt not found")
    attempt = rows[0]
    bank, digest = await chapter_test_bank(request, attempt["level"], attempt["area"], attempt["language"], int(attempt["chapter"]))
    if digest != attempt["bank_sha256"]:
        raise HTTPException(409, "The test changed; start a new attempt")
    if attempt["status"] == "complete":
        score = int(attempt["score"])
        return {"attempt_id": attempt_id, "complete": True, "score": score, "total": 10,
                "perfect": score == 10, "feedback": feedback(bank, json.loads(attempt["answers_json"]))}
    now_ms = int(time.time() * 1000)
    return {"attempt_id": attempt_id, "question": public_question(
        bank, int(attempt["next_index"]), int(attempt["deadline_ms"]), now_ms)}


@app.get("/private/tests/results")
@app.get("/student/tests/results")
async def api_test_results(request: Request, level: str, area: str, language: str) -> Response:
    student = await identity(request)
    return JSONResponse(await test_results(request, level, area, language, student),
                        headers={"Cache-Control": "no-store"})


async def test_results(request: Request, level: str, area: str, language: str, student: dict) -> dict:
    get_course(await catalog(request), level, area, language)
    db = database(request)
    rows = await db.prepare(
        "SELECT chapter, bank_sha256, MAX(score) AS best_score, MAX(updated_at) AS last_attempt "
        "FROM chapter_test_attempts WHERE user_id = ? AND level = ? AND area = ? AND language = ? AND status = 'complete' "
        "GROUP BY chapter, bank_sha256 ORDER BY chapter"
    ).bind(student["sub"], level, area, language).all()
    return {"results": d1_rows(rows)}


@app.post("/private/tests/certificate")
@app.post("/student/tests/certificate")
async def api_test_certificate(request: Request, payload: CertificateClaim) -> Response:
    same_origin(request)
    student = await identity(request)
    course = get_course(await catalog(request), payload.level, payload.area, payload.language)
    book = await source_text(request, book_path(payload.level, payload.area, payload.language, "MANUSCRIPT.md"))
    if book is None:
        raise HTTPException(409, "This course has no complete authored book")
    book_sha = hashlib.sha256(book.encode("utf-8")).hexdigest()
    approvals = await approved_books(request)
    approved = any(
        item.get("level") == payload.level and item.get("area") == payload.area
        and item.get("language") == payload.language and item.get("book_sha256") == book_sha
        for item in approvals.get("books", [])
    )
    if not approved:
        raise HTTPException(409, "This book has not passed the course-completion editorial gate")
    published = chapter_sections(book)
    expected = set(range(1, int(course["planned_chapters"]) + 1))
    if set(published) != expected:
        raise HTTPException(409, "Not every planned chapter is authored")
    coverage = (await test_index(request))["courses"].get(f"{payload.level}/{payload.area}/{payload.language}", [])
    if {item["chapter"] for item in coverage} != expected:
        raise HTTPException(409, "Not every chapter has a published test")
    for item in coverage:
        section = published[item["chapter"]]["markdown"]
        if hashlib.sha256(section.encode("utf-8")).hexdigest() != item["source_sha256"]:
            raise HTTPException(409, "A chapter changed; its test needs editorial review")
    db = database(request)
    result = await db.prepare(
        "SELECT chapter, bank_sha256 FROM chapter_test_attempts WHERE user_id = ? AND level = ? AND area = ? "
        "AND language = ? AND status = 'complete' AND score = 10"
    ).bind(student["sub"], payload.level, payload.area, payload.language).all()
    passed = {(int(row["chapter"]), row["bank_sha256"]) for row in d1_rows(result)}
    if any((item["chapter"], item["bank_sha256"]) not in passed for item in coverage):
        raise HTTPException(409, "Complete every chapter test with ten correct answers first")
    certificate_id = secrets.token_urlsafe(18)
    await db.prepare(
        "INSERT OR IGNORE INTO course_certificates (id, user_id, level, area, language, book_sha256) VALUES (?, ?, ?, ?, ?, ?)"
    ).bind(certificate_id, student["sub"], payload.level, payload.area, payload.language, book_sha).run()
    issued = await db.prepare(
        "SELECT id, issued_at FROM course_certificates WHERE user_id = ? AND level = ? AND area = ? AND language = ? AND book_sha256 = ?"
    ).bind(student["sub"], payload.level, payload.area, payload.language, book_sha).all()
    certificate = d1_rows(issued)[0]
    return JSONResponse({"certificate_id": certificate["id"], "issued_at": certificate["issued_at"],
                         "certificate_url": f"/student/certificates/{certificate['id']}" if request.url.path.startswith("/student/") else f"/private/certificates/{certificate['id']}",
                         "verify_url": f"https://opencyber.academy/api/certificates/{certificate['id']}"},
                        headers={"Cache-Control": "no-store"})


@app.get("/private/certificates/{certificate_id}")
@app.get("/student/certificates/{certificate_id}")
async def api_certificate_view(request: Request, certificate_id: str) -> Response:
    student = await identity(request)
    if not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", certificate_id):
        raise HTTPException(404, "Certificate not found")
    db = database(request)
    found = await db.prepare(
        "SELECT level, area, language, book_sha256, issued_at FROM course_certificates WHERE id = ? AND user_id = ?"
    ).bind(certificate_id, student["sub"]).all()
    rows = d1_rows(found)
    if not rows:
        raise HTTPException(404, "Certificate not found")
    item = rows[0]
    course = get_course(await catalog(request), item["level"], item["area"], item["language"])
    title = html.escape(course.get("titles", {}).get(item["language"], course["title"]))
    learner = html.escape(str(student.get("username") or student.get("email") or student["sub"]))
    issued = html.escape(item["issued_at"])
    verify_url = f"https://opencyber.academy/api/certificates/{certificate_id}"
    page = f"""<!doctype html><html lang="{html.escape(item['language'])}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Course completion · OpenCyber Academy</title>
<style>body{{font:18px/1.6 system-ui,sans-serif;background:#071123;color:#f7f7f3;margin:0;padding:5vw}}
main{{max-width:850px;margin:auto;border:2px solid #c9a75e;padding:clamp(24px,5vw,70px);background:#0e1c35}}
.eyebrow{{color:#d7b76b;letter-spacing:.18em;text-transform:uppercase;font-size:.76rem}}h1{{font-size:clamp(2rem,5vw,4rem);line-height:1.1}}
.learner{{font-size:1.5rem;font-weight:600}}a{{color:#e2c27b;overflow-wrap:anywhere}}small{{color:#bdc8d5}}
@media print{{body{{background:white;color:#141c2c}}main{{background:white;border-color:#876a2d}}.eyebrow,a{{color:#876a2d}}small{{color:#424a58}}button{{display:none}}}}
</style></head><body><main><div class="eyebrow">OpenCyber Academy · Self-study</div>
<h1>Course completion certificate</h1><p>This certifies that</p><p class="learner">{learner}</p>
<p>completed all published chapter assessments with a score of 10/10 in:</p><h2>{title}</h2>
<p>Issued {issued} UTC · Certificate ID {html.escape(certificate_id)}</p>
<p><a href="{verify_url}">Verify this certificate</a></p>
<small>Free self-study credential. This is not an accredited degree or a proctored examination.</small>
<p><button onclick="window.print()">Print certificate</button></p></main></body></html>"""
    return HTMLResponse(page, headers={"Cache-Control": "private, no-store", "X-Robots-Tag": "noindex, nofollow"})


@app.get("/api/certificates/{certificate_id}")
async def api_certificate_verify(request: Request, certificate_id: str) -> Response:
    if not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", certificate_id):
        raise HTTPException(404, "Certificate not found")
    db = database(request)
    found = await db.prepare(
        "SELECT level, area, language, book_sha256, issued_at FROM course_certificates WHERE id = ?"
    ).bind(certificate_id).all()
    rows = d1_rows(found)
    if not rows:
        raise HTTPException(404, "Certificate not found")
    return JSONResponse({"issuer": "OpenCyber Academy", "credential": "Self-study course completion",
                         "accredited_degree": False, **rows[0]}, headers={"Cache-Control": "no-store"})


@app.get("/api/catalog")
async def api_catalog(request: Request) -> dict[str, Any]:
    return await catalog(request)


@app.get("/api/courses/{level}/{area}/{language}")
async def api_course(request: Request, level: str, area: str, language: str) -> dict[str, Any]:
    return await course_details(request, level, area, language)


@app.get("/api/lessons/{level}/{area}/{language}/{chapter}")
async def api_lesson(request: Request, level: str, area: str, language: str, chapter: int) -> dict[str, Any]:
    return await lesson_details(request, level, area, language, chapter)


@app.get("/api/chapters/{level}/{area}/{language}/{chapter}")
async def api_chapter(request: Request, level: str, area: str, language: str, chapter: int) -> dict[str, Any]:
    """Read an authored subject chapter even during a partial daily conversion."""
    return await lesson_details(request, level, area, language, chapter, legacy=True)


@app.get("/courses/{level}/{area}/lessons/{language}/{chapter}.md", include_in_schema=False)
async def public_lesson_markdown(request: Request, level: str, area: str, language: str, chapter: int) -> Response:
    lesson = await lesson_details(request, level, area, language, chapter)
    if lesson["content_kind"] != "daily_lesson":
        return RedirectResponse(f"/courses/{level}/{area}/chapters/{language}/{chapter}.md", status_code=308)
    return lesson_markdown_response(lesson, language)


@app.get("/courses/{level}/{area}/chapters/{language}/{chapter}.md", include_in_schema=False)
async def public_chapter_markdown(request: Request, level: str, area: str, language: str, chapter: int) -> Response:
    return lesson_markdown_response(await lesson_details(request, level, area, language, chapter, legacy=True), language)


def lesson_markdown_response(lesson: dict[str, Any], language: str) -> Response:
    """A stable Markdown address for one authored unit, backed by the one book."""
    text = lesson["markdown"]
    if lesson["worked_answers"]:
        text += "\n\n## Worked answers\n\n" + lesson["worked_answers"]
    return PlainTextResponse(text + "\n", media_type="text/markdown; charset=utf-8", headers={
        "Cache-Control": "no-store", "Content-Language": language,
        "X-OpenCyberAcademy-Unit": lesson["unit_code"],
        "X-OpenCyberAcademy-Source-SHA256": lesson["source_sha256"],
        "X-Content-Type-Options": "nosniff",
    })


@app.get("/courses/{level}/{area}/lessons/{language}/{chapter}/", include_in_schema=False)
async def public_lesson_page(request: Request, level: str, area: str, language: str, chapter: int) -> Response:
    data = await catalog(request)
    course = get_course(data, level, area, language)
    try:
        lesson = await lesson_details(request, level, area, language, chapter)
    except HTTPException as exc:
        if exc.status_code != 404:
            raise
        guide = await course_details(request, level, area, language)
        if chapter < 1 or chapter > guide["planned_lessons"]:
            raise
        slot = guide["daily_slots"][chapter - 1]
        published_chapter = next((item for item in guide["legacy_chapters"]
                                  if item["chapter"] == slot["module"] and item["published"]), None)
        page = render_planned_lesson_page(course, slot, language, data["level_names"][level].get(language, data["level_names"][level]["en"]), published_chapter)
        return HTMLResponse(page, headers={"Cache-Control": "no-store", "Content-Language": language,
                                           "X-Robots-Tag": "noindex, follow", "X-Content-Type-Options": "nosniff"})
    if lesson["content_kind"] != "daily_lesson":
        return RedirectResponse(lesson_path(level, area, language, chapter, "chapter"), status_code=308)
    level_name = data["level_names"][level].get(language, data["level_names"][level]["en"])
    guide = await course_details(request, level, area, language)
    available_tests = {item["chapter"] for item in (await test_index(request))["courses"].get(f"{level}/{area}/{language}", [])}
    return HTMLResponse(render_lesson_page(lesson, course, level_name, guide=guide, available_test_chapters=available_tests), headers={"Cache-Control": "no-store", "Content-Language": language, "X-Content-Type-Options": "nosniff"})


@app.get("/courses/{level}/{area}/chapters/{language}/{chapter}/", include_in_schema=False)
async def public_chapter_page(request: Request, level: str, area: str, language: str, chapter: int) -> Response:
    data = await catalog(request)
    course = get_course(data, level, area, language)
    lesson = await lesson_details(request, level, area, language, chapter, legacy=True)
    level_name = data["level_names"][level].get(language, data["level_names"][level]["en"])
    kind = "chapter_lesson" if lesson["chapter_lesson"] else "chapter"
    guide = await course_details(request, level, area, language)
    available_tests = {item["chapter"] for item in (await test_index(request))["courses"].get(f"{level}/{area}/{language}", [])}
    return HTMLResponse(render_lesson_page(lesson, course, level_name, kind, guide, available_tests), headers={"Cache-Control": "no-store", "Content-Language": language, "X-Content-Type-Options": "nosniff"})


@app.get("/courses/{level}/{area}/start/", include_in_schema=False)
async def public_course_start(request: Request, level: str, area: str, lang: str | None = None) -> Response:
    """The course selector always opens the first currently authored lesson."""
    language = lang if lang in LANGUAGES else language_for_host(request.headers.get("host", "")) or "en"
    guide = await course_details(request, level, area, language)
    daily = [] if guide["chapter_lessons"] else [unit for unit in guide["daily_slots"] if unit["published"]]
    chapters = [unit for unit in guide["legacy_chapters"] if unit["published"]]
    first = daily[0] if daily else chapters[0] if chapters else None
    target = (lesson_path(level, area, language, int(first["chapter"]), "lesson" if daily else "chapter")
              if first else f"/courses/{level}/{area}/")
    return RedirectResponse(site_for_language(language) + target, status_code=302,
                            headers={"Cache-Control": "no-store"})


@app.get("/courses/{level}/{area}/", include_in_schema=False)
async def public_course_page(request: Request, level: str, area: str, lang: str | None = None) -> Response:
    """Keep the course directory in sync with main without rebuilding Astro."""
    hostname_language = language_for_host(request.headers.get("host", "")) or "en"
    language = lang if lang in LANGUAGES else hostname_language
    if language != hostname_language and language in ACTIVE_INTERFACES:
        return RedirectResponse(site_for_language(language) + f"/courses/{level}/{area}/", status_code=308)
    data = await catalog(request)
    course = get_course(data, level, area, language)
    asset = f"courses/{level}/{area}/index.html"
    if hostname_language in {"pt", "es"}:
        asset = f"_locales/{hostname_language}/{asset}"
    env = request.scope.get("env")
    if env is not None:
        source = await env.ASSETS.fetch("https://assets.local/" + asset)
        if int(source.status) != 200:
            raise HTTPException(503, "Course page is unavailable")
        page = str(await source.text())
    else:
        target = Path(__file__).resolve().parents[1] / "dist" / asset
        if not target.is_file():
            raise HTTPException(503, "Course page is unavailable")
        page = target.read_text(encoding="utf-8")
    guide = await course_details(request, level, area, language)
    directory = render_course_focus(course, language) + render_course_directory(guide, level, area, language, int(course["number"]))
    if '<div id="live-lesson-directory"></div>' not in page:
        raise HTTPException(503, "Course page needs a current deployment")
    page = page.replace('<div id="live-lesson-directory"></div>', directory, 1)
    if any(unit["published"] for unit in guide["daily_slots"]) or any(unit["published"] for unit in guide["legacy_chapters"]):
        page = page.replace('<meta name="robots" content="noindex,follow">',
                            '<meta name="robots" content="index,follow,max-image-preview:large">', 1)
    level_name = data["level_names"][level].get(language, data["level_names"][level]["en"])
    course_name = course.get("titles", {}).get(language) or course["title"]
    localized_title = f"{level_name} · {course_name} · OpenCyber Academy"
    descriptions = {
        "en": f"{course.get('scope') or course_name} Free {level_name.lower()} course with published lessons, examples, exercises and worked answers.",
        "pt": f"Estude gratuitamente {course_name} no nível {level_name.lower()}. Acesse as aulas publicadas em sequência, com exemplos, exercícios e respostas comentadas.",
        "es": f"Estudia gratis {course_name} en el nivel {level_name.lower()}. Sigue las lecciones publicadas con ejemplos, ejercicios y respuestas desarrolladas.",
    }
    description = descriptions.get(language, descriptions["en"])
    for pattern, value in (
        (r"<title>[^<]*</title>", f"<title>{html.escape(localized_title)}</title>"),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(description, quote=True)}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(localized_title, quote=True)}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(description, quote=True)}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{html.escape(localized_title, quote=True)}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{html.escape(description, quote=True)}">'),
    ):
        page = re.sub(pattern, lambda _: value, page, count=1)
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, flags=re.S)
    if schema_match:
        schema = json.loads(schema_match.group(1))
        course_url = site_for_language(language) + f"/courses/{level}/{area}/"
        schema[0].update(name=f"{level_name} {course_name}", description=description,
                         url=course_url, inLanguage=language)
        crumbs = schema[1]["itemListElement"]
        crumbs[0]["item"] = site_for_language(language) + "/"
        crumbs[1].update(name=level_name, item=site_for_language(language) + f"/levels/{level}/")
        crumbs[2].update(name=course_name, item=course_url)
        script = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + '</script>'
        page = page[:schema_match.start()] + script + page[schema_match.end():]
    return HTMLResponse(page, headers={"Cache-Control": "no-store", "Content-Language": hostname_language,
                                       "X-Content-Type-Options": "nosniff"})


@app.get("/api/books/{level}/{area}/{language}")
async def api_book(request: Request, level: str, area: str, language: str) -> Response:
    get_course(await catalog(request), level, area, language)
    book = await source_text(request, book_path(level, area, language, "MANUSCRIPT.md"))
    if book is None:
        raise HTTPException(404, "This edition has no authored manuscript yet")
    return PlainTextResponse(book, media_type="text/markdown; charset=utf-8", headers={"Cache-Control": "no-store", "X-OpenCyberAcademy-Source-SHA256": hashlib.sha256(book.encode("utf-8")).hexdigest()})


@app.get("/api/source")
async def api_source(request: Request, path: str = Query(min_length=1, max_length=320)) -> Response:
    """Serve a public Markdown reference so course navigation stays on OpenCyber Academy."""
    if (not path.endswith(".md") or path.startswith("/") or "\\" in path
            or any(part in ("", ".", "..") for part in path.split("/"))
            or not re.fullmatch(r"[\w./-]+", path, re.UNICODE)):
        raise HTTPException(404, "Unknown public document")
    document = await source_text(request, path)
    if document is None:
        raise HTTPException(404, "Public document not found")
    return PlainTextResponse(document, media_type="text/markdown; charset=utf-8", headers={"Cache-Control": "public, max-age=60"})


@app.get("/api/search/{level}/{area}/{language}")
async def api_search(request: Request, level: str, area: str, language: str, q: str = Query(min_length=3, max_length=80)) -> dict[str, Any]:
    get_course(await catalog(request), level, area, language)
    book = await source_text(request, book_path(level, area, language, "MANUSCRIPT.md"))
    if book is None:
        raise HTTPException(404, "This edition has no authored manuscript yet")
    matches = []
    for chapter, section in chapter_sections(book).items():
        for match in re.finditer(re.escape(q), section["markdown"], re.I):
            start, end = max(0, match.start() - 100), min(len(section["markdown"]), match.end() + 100)
            matches.append({"chapter": chapter, "title": section["title"], "snippet": re.sub(r'\s+', ' ', section["markdown"][start:end])})
            if len(matches) == 20:
                return {"query": q, "results": matches, "truncated": True}
    return {"query": q, "results": matches, "truncated": False}


def rpc_result(identifier: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": identifier, "result": result}


def rpc_error(identifier: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": identifier, "error": {"code": code, "message": message}}


TOOLS = [
    {"name": "get_editorial_policy", "description": "Read the current public book standard and language production gate: English, then Portuguese, then Spanish; later languages begin only when all three collections are verified complete.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "list_courses", "description": "Discover the 207 public OpenCyber Academy courses. Optional language, level, area or title query filters.", "inputSchema": {"type": "object", "properties": {"language": {"type": "string"}, "level": {"type": "string"}, "area": {"type": "string"}, "query": {"type": "string"}}}},
    {"name": "list_lessons", "description": "List planned and authored lessons for one course. Only published=true represents written teaching.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}}, "required": ["level", "area", "language"]}},
    {"name": "read_lesson", "description": "Read the public Markdown for an authored lesson and its worked answers, with its GitHub source URL.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "start": {"type": "integer", "minimum": 0}, "max_chars": {"type": "integer", "minimum": 1000, "maximum": 50000}}, "required": ["level", "area", "language", "chapter"]}},
    {"name": "read_chapter", "description": "Read an authored legacy subject chapter during conversion to weekday lessons; plans are not returned as teaching.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "start": {"type": "integer", "minimum": 0}, "max_chars": {"type": "integer", "minimum": 1000, "maximum": 50000}}, "required": ["level", "area", "language", "chapter"]}},
    {"name": "search_course", "description": "Search within one authored manuscript; returns bounded snippets and chapter numbers.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "query": {"type": "string"}}, "required": ["level", "area", "language", "query"]}},
    {"name": "student_sign_in", "description": "Legacy credential exchange for existing provisioned clients. New clients should create a personal AI key from the signed-in account page; never put a password in prompts or tool arguments.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "student_get_stats", "description": "Read your own learning totals, recent activity and course performance with a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "student_get_progress", "description": "Read your own saved lessons and exercise attempts with a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "student_list_analyses", "description": "List your own saved lesson analyses (course, lesson and update time). Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "student_get_analysis", "description": "Read your own saved analysis for one lesson. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}}, "required": ["level", "area", "language", "chapter"]}},
    {"name": "student_read_lesson", "description": "Read an authored lesson as a student and record the visit. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "start": {"type": "integer", "minimum": 0}, "max_chars": {"type": "integer", "minimum": 1000, "maximum": 50000}}, "required": ["level", "area", "language", "chapter"]}},
    {"name": "student_save_analysis", "description": "Save your private analysis of an authored lesson with a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "note": {"type": "string", "minLength": 1, "maxLength": 10000}}, "required": ["level", "area", "language", "chapter", "note"]}},
    {"name": "student_save_lesson", "description": "Mark an authored lesson as in progress or completed for your account. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "status": {"type": "string", "enum": ["in_progress", "completed"]}}, "required": ["level", "area", "language", "chapter", "status"]}},
    {"name": "student_save_exercise", "description": "Save your answer to a published lesson or chapter exercise. Set unit_kind to chapter when using read_chapter; otherwise lesson. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}, "unit_kind": {"type": "string", "enum": ["lesson", "chapter"]}, "exercise_id": {"type": "string"}, "answer": {"type": "string"}}, "required": ["level", "area", "language", "chapter", "exercise_id", "answer"]}},
    {"name": "student_start_test", "description": "Start your published ten-question chapter test. Each question has a server-enforced deadline of ten seconds plus transit allowance. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}, "chapter": {"type": "integer"}}, "required": ["level", "area", "language", "chapter"]}},
    {"name": "student_answer_test", "description": "Submit your answer before its server deadline, or null to skip. Returns the next question or completed score. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"attempt_id": {"type": "string"}, "index": {"type": "integer", "minimum": 0, "maximum": 9}, "selected": {"type": ["string", "null"], "enum": ["a", "b", "c", "d", None]}}, "required": ["attempt_id", "index", "selected"]}},
    {"name": "student_test_state", "description": "Resume your timed chapter test or view its result. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"attempt_id": {"type": "string"}}, "required": ["attempt_id"]}},
    {"name": "student_test_results", "description": "Read your best saved chapter-test scores for one course edition. Requires a personal AI key or student bearer session.", "inputSchema": {"type": "object", "properties": {"level": {"type": "string"}, "area": {"type": "string"}, "language": {"type": "string"}}, "required": ["level", "area", "language"]}},
]


@app.post("/mcp")
async def mcp(request: Request) -> Response:
    origin = request.headers.get("origin")
    if origin and origin not in ALLOWED_ORIGINS:
        raise HTTPException(403, "Origin is not allowed")
    if "application/json" not in request.headers.get("content-type", ""):
        raise HTTPException(415, "MCP expects application/json")
    if "application/json" not in request.headers.get("accept", "") or "text/event-stream" not in request.headers.get("accept", ""):
        raise HTTPException(406, "MCP client must accept JSON and event stream")
    body = await request.body()
    if len(body) > 65_536:
        raise HTTPException(413, "MCP request too large")
    try:
        payload = json.loads(body)
    except ValueError:
        return JSONResponse(rpc_error(None, -32700, "Parse error"), status_code=400)
    if not isinstance(payload, dict) or payload.get("jsonrpc") != "2.0" or not isinstance(payload.get("method"), str):
        return JSONResponse(rpc_error(payload.get("id") if isinstance(payload, dict) else None, -32600, "Invalid Request"), status_code=400)
    if "id" not in payload:
        return Response(status_code=202)
    identifier, method = payload["id"], payload["method"]
    params = payload.get("params") or {}
    if not isinstance(params, dict):
        return JSONResponse(rpc_error(identifier, -32602, "Invalid params"))
    try:
        if method == "initialize":
            return JSONResponse(rpc_result(identifier, {"protocolVersion": MCP_VERSION, "capabilities": {"resources": {}, "tools": {}}, "serverInfo": {"name": "OpenCyber Academy", "version": "0.1.0"}}))
        if method == "ping":
            return JSONResponse(rpc_result(identifier, {}))
        if method == "tools/list":
            return JSONResponse(rpc_result(identifier, {"tools": TOOLS}))
        if method == "resources/list":
            return JSONResponse(rpc_result(identifier, {"resources": [
                {"uri": "open-cyber-academy://catalog", "name": "OpenCyber Academy course catalog", "mimeType": "application/json", "description": "207 courses in study order"},
                {"uri": EDITORIAL_POLICY_URI, "name": "OpenCyber Academy editorial policy", "mimeType": "text/markdown", "description": "Current public book standard and three-language production gate"},
            ]}))
        if method == "resources/templates/list":
            return JSONResponse(rpc_result(identifier, {"resourceTemplates": [
                {"uriTemplate": "open-cyber-academy://lesson/{level}/{area}/{language}/{chapter}", "name": "OpenCyber Academy lesson", "mimeType": "text/markdown", "description": "A published daily lesson, or a legacy chapter when this edition has no daily lessons"},
                {"uriTemplate": "open-cyber-academy://chapter/{level}/{area}/{language}/{chapter}", "name": "OpenCyber Academy subject chapter", "mimeType": "text/markdown", "description": "An authored legacy chapter retained during the daily lesson conversion"},
            ]}))
        if method == "resources/read":
            uri = params.get("uri", "")
            if uri == "open-cyber-academy://catalog":
                contents = [{"uri": uri, "mimeType": "application/json", "text": json.dumps(await catalog(request), ensure_ascii=False)}]
            elif uri == EDITORIAL_POLICY_URI:
                contents = [{"uri": uri, "mimeType": "text/markdown", "text": await editorial_policy(request)}]
            else:
                match = re.fullmatch(r'open-cyber-academy://(lesson|chapter)/([a-z0-9-]+)/([a-z0-9-]+)/([a-z]{2})/(\d{1,4})', str(uri))
                if not match:
                    return JSONResponse(rpc_error(identifier, -32602, "Unknown resource URI"))
                result = await lesson_details(request, match[2], match[3], match[4], int(match[5]), legacy=match[1] == "chapter")
                contents = [{"uri": uri, "mimeType": "text/markdown", "text": result["markdown"] + "\n\n## Worked answers for this lesson\n\n" + result["worked_answers"] + "\n\nSource: " + result["source_url"]}]
            return JSONResponse(rpc_result(identifier, {"contents": contents}))
        if method == "tools/call":
            name, args = params.get("name"), params.get("arguments") or {}
            if not isinstance(args, dict):
                return JSONResponse(rpc_error(identifier, -32602, "Invalid tool arguments"))
            private_tools = {"student_get_stats", "student_get_progress", "student_list_analyses",
                             "student_get_analysis", "student_read_lesson",
                             "student_save_analysis", "student_save_lesson", "student_save_exercise",
                             "student_start_test", "student_answer_test", "student_test_state",
                             "student_test_results"}
            student = None
            if name == "student_sign_in":
                try:
                    username, password = basic_credentials(request)
                    account = await password_account(request, username, password)
                except HTTPException as exc:
                    return JSONResponse(rpc_error(identifier, -32001, "Student sign-in failed"),
                                        status_code=exc.status_code,
                                        headers={"WWW-Authenticate": 'Basic realm="OpenCyber Academy students"'})
                token = await create_session(database(request), account["sub"])
                result = {"student_id": account["sub"], "username": account["username"],
                          "access_token": token, "token_type": "Bearer", "expires_in": SESSION_LIFETIME}
                return JSONResponse(rpc_result(identifier, {"content": [{"type": "text", "text": json.dumps(result)}]}))
            if name in private_tools:
                try:
                    student = await mcp_student_identity(request)
                except HTTPException as exc:
                    return JSONResponse(rpc_error(identifier, -32001, "A student bearer session is required"),
                                        status_code=exc.status_code,
                                        headers={"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else {})
            if name == "get_editorial_policy":
                result = {"markdown": await editorial_policy(request), "source_url": GITHUB_VIEW + "BOOK_STANDARD.md"}
            elif name == "list_courses":
                data = await catalog(request)
                courses = data["courses"]
                for key in ("level", "area"):
                    if args.get(key):
                        courses = [item for item in courses if item[key] == args[key]]
                if args.get("query"):
                    courses = [item for item in courses if str(args["query"]).casefold() in item["title"].casefold()]
                result = {"courses": courses, "total": len(courses), "source": data["source"]}
            elif name == "list_lessons":
                result = await course_details(request, args["level"], args["area"], args["language"])
            elif name in {"read_lesson", "read_chapter"}:
                result = await lesson_details(request, args["level"], args["area"], args["language"], int(args["chapter"]), legacy=name == "read_chapter")
                start = max(0, int(args.get("start", 0)))
                length = min(50_000, max(1000, int(args.get("max_chars", 30000))))
                text = result.pop("markdown")
                result["markdown"] = text[start:start + length]
                result["next_start"] = start + length if start + length < len(text) else None
                result["total_chars"] = len(text)
            elif name == "search_course":
                result = await api_search(request, args["level"], args["area"], args["language"], str(args["query"]))
            elif name == "student_get_stats":
                result = await activity_summary(database(request), student["sub"])
                result["courses"] = await course_performance(database(request), student["sub"])
                result["recent"] = activity_rows(await database(request).prepare(
                    "SELECT kind, level, area, language, chapter, exercise_id, seconds, score, source, occurred_at "
                    "FROM student_activity WHERE user_id = ? ORDER BY occurred_at DESC LIMIT 50"
                ).bind(student["sub"]).all())
            elif name == "student_get_progress":
                db = database(request)
                lessons = activity_rows(await db.prepare(
                    "SELECT level, area, language, chapter, status, updated_at FROM lesson_progress WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500"
                ).bind(student["sub"]).all())
                exercises = activity_rows(await db.prepare(
                    "SELECT level, area, language, chapter, exercise_id, answer, status, updated_at FROM exercise_attempts WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500"
                ).bind(student["sub"]).all())
                result = {"lessons": lessons, "exercises": exercises}
            elif name == "student_list_analyses":
                result = {"analyses": activity_rows(await database(request).prepare(
                    "SELECT level, area, language, chapter, updated_at FROM student_analysis "
                    "WHERE user_id = ? ORDER BY updated_at DESC LIMIT 500"
                ).bind(student["sub"]).all())}
            elif name == "student_get_analysis":
                get_course(await catalog(request), str(args["level"]), str(args["area"]), str(args["language"]))
                result = {"analysis": await load_student_analysis(database(request), student["sub"],
                    str(args["level"]), str(args["area"]), str(args["language"]), int(args["chapter"]))}
            elif name == "student_read_lesson":
                data = TestStart(**args)
                result = await lesson_details(request, data.level, data.area, data.language, data.chapter)
                await record_activity(database(request), student["sub"], "lesson_opened",
                                      data.level, data.area, data.language, data.chapter, source="mcp")
                start = max(0, int(args.get("start", 0)))
                length = min(50_000, max(1000, int(args.get("max_chars", 30000))))
                markdown = result.pop("markdown")
                result["markdown"] = markdown[start:start + length]
                result["next_start"] = start + length if start + length < len(markdown) else None
                result["total_chars"] = len(markdown)
            elif name == "student_save_analysis":
                data = StudentAnalysis(**args)
                await lesson_details(request, data.level, data.area, data.language, data.chapter)
                db = database(request)
                await db.prepare(
                    "INSERT INTO student_analysis (user_id, level, area, language, chapter, note) VALUES (?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(user_id, level, area, language, chapter) DO UPDATE SET note = excluded.note, updated_at = datetime('now')"
                ).bind(student["sub"], data.level, data.area, data.language, data.chapter, data.note).run()
                await record_activity(db, student["sub"], "analysis_saved", data.level, data.area, data.language, data.chapter,
                                      source="mcp")
                result = {"saved": True}
            elif name == "student_save_lesson":
                data = LessonProgress(**args)
                await lesson_details(request, data.level, data.area, data.language, data.chapter)
                db = database(request)
                await db.prepare(
                    "INSERT INTO lesson_progress (user_id, level, area, language, chapter, status) VALUES (?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(user_id, level, area, language, chapter) DO UPDATE SET status = excluded.status, updated_at = datetime('now')"
                ).bind(student["sub"], data.level, data.area, data.language, data.chapter, data.status).run()
                await record_activity(db, student["sub"], "lesson_completed" if data.status == "completed" else "lesson_opened",
                                      data.level, data.area, data.language, data.chapter, source="mcp")
                result = {"saved": True}
            elif name == "student_save_exercise":
                data = ExerciseAttempt(**{**args, "status": "attempted"})
                lesson = await lesson_details(request, data.level, data.area, data.language, data.chapter,
                                              legacy=data.unit_kind == "chapter")
                if data.exercise_id.removeprefix("EX") not in lesson["exercise_ids"]:
                    raise HTTPException(404, "Exercise is not in this lesson")
                db = database(request)
                await db.prepare(
                    "INSERT INTO exercise_attempts (user_id, level, area, language, chapter, exercise_id, answer, status) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, 'attempted') "
                    "ON CONFLICT(user_id, level, area, language, chapter, exercise_id) DO UPDATE SET "
                    "answer = excluded.answer, status = excluded.status, updated_at = datetime('now')"
                ).bind(student["sub"], data.level, data.area, data.language, data.chapter, data.exercise_id, data.answer).run()
                await record_activity(db, student["sub"], "exercise_answered", data.level, data.area,
                                      data.language, data.chapter, exercise_id=data.exercise_id, source="mcp")
                result = {"saved": True}
            elif name == "student_start_test":
                result = await start_test(request, TestStart(**args), student, source="mcp")
            elif name == "student_answer_test":
                result = await answer_test(request, TestAnswer(**args), student, source="mcp")
            elif name == "student_test_state":
                result = await test_state(request, str(args["attempt_id"]), student)
            elif name == "student_test_results":
                result = await test_results(request, str(args["level"]), str(args["area"]),
                                            str(args["language"]), student)
            else:
                return JSONResponse(rpc_error(identifier, -32602, "Unknown tool"))
            return JSONResponse(rpc_result(identifier, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}))
        return JSONResponse(rpc_error(identifier, -32601, "Method not found"))
    except (KeyError, ValueError, TypeError):
        return JSONResponse(rpc_error(identifier, -32602, "Invalid params"))
    except HTTPException as exc:
        return JSONResponse(rpc_result(identifier, {"content": [{"type": "text", "text": str(exc.detail)}], "isError": True}))


@app.get("/mcp")
async def mcp_get() -> Response:
    return Response(status_code=405, headers={"Allow": "POST"})


async def tabletop_source(request: Request) -> dict[str, Any]:
    raw = await source_text(request, "web/tabletop/scenarios.json")
    if raw is None:
        raise HTTPException(503, "TableTop scenarios are unavailable")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(503, "TableTop scenarios are invalid") from exc


@app.get("/tabletop/", include_in_schema=False)
async def tabletop_index(request: Request) -> Response:
    language = language_for_host(request.headers.get("host", "")) or "en"
    if language not in ACTIVE_INTERFACES:
        return RedirectResponse(site_for_language("en") + "/tabletop/", status_code=302)
    try:
        page = render_tabletop_index(await tabletop_source(request), language)
    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(503, "TableTop scenarios are invalid") from exc
    return HTMLResponse(page, headers={"Cache-Control": "no-store", "Content-Language": language})


@app.get("/tabletop/{slug}/", include_in_schema=False)
async def tabletop_case(request: Request, slug: str) -> Response:
    language = language_for_host(request.headers.get("host", "")) or "en"
    if language not in ACTIVE_INTERFACES:
        return RedirectResponse(site_for_language("en") + f"/tabletop/{quote(slug)}/", status_code=302)
    try:
        page = render_tabletop_case(await tabletop_source(request), language, slug)
    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(503, "TableTop scenarios are invalid") from exc
    if page is None:
        raise HTTPException(404, "Unknown TableTop scenario")
    return HTMLResponse(page, headers={"Cache-Control": "no-store", "Content-Language": language})


@app.get("/robots.txt", include_in_schema=False)
async def robots(request: Request) -> Response:
    language = language_for_host(request.headers.get("host", "")) or "en"
    site = site_for_language(language)
    return PlainTextResponse(f"User-agent: *\nAllow: /\nSitemap: {site}/sitemap.xml\n")


@app.get("/sitemap.xml", include_in_schema=False)
async def localized_sitemap(request: Request) -> Response:
    language = language_for_host(request.headers.get("host", "")) or "en"
    return await static_assets(f"sitemap-{language}.xml", request)


@app.get("/sitemaps/{level}/{area}/{language}.xml", include_in_schema=False)
async def course_sitemap(request: Request, level: str, area: str, language: str) -> Response:
    """Discover new and edited lessons in an existing book directly from main."""
    get_course(await catalog(request), level, area, language)
    if language != (language_for_host(request.headers.get("host", "")) or "en"):
        return RedirectResponse(site_for_language(language) + f"/sitemaps/{level}/{area}/{language}.xml", status_code=302)
    book = await source_text(request, book_path(level, area, language, "MANUSCRIPT.md"))
    if book is None:
        raise HTTPException(404, "This edition has no authored lessons")
    daily = lesson_sections(book)
    chapters = chapter_sections(book)
    if CHAPTER_LESSONS_MARKER in book and not daily:
        daily = {}
    if not daily and not chapters:
        raise HTTPException(404, "This edition has no authored lessons")
    base = site_for_language(language) + f"/courses/{level}/{area}/"
    urls = [base]
    urls += [f"{base}lessons/{language}/{number}/" for number in sorted(daily)]
    urls += [f"{base}chapters/{language}/{number}/" for number in sorted(chapters)]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body += ''.join(f"  <url><loc>{html.escape(url)}</loc></url>\n" for url in urls)
    body += "</urlset>\n"
    return Response(body, media_type="application/xml", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


@app.get("/{path:path}", include_in_schema=False)
async def static_assets(path: str, request: Request) -> Response:
    asset = path.strip("/")
    if not asset or "." not in asset.rsplit("/", 1)[-1]:
        asset = (asset + "/" if asset else "") + "index.html"
    language = language_for_host(request.headers.get("host", "")) or "en"
    if language not in ACTIVE_INTERFACES and asset.endswith("index.html"):
        if asset != "index.html":
            return RedirectResponse(site_for_language(language) + "/", status_code=302)
        asset = f"_locales/{language}/index.html"
    elif language in {"pt", "es"} and asset.endswith("index.html"):
        asset = f"_locales/{language}/{asset}"
    env = request.scope.get("env")
    if env is not None:
        response = await env.ASSETS.fetch("https://assets.local/" + asset)
        content = await response.bytes()
        headers = dict(response.headers)
        if asset.endswith("index.html"):
            headers["Content-Language"] = language
        return Response(content=content, status_code=int(response.status), headers=headers)
    root = Path(__file__).resolve().parents[1] / "dist"
    target = (root / asset).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise HTTPException(404, "Page not found")
    return FileResponse(target, headers={"Content-Language": language} if asset.endswith("index.html") else None)
