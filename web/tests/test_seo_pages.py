"""Search pages must expose real authored lessons and safe, stable metadata."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import app, worked_answers
from seo_pages import render_lesson_page


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def client():
    app.state.catalog_override = json.loads((ROOT / "web/public/catalog.json").read_text())

    async def local_source(path):
        file = ROOT / path
        return file.read_text(encoding="utf-8") if file.is_file() else None

    app.state.source_override = local_source
    try:
        yield TestClient(app)
    finally:
        del app.state.catalog_override
        del app.state.source_override


def test_authored_lesson_has_indexable_html_and_stable_navigation(client):
    path = "/courses/rapid-1-month/incident-response-resilience/lessons/en/1/"
    response = client.get(path)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.headers["content-language"] == "en"
    assert response.headers["cache-control"] == "no-store"
    assert f'<link rel="canonical" href="https://opencyber.academy{path}">' in response.text
    assert '<meta name="robots" content="index,follow' in response.text
    assert '"@type":"LearningResource"' in response.text
    assert '"@type":"BreadcrumbList"' in response.text
    assert '"isAccessibleForFree":true' in response.text
    structured = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.S).group(1))
    assert structured[0]["url"] == f"https://opencyber.academy{path}"
    assert structured[1]["itemListElement"][-1]["item"] == f"https://opencyber.academy{path}"
    assert '<article class="prose" lang="en">' in response.text
    assert '<nav aria-label="Published lessons">' in response.text
    assert 'href="/courses/rapid-1-month/incident-response-resilience/lessons/en/1/" aria-current="page"' in response.text
    assert 'href="/courses/rapid-1-month/incident-response-resilience/lessons/en/20/"' in response.text
    assert '<link rel="next" href="https://opencyber.academy/courses/rapid-1-month/incident-response-resilience/lessons/en/2/">' in response.text
    assert 'id="progress-metrics" hidden' in response.text
    assert 'data-published="20"' in response.text
    assert 'href="/tests/?lang=en&amp;area=incident-response-resilience&amp;level=rapid-1-month&amp;chapter=1"' in response.text
    assert 'OCA-016-A001 · ' in response.text
    assert "An incident response team does more than react" in response.text
    assert 'id="exercise-ex001"' in response.text
    assert 'id="answer-ex001"' in response.text
    assert 'href="#answer-ex001"' in response.text
    assert 'data-insight="page.browsers"' in response.text
    assert 'data-exercise-browsers="EX001"' in response.text
    assert '/lessons/en/2/' in response.text
    assert 'src="/analytics.js"' in response.text
    assert client.get("/courses/rapid-1-month/incident-response-resilience/lessons/en/21/").status_code == 404
    chapter_only = client.get("/courses/rapid-1-month/information-security/lessons/en/1/", follow_redirects=False)
    assert chapter_only.status_code == 308
    assert chapter_only.headers["location"] == "/courses/rapid-1-month/information-security/chapters/en/1/"


@pytest.mark.parametrize("language,area,label", [
    ("en", "cybersecurity", "Share this lesson"),
    ("pt", "information-security", "Compartilhar esta aula"),
    ("es", "information-security", "Compartir esta lección"),
])
def test_published_chapter_can_share_its_canonical_link(client, language, area, label):
    path = f"/courses/rapid-1-month/{area}/chapters/{language}/1/"
    response = client.get(path, headers={"host": f"{language}.opencyber.academy"})
    assert response.status_code == 200
    origin = "https://opencyber.academy" if language == "en" else f"https://{language}.opencyber.academy"
    canonical = origin + path
    assert f'<link rel="canonical" href="{canonical}">' in response.text
    assert f'id="share-lesson" type="button" data-url="{canonical}"' in response.text
    assert label in response.text
    assert f'<a href="{canonical}">' in response.text


def test_lesson_test_link_uses_its_week_and_chapter_matches_published_index(client):
    for lesson_number, chapter in ((5, 1), (6, 2), (11, 3), (16, 4)):
        response = client.get(f"/courses/rapid-1-month/incident-response-resilience/lessons/en/{lesson_number}/")
        assert f'href="/tests/?lang=en&amp;area=incident-response-resilience&amp;level=rapid-1-month&amp;chapter={chapter}"' in response.text
    published = client.get("/courses/rapid-1-month/information-security/chapters/en/1/")
    assert 'href="/tests/?lang=en&amp;area=information-security&amp;level=rapid-1-month&amp;chapter=1"' in published.text
    privacy = client.get("/courses/rapid-1-month/privacy-data-protection/chapters/en/1/")
    index = json.loads((ROOT / "web/public/test-index.json").read_text())
    published_privacy = any(item["chapter"] == 1 for item in
                            index["courses"].get("rapid-1-month/privacy-data-protection/en", []))
    if published_privacy:
        assert 'href="/tests/?lang=en&amp;area=privacy-data-protection&amp;level=rapid-1-month&amp;chapter=1"' in privacy.text
    else:
        assert "A chapter test has not been published yet." in privacy.text


def test_translated_chapters_use_localized_course_names_in_search_and_navigation(client):
    cases = (
        ("pt", "quantum-post-quantum-security", "Profissionalizante", "Segurança quântica e pós-quântica", "Navegação entre aulas"),
        ("es", "ot-iot-security", "Profesional", "Seguridad de OT, IoT y sistemas ciberfísicos", "Navegación entre lecciones"),
    )
    for language, area, level_name, course_name, navigation in cases:
        path = f"/courses/professional-6-months/{area}/chapters/{language}/1/"
        response = client.get(path, headers={"host": f"{language}.opencyber.academy"})
        assert response.status_code == 200
        assert f'<html lang="{language}"' in response.text
        assert f"{level_name} {course_name} | OpenCyber Academy</title>" in response.text
        assert f'aria-label="{navigation}"' in response.text
        structured = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.S).group(1))
        assert structured[0]["isPartOf"]["name"] == course_name
        assert structured[0]["educationalLevel"] == level_name


def test_portuguese_chapter_reads_as_a_lesson_on_small_screens(client):
    path = "/courses/rapid-1-month/data-governance/chapters/pt/1/"
    response = client.get(path, headers={"host": "pt.opencyber.academy"})
    assert response.status_code == 200
    page = response.text
    article = page.split('<article class="prose" lang="pt">', 1)[1].split("</article>", 1)[0]
    assert page.count('<h1 id="ch-01">Capítulo 1 — Governança de dados: fundamentos e primeiras decisões</h1>') == 1
    assert "<h2>Capítulo 1 — Governança de dados: fundamentos e primeiras decisões</h2>" not in article
    assert "Próximo capítulo →" in page
    assert "Próxima capítulo" not in page
    assert "Código do curso: <strong>OCA-003</strong>" in page
    assert "Capítulo 01: <strong>OCA-003-C001</strong>" in page
    assert "OCA-003-C002" in page
    assert "Continue estudando — aula 01" not in article
    assert '"courseCode":"OCA-003"' in page
    assert '<nav aria-label="Aulas publicadas">' in page
    assert 'href="/courses/rapid-1-month/data-governance/chapters/pt/1/" aria-current="page"' in page
    assert 'href="/courses/rapid-1-month/data-governance/chapters/pt/2/"' in page
    assert '<link rel="next" href="https://pt.opencyber.academy/courses/rapid-1-month/data-governance/chapters/pt/2/">' in page
    assert '<script src="/seo-diagrams.js" defer></script>' in page
    assert '<code class="language-mermaid">' in article  # Accessible source before client rendering.
    assert '<div class="table-scroll" role="region" tabindex="0"' in article
    assert '<details class="rubric"><summary>Mostrar critérios de avaliação</summary>' in article
    assert "EX001 — Tamanho do negócio." in article
    assert '<summary>Respostas comentadas</summary>' in page
    assert 'id="answer-ex001"' in page and 'id="answer-ex051"' in page
    assert 'id="answer-ex014"' not in page
    lesson = client.get("/api/chapters/rapid-1-month/data-governance/pt/1").json()
    assert lesson["course_code"] == "OCA-003"
    assert lesson["unit_code"] == "OCA-003-C001"


def test_daily_lesson_uses_distinct_sequential_code(client):
    response = client.get("/courses/rapid-1-month/incident-response-resilience/lessons/en/1/")
    assert response.status_code == 200
    assert "OCA-016-A001" in response.text
    assert "OCA-016-A002" in response.text
    assert '"identifier":"OCA-016-A001"' in response.text
    article = response.text.split('<article class="prose" lang="en">', 1)[1].split("</article>", 1)[0]
    assert "Continue studying — lesson 01" not in article
    assert "Lesson 01 — Evidence readiness and the first case question" not in article
    assert '<h1 id="lesson-01">Evidence readiness and the first case question</h1>' in response.text


@pytest.mark.parametrize("path,exercise", [
    ("/courses/professional-6-months/incident-response-resilience/lessons/en/1/", "EX001"),
    ("/courses/rapid-1-month/security-governance-risk-compliance/chapters/pt/1/", "EX001"),
    ("/courses/professional-6-months/ot-iot-security/chapters/es/1/", "EX001"),
])
def test_published_exercises_have_prompt_answer_and_five_choice_slot(client, path, exercise):
    response = client.get(path)
    assert response.status_code == 200
    page = response.text
    digits = exercise.removeprefix("EX")
    assert f'id="exercise-ex{digits}"' in page
    assert page.count(f'id="exercise-ex{digits}"') == 1
    assert f'id="answer-ex{digits}"' in page
    assert f'data-exercise-id="{exercise}"' in page
    assert 'id="lesson-practice"' in page
    assert '<textarea id="attempt-' not in page
    assert 'class="exercise-choice-options"' in page
    if "/lessons/en/" in path:
        assert "at least five dependencies" in page
    assert page.count(f'id="answer-ex{digits}"') == 1


def test_reviewed_practice_matches_the_published_exercise(client):
    route = "/api/practice/rapid-1-month/security-governance-risk-compliance/chapters/pt/8"
    response = client.get(route)
    assert response.status_code == 200
    question = response.json()["questions"][0]
    assert question["exercise_id"] == "EX062"
    assert len(question["options"]) == 5
    assert question["options"][1]["id"] == question["correct"] == "b"
    assert client.get(route.replace("/8", "/7")).status_code == 404
    page = client.get("/courses/rapid-1-month/security-governance-risk-compliance/chapters/pt/8/").text
    assert 'data-exercise-id="EX062"' in page
    assert '<textarea id="attempt-EX062"' not in page


@pytest.mark.parametrize("language", ["en", "pt", "es"])
def test_building_network_exercises_have_reviewed_choices_in_each_language(client, language):
    route = f"/api/practice/professional-6-months/ot-iot-security/chapters/{language}/3"
    response = client.get(route)
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert [question["exercise_id"] for question in questions] == [
        "EX011", "EX012", "EX013", "EX014", "EX015"
    ]
    assert all(len(question["options"]) == 5 for question in questions)
    chapter = client.get(f"/courses/professional-6-months/ot-iot-security/chapters/{language}/3/")
    assert chapter.status_code == 200
    for question in questions:
        assert f'data-exercise-id="{question["exercise_id"]}"' in chapter.text


def test_sitemap_lists_only_routes_that_resolve_to_authored_sections(client):
    sitemaps = {language: (ROOT / f"web/public/sitemap-{language}.xml").read_text()
                for language in ("en", "pt", "es", "he", "fr", "ru", "de", "zh", "ja")}
    sitemap = sitemaps["en"]
    index = json.loads((ROOT / "web/public/lesson-index.json").read_text())
    assert "https://opencyber.academy/sitemaps/rapid-1-month/incident-response-resilience/en.xml" in sitemap
    assert index["rapid-1-month/incident-response-resilience/en"]["lessons"][0]["number"] == 1
    info = index["rapid-1-month/information-security/en"]
    assert info["chapter_lessons"] is True
    assert len(info["chapters"]) == 20 and not info["lessons"]
    assert "https://pt.opencyber.academy/sitemaps/professional-6-months/quantum-post-quantum-security/pt.xml" in sitemaps["pt"]
    assert "https://es.opencyber.academy/sitemaps/professional-6-months/ot-iot-security/es.xml" in sitemaps["es"]
    for language, xml in sitemaps.items():
        urls = [node.text for node in ET.fromstring(xml).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        assert len(urls) == len(set(urls))
        assert all(url.startswith(f"https://{language + '.' if language != 'en' else ''}opencyber.academy/") for url in urls)
        if language not in {"en", "pt", "es"}:
            assert len(urls) == 1  # No translated manuscripts exist yet.
    assert sum(len(re.findall(r"<sitemap><loc>", xml)) for xml in sitemaps.values()) > 350
    live = client.get("/sitemaps/rapid-1-month/information-security/en.xml")
    assert "https://opencyber.academy/courses/rapid-1-month/information-security/chapters/en/20/" in live.text
    assert "https://opencyber.academy/courses/rapid-1-month/information-security/lessons/en/20/" not in live.text
    assert "https://opencyber.academy/courses/rapid-1-month/incident-response-resilience/lessons/en/21/" not in client.get("/sitemaps/rapid-1-month/incident-response-resilience/en.xml").text
    assert client.get("/sitemap.xml", headers={"host": "pt.opencyber.academy"}).text == sitemaps["pt"]
    assert "https://es.opencyber.academy/sitemap.xml" in client.get("/robots.txt", headers={"host": "es.opencyber.academy"}).text
    assert client.get("/api/catalog").headers["x-robots-tag"] == "noindex"


def test_sitemap_language_alternates_are_reciprocal_and_authored():
    sitemap_ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    xhtml_link = "{http://www.w3.org/1999/xhtml}link"
    pages = {}
    for language in ("en", "pt", "es"):
        root = ET.fromstring((ROOT / f"web/public/sitemap-{language}-pages.xml").read_text())
        for page in root.findall(f"{sitemap_ns}url"):
            pages[page.findtext(f"{sitemap_ns}loc")] = {
                alternate.attrib["hreflang"]: alternate.attrib["href"]
                for alternate in page.findall(xhtml_link)
            }

    variants = {language: f"https://{language + '.' if language != 'en' else ''}opencyber.academy/"
                for language in ("en", "pt", "es")}
    assert all(pages[url] == variants for url in variants.values())
    english_only = "https://opencyber.academy/courses/rapid-1-month/incident-response-resilience/"
    assert pages[english_only] == {}
    assert all(
        target in pages and pages[target] == alternates
        for alternates in pages.values() for target in alternates.values()
    )


def test_course_directory_and_markdown_follow_new_github_text_without_rebuild(client):
    level, area, language = "rapid-1-month", "application-supply-chain", "en"
    book_path = f"levels/{level}/{area}/{language}/book/MANUSCRIPT.md"
    original = app.state.source_override

    async def edited_source(path):
        text = await original(path)
        if path == book_path:
            return text + '\n<a id="ch-21"></a>\n## Chapter 21 — Newly published lesson\n\nA new explanation appears immediately.\n'
        return text

    app.state.source_override = edited_source
    try:
        directory = client.get(f"/courses/{level}/{area}/")
        assert directory.status_code == 200
        assert 'OCA-014-A021' in directory.text
        assert f'/courses/{level}/{area}/chapters/en/21/' in directory.text
        sitemap = client.get(f"/sitemaps/{level}/{area}/en.xml")
        assert sitemap.status_code == 200
        assert f'/courses/{level}/{area}/chapters/en/21/' in sitemap.text
        markdown = client.get(f"/courses/{level}/{area}/chapters/en/21.md")
        assert markdown.status_code == 200
        assert markdown.headers["x-opencyberacademy-unit"] == 'OCA-014-A021'
        assert "A new explanation appears immediately." in markdown.text
        html_page = client.get(f"/courses/{level}/{area}/chapters/en/21/")
        assert html_page.status_code == 200
        assert f'/courses/{level}/{area}/chapters/en/21.md' in html_page.text
        assert '<nav aria-label="Published lessons">' in html_page.text
        assert f'href="/courses/{level}/{area}/chapters/en/20/"' in html_page.text
        assert 'href="/courses/rapid-1-month/application-supply-chain/chapters/en/21/" aria-current="page"' in html_page.text
    finally:
        app.state.source_override = original


def test_course_selection_opens_first_published_lesson_and_course_guide_is_indexable(client):
    host = {"host": "pt.opencyber.academy"}
    route = "/courses/technical-18-months/data-governance/"
    start = client.get(route + "start/?lang=pt", headers=host, follow_redirects=False)
    assert start.status_code == 302
    assert start.headers["location"] == "https://pt.opencyber.academy/courses/technical-18-months/data-governance/chapters/pt/1/"
    course = client.get(route + "?lang=pt", headers=host)
    assert course.status_code == 200
    assert '<title>Técnico · Governança de dados · OpenCyber Academy</title>' in course.text
    assert 'name="description" content="Estude gratuitamente Governança de dados' in course.text
    assert 'name="robots" content="index,follow' in course.text
    assert 'id="course-start-link"' in course.text
    assert 'href="/courses/technical-18-months/data-governance/chapters/pt/1/"' in course.text
    assert 'href="/courses/technical-18-months/data-governance/chapters/pt/18/"' in course.text
    assert 'Carregando o livro' not in course.text
    assert 'id="course-reader-title"' not in course.text
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', course.text, re.S).group(1))
    assert schema[0]["inLanguage"] == "pt"
    assert schema[0]["name"] == "Técnico Governança de dados"


def test_language_hosts_and_unwritten_study_slots_are_honest(client):
    english_offer = client.get("/", headers={"host": "opencyber.academy", "accept-language": "pt-BR,pt;q=0.9,en;q=0.8"}, follow_redirects=False)
    assert english_offer.status_code == 200
    assert '<html lang="en">' in english_offer.text
    assert 'id="language-offer"' in english_offer.text
    assert client.get("/", headers={"host": "opencyber.academy", "accept-language": "en-US"}).status_code == 200
    for language in ("pt", "es"):
        host = f"{language}.opencyber.academy"
        home = client.get("/", headers={"host": host})
        about = client.get("/about/", headers={"host": host})
        assert home.status_code == about.status_code == 200
        assert f'<html lang="{language}">' in home.text
        assert f'https://{host}/about/' in about.text
        assert 'name="robots" content="index,follow' in home.text
        assert "Hiago Kin Levi" in about.text
    french = client.get("/", headers={"host": "fr.opencyber.academy"})
    assert french.status_code == 200 and 'content="noindex,follow"' in french.text
    guide = client.get("/api/courses/professional-6-months/incident-response-resilience/en").json()
    first_unpublished = next(slot["chapter"] for slot in guide["daily_slots"] if not slot["published"])
    planned = client.get(f"/courses/professional-6-months/incident-response-resilience/lessons/en/{first_unpublished}/", headers={"host": "opencyber.academy"})
    assert planned.status_code == 200
    assert planned.headers["x-robots-tag"] == "noindex, follow"
    assert "have not been published yet" in planned.text
    assert f"OCA-039-A{first_unpublished:03d}" in planned.text
    assert f"OCA-039-A{first_unpublished + 1:03d}" in planned.text
    assert f"/lessons/en/{first_unpublished + 1}/" in planned.text
    assert client.get("/courses/professional-6-months/incident-response-resilience/lessons/en/131/").status_code == 404
    cross_host = client.get("/courses/rapid-1-month/incident-response-resilience/lessons/pt/1/", headers={"host": "opencyber.academy"}, follow_redirects=False)
    assert cross_host.status_code == 308
    assert cross_host.headers["location"].startswith("https://pt.opencyber.academy/")


def test_chapter_with_final_appendix_exposes_its_own_worked_answer(client):
    path = "/courses/rapid-1-month/cybersecurity/chapters/en/20/"
    response = client.get(path)
    assert response.status_code == 200
    assert 'id="exercise-ex036"' in response.text
    assert 'id="answer-ex036"' in response.text
    assert "The outage cause is still not established" in response.text
    assert 'id="answer-ex035"' not in response.text
    assert 'href="https://opencyber.academy' + path + '"' in response.text
    assert "respuesta" in worked_answers(
        "## Resultados resueltos\n\n### EX001 — Respuesta\n\nUna respuesta.",
        "### EX001 — Ejercicio",
        ["001"],
    ).lower()


def test_authored_markdown_cannot_inject_script_or_foreign_click_target():
    lesson = {
        "course": {"level": "rapid-1-month", "area": "incident-response-resilience", "language": "en"},
        "chapter": 1, "title": "A lesson </script><script>alert(1)</script>",
        "markdown": "### A lesson\n\nTeaching text. <script>alert(1)</script> [bad](javascript:alert(1)) [next](#lesson-02)",
        "worked_answers": "", "previous": None, "next": 2,
        "source_url": "https://github.com/hiagokinlevi/OpenCyberAcademy/blob/main/levels/rapid-1-month/incident-response-resilience/en/book/MANUSCRIPT.md#lesson-01",
    }
    page = render_lesson_page(lesson, {"number": 16, "title": "Incident response"}, "Rapid course")
    assert "<script>alert(1)</script>" not in page
    assert 'href="javascript:' not in page
    assert 'href="/courses/rapid-1-month/incident-response-resilience/lessons/en/2/"' in page
    assert "\\u003c/script>" in page
    assert page.index('<div class="lesson-main">') < page.index('<aside class="course-sidebar"')
