"""Server-rendered course guide linking only to published, canonical units."""

from __future__ import annotations

import html
import re
from itertools import groupby

from seo_pages import lesson_path


TEXT = {
    "en": {"eyebrow": "YOUR COURSE PATH", "title": "Start with the first lesson", "description": "Read each published lesson in order. Every lesson has its own permanent page, examples, exercises and previous/next navigation.", "start": "Start learning", "guide": "Published course guide", "week": "Week", "lesson": "Lesson", "lessons": "lessons", "chapter": "Chapter", "chapters": "chapters", "none": "Lessons for this edition have not been published yet."},
    "pt": {"eyebrow": "SEU PERCURSO", "title": "Comece pela primeira aula", "description": "Estude as aulas publicadas em sequência. Cada aula tem página própria e permanente, exemplos, exercícios e navegação anterior/próxima.", "start": "Começar a estudar", "guide": "Roteiro do curso publicado", "week": "Semana", "lesson": "Aula", "lessons": "aulas", "chapter": "Capítulo", "chapters": "capítulos", "none": "As aulas desta edição ainda não foram publicadas."},
    "es": {"eyebrow": "TU RUTA DE ESTUDIO", "title": "Empieza por la primera lección", "description": "Estudia las lecciones publicadas en orden. Cada una tiene su página permanente, ejemplos, ejercicios y navegación anterior/siguiente.", "start": "Empezar a estudiar", "guide": "Guía del curso publicada", "week": "Semana", "lesson": "Lección", "lessons": "lecciones", "chapter": "Capítulo", "chapters": "capítulos", "none": "Todavía no se han publicado las lecciones de esta edición."},
}


def unit_title(value: str) -> str:
    return re.sub(r"^(?:Chapter|Capítulo|Lesson|Aula|Lección)\s+\d+\s*[—:-]\s*", "", value, flags=re.I).strip()


def render_course_focus(course: dict, language: str) -> str:
    """Show the source-backed curriculum brief only in its authored language."""
    if language != "en":
        return ""
    fields = [("Scope", "scope"), ("Audience", "audience"),
              ("Entry knowledge", "entry_knowledge"), ("Intended outcome", "exit_goal")]
    if any(not course.get(key) for _, key in fields):
        return ""
    items = "".join(f'<dt>{label}</dt><dd>{html.escape(str(course[key]))}</dd>' for label, key in fields)
    return ('<section class="shell course-focus" aria-labelledby="course-focus-title">'
            '<div class="eyebrow">COURSE BRIEF</div><h2 id="course-focus-title">What you will study</h2>'
            f'<dl>{items}</dl><p>The intended outcome is a learning goal, not a completion or accreditation claim.</p>'
            '</section>')


def render_course_directory(guide: dict, level: str, area: str, language: str, course_number: int) -> str:
    ui = TEXT.get(language, TEXT["en"])
    chapter_lessons = guide["chapter_lessons"]
    daily = [] if chapter_lessons else [unit for unit in guide["daily_slots"] if unit["published"]]
    chapters = [unit for unit in guide["legacy_chapters"] if unit["published"]]
    source_hash = html.escape(guide.get("source_sha256") or "", quote=True)
    code = f"OCA-{course_number:03d}"
    primary = daily if daily else chapters
    route = "lesson" if daily else "chapter"
    letter = "A" if daily or chapter_lessons else "C"
    label_key = "lesson" if daily or chapter_lessons else "chapter"
    if not primary:
        return (f'<section id="live-lesson-directory" class="shell published-lesson-directory" '
                f'data-source-sha256="{source_hash}"><h2>{ui["guide"]}</h2><p>{ui["none"]}</p></section>')

    first = primary[0]
    first_path = lesson_path(level, area, language, int(first["chapter"]), route)
    first_title = html.escape(unit_title(first["title"]))

    def link(unit: dict) -> str:
        number = int(unit["chapter"])
        target = lesson_path(level, area, language, number, route)
        title = html.escape(unit_title(unit["title"]))
        return (f'<li><a href="{target}"><span class="course-map-code">{code}-{letter}{number:03d}</span>'
                f'<span class="course-map-title">{title}</span><span class="course-map-arrow" aria-hidden="true">→</span></a></li>')

    if daily:
        sections = []
        for week, units in groupby(primary, key=lambda unit: int(unit.get("module") or (int(unit["chapter"]) - 1) // 5 + 1)):
            rows = ''.join(link(unit) for unit in units)
            sections.append(f'<section class="course-map-group"><h3>{ui["week"]} {week}</h3><ol>{rows}</ol></section>')
        body = ''.join(sections)
    else:
        body = f'<ol class="course-map-list">{"".join(link(unit) for unit in primary)}</ol>'
    return (
        f'<section id="live-lesson-directory" class="shell published-lesson-directory" data-source-sha256="{source_hash}" '
        f'aria-labelledby="published-lessons-title">'
        f'<div class="course-entry"><div><div class="eyebrow">{ui["eyebrow"]}</div>'
        f'<h2 id="published-lessons-title">{ui["title"]}</h2><p>{ui["description"]}</p>'
        f'<p class="course-entry-first">{code}-{letter}{int(first["chapter"]):03d} · {first_title}</p></div>'
        f'<a id="course-start-link" class="button gold" href="{first_path}">{ui["start"]} →</a></div>'
        f'<div class="course-map"><h2>{ui["guide"]}</h2><p>{len(primary)} '
        f'{ui[label_key if len(primary) == 1 else label_key + "s"].lower()}</p>'
        f'<div class="course-map-groups">{body}</div></div>'
        f'</section>'
    )
