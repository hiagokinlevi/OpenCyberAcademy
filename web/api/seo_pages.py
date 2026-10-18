"""Server-rendered, canonical HTML for public lessons and chapters."""

from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import parse_qs, quote, urljoin, urlparse

import bleach
import markdown
from locales import site_for_language


SITE = "https://opencyber.academy"
REPOSITORY = "hiagokinlevi/OpenCyberAcademy"
ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "article", "br", "caption", "code", "details", "div", "figure", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "img", "input", "main", "nav", "p", "pre", "section", "span", "summary", "table", "tbody", "td", "th", "thead", "tr",
}
ALLOWED_ATTRIBUTES = {
    "*": ["id", "class", "lang", "dir"],
    "a": ["href", "title", "id", "class"],
    "img": ["src", "alt", "title", "width", "height"],
    "input": ["type", "checked", "disabled"],
    "th": ["align"],
    "td": ["align"],
}
LANGUAGE_NAMES = {"en": "English", "pt": "Português", "es": "Español", "he": "עברית", "fr": "Français", "ru": "Русский", "de": "Deutsch", "zh": "中文", "ja": "日本語"}
PAGE_TEXT = {
    "en": {"lesson": "Lesson", "chapter": "Chapter", "course_code": "Course code", "previous": "Previous", "next": "Next", "guide": "Course guide", "all": "All lessons", "answers": "Worked answers", "criteria": "Show marking criteria", "table": "Lesson table; scroll horizontally to read all columns", "home": "Home", "free": "Open, free learning for anyone who wants to protect people and technology. No account is required to read this text or its worked answers."},
    "pt": {"lesson": "Aula", "chapter": "Capítulo", "course_code": "Código do curso", "previous": "Anterior", "next": "Próxima", "guide": "Guia do curso", "all": "Todas as aulas", "answers": "Respostas comentadas", "criteria": "Mostrar critérios de avaliação", "table": "Tabela da aula; deslize para ver todas as colunas", "home": "Início", "free": "Ensino gratuito e aberto para quem deseja proteger pessoas e tecnologias. Não é preciso criar uma conta para estudar ou consultar as respostas."},
    "es": {"lesson": "Lección", "chapter": "Capítulo", "course_code": "Código del curso", "previous": "Anterior", "next": "Siguiente", "guide": "Guía del curso", "all": "Todas las lecciones", "answers": "Respuestas desarrolladas", "criteria": "Mostrar criterios de evaluación", "table": "Tabla de la lección; desplázate para ver todas las columnas", "home": "Inicio", "free": "Aprendizaje gratuito y abierto para quienes desean proteger a las personas y la tecnología. No se necesita una cuenta para estudiar ni consultar las respuestas."},
}
PAGE_CHROME = {
    "en": {"skip": "Skip to lesson", "navigation": "Main navigation", "levels": "Levels", "subjects": "Subjects", "ai": "For AIs", "theme": "Toggle light and dark theme", "lesson_navigation": "Lesson navigation", "next_step": "Next study step", "footer": "Free public cybersecurity education", "api": "Open API and MCP"},
    "pt": {"skip": "Pular para a aula", "navigation": "Navegação principal", "levels": "Níveis", "subjects": "Temas", "ai": "Para IAs", "theme": "Alternar tema claro e escuro", "lesson_navigation": "Navegação entre aulas", "next_step": "Próxima etapa de estudo", "footer": "Educação pública e gratuita em cibersegurança", "api": "API e MCP abertos"},
    "es": {"skip": "Saltar a la lección", "navigation": "Navegación principal", "levels": "Niveles", "subjects": "Temas", "ai": "Para IA", "theme": "Cambiar entre tema claro y oscuro", "lesson_navigation": "Navegación entre lecciones", "next_step": "Siguiente etapa de estudio", "footer": "Educación pública y gratuita en ciberseguridad", "api": "API y MCP abiertos"},
}
STUDY_TEXT = {
    "en": {"published": "Published lessons", "chapters": "Book chapters", "week": "Week", "progress": "Your progress", "sign_in": "Sign in to track your study", "loading": "Loading your study record…", "completed": "Lessons completed", "exercises": "Exercises saved", "correct": "Correct test answers", "mark": "Mark this lesson complete", "marked": "Lesson completed", "dashboard": "View detailed progress", "tests": "Test this chapter", "tests_unavailable": "A chapter test has not been published yet.", "unavailable": "Progress is unavailable right now."},
    "pt": {"published": "Aulas publicadas", "chapters": "Capítulos do livro", "week": "Semana", "progress": "Seu progresso", "sign_in": "Entre para acompanhar seus estudos", "loading": "Carregando seu histórico…", "completed": "Aulas concluídas", "exercises": "Exercícios salvos", "correct": "Acertos nos testes", "mark": "Marcar esta aula como concluída", "marked": "Aula concluída", "dashboard": "Ver progresso detalhado", "tests": "Fazer teste do capítulo", "tests_unavailable": "O teste deste capítulo ainda não foi publicado.", "unavailable": "O progresso está indisponível agora."},
    "es": {"published": "Lecciones publicadas", "chapters": "Capítulos del libro", "week": "Semana", "progress": "Tu progreso", "sign_in": "Inicia sesión para seguir tus estudios", "loading": "Cargando tu historial…", "completed": "Lecciones completadas", "exercises": "Ejercicios guardados", "correct": "Aciertos en las pruebas", "mark": "Marcar esta lección como completada", "marked": "Lección completada", "dashboard": "Ver progreso detallado", "tests": "Hacer la prueba del capítulo", "tests_unavailable": "La prueba de este capítulo aún no se ha publicado.", "unavailable": "El progreso no está disponible ahora."},
}


def lesson_path(level: str, area: str, language: str, number: int, kind: str = "lesson") -> str:
    route = "lessons" if kind == "lesson" else "chapters"
    return f"/courses/{level}/{area}/{route}/{language}/{number}/"


def plain_description(source: str, fallback: str) -> str:
    """Use authored prose, not an outline or a fabricated excerpt."""
    for paragraph in re.split(r"\n\s*\n", source):
        if paragraph.lstrip().startswith(("#", "<a ", "**Week ", "**Month ", "```", "|", "- ")):
            continue
        paragraph = re.sub(r"<[^>]+>|`+|\[([^]]+)\]\([^)]*\)|[*_#>]", r"\1", paragraph)
        paragraph = " ".join(paragraph.split())
        if len(paragraph) >= 55 and not paragraph.startswith(("|", "```", "!")):
            return paragraph[:157].rstrip(" .,;:") + ("…" if len(paragraph) > 157 else "")
    return fallback


def local_link(href: str, source_url: str, level: str, area: str, language: str) -> str:
    if match := re.fullmatch(r"#ex(\d{3,4})--worked-result", href, re.I):
        return f"#answer-ex{match.group(1)}"
    if href.startswith("#") and not re.fullmatch(r"#(?:ch|lesson)-\d{2,4}|#week-\d{2,4}-day-\d{2}", href):
        return href
    resolved = urlparse(urljoin(source_url, href))
    if resolved.hostname != "github.com":
        return href if href.startswith("#") else resolved.geturl()
    match = re.fullmatch(rf"/{REPOSITORY}/blob/main/(.+)", resolved.path)
    if not match:
        return resolved.geturl()
    path = match.group(1)
    book = re.fullmatch(r"levels/([^/]+)/([^/]+)/([a-z]{2})/book/MANUSCRIPT\.md", path)
    if book:
        target_level, target_area, target_lang = book.groups()
        fragment = resolved.fragment
        daily = re.fullmatch(r"lesson-(\d{2,4})", fragment)
        weekday = re.fullmatch(r"week-(\d{2,4})-day-(\d{2})", fragment)
        chapter = re.fullmatch(r"ch-(\d{2,4})", fragment)
        if daily:
            return lesson_path(target_level, target_area, target_lang, int(daily.group(1)))
        if weekday:
            number = (int(weekday.group(1)) - 1) * 5 + int(weekday.group(2))
            return lesson_path(target_level, target_area, target_lang, number)
        if chapter:
            return lesson_path(target_level, target_area, target_lang, int(chapter.group(1)), "chapter")
        return f"/book/?level={quote(target_level)}&area={quote(target_area)}&lang={quote(target_lang)}" + (f"#{quote(fragment)}" if fragment else "")
    course_doc = re.fullmatch(r"levels/([^/]+)/([^/]+)/(?:[a-z]{2}/)?(?:README|SUBJECTS)\.md", path)
    if course_doc:
        return f"/courses/{course_doc.group(1)}/{course_doc.group(2)}/"
    if path.endswith(".md"):
        return "/read/?path=" + quote(path) + (f"#{quote(resolved.fragment)}" if resolved.fragment else "")
    return resolved.geturl()


class LocalizeHTML(HTMLParser):
    def __init__(self, source_url: str, level: str, area: str, language: str):
        super().__init__(convert_charrefs=False)
        self.source_url = source_url
        self.level, self.area, self.language = level, area, language
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        parts = []
        for key, value in attrs:
            if value is None:
                parts.append(key)
                continue
            if tag == "a" and key == "href":
                value = local_link(value, self.source_url, self.level, self.area, self.language)
            if tag == "img" and key == "src":
                resolved = urlparse(urljoin(self.source_url, value))
                prefix = f"/{REPOSITORY}/blob/main/"
                value = (f"https://raw.githubusercontent.com/{REPOSITORY}/main/" + resolved.path[len(prefix):]) if resolved.hostname == "github.com" and resolved.path.startswith(prefix) else resolved.geturl()
            parts.append(f'{key}="{html.escape(value, quote=True)}"')
        self.parts.append("<" + tag + (" " + " ".join(parts) if parts else "") + ">")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(html.escape(data))

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")


def render_markdown(source: str, source_url: str, level: str, area: str, language: str,
                    *, exercise_anchors: bool = True) -> str:
    for digits in (set(re.findall(r'^[ \t]*(?:#{3,6}[ \t]+|[-*][ \t]+)?(?:\*\*)?EX(\d{3,4})\b', source, re.M))
                   if exercise_anchors else set()):
        if f'id="exercise-ex{digits}"' not in source:
            bullet = rf'^([ \t]*[-*][ \t]+)((?:\*\*)?EX{digits}\b)'
            if re.search(bullet, source, re.M):
                source = re.sub(bullet, rf'\1<a id="exercise-ex{digits}"></a> \2', source, count=1, flags=re.M)
            else:
                source = re.sub(rf'^([ \t]*(?:#{{3,6}}[ \t]+)?(?:\*\*)?EX{digits}\b)',
                                f'<a id="exercise-ex{digits}"></a>\n\\1', source, count=1, flags=re.M)
    rendered = markdown.markdown(source, extensions=["fenced_code", "tables", "sane_lists"])
    sanitized = bleach.clean(rendered, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, protocols=["http", "https", "mailto"], strip=True)
    ui = PAGE_TEXT.get(language, PAGE_TEXT["en"])
    # The manuscript keeps full grading rubrics. On the study page they must not
    # give away the answer before a learner has attempted the exercise.
    rubric = re.compile(r'(<li>(?:(?!</li>).)*?)(<em>(?:Rubrica|Rúbrica|Rubric):</em>.*?)(</li>)', re.I | re.S)
    sanitized = rubric.sub(
        lambda match: match.group(1) + '<details class="rubric"><summary>'
        + html.escape(ui["criteria"]) + '</summary><div>' + match.group(2)
        + '</div></details>' + match.group(3), sanitized,
    )
    sanitized = re.sub(
        r'(<table(?:\s[^>]*)?>.*?</table>)',
        lambda match: '<p class="table-hint">' + html.escape(ui["table"]) + ' →</p>'
        + '<div class="table-scroll" role="region" tabindex="0" aria-label="'
        + html.escape(ui["table"], quote=True) + '">' + match.group(1) + '</div>',
        sanitized, flags=re.S,
    )
    parser = LocalizeHTML(source_url, level, area, language)
    parser.feed(sanitized)
    return "".join(parser.parts)


def json_script(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def render_course_sidebar(guide: dict, level: str, area: str, language: str, number: int, kind: str,
                          course_code: str) -> str:
    """Publish actual lesson links in HTML so navigation works without JavaScript."""
    ui = STUDY_TEXT.get(language, STUDY_TEXT["en"])
    daily = [] if guide["chapter_lessons"] else [unit for unit in guide["daily_slots"] if unit["published"]]
    chapters = [unit for unit in guide["legacy_chapters"] if unit["published"]]
    sections = []
    for route_kind, units, title, letter in (
        ("lesson", daily, ui["published"], "A"),
        ("chapter", chapters, ui["published"] if guide["chapter_lessons"] else ui["chapters"],
         "A" if guide["chapter_lessons"] else "C"),
    ):
        if not units:
            continue
        entries = []
        last_module = None
        for unit in units:
            index = int(unit["chapter"])
            module = unit.get("module")
            if route_kind == "lesson" and module and module != last_module:
                entries.append(f'<li class="course-week">{html.escape(ui["week"])} {module}</li>')
                last_module = module
            current = index == number and route_kind == ("lesson" if kind == "lesson" else "chapter")
            href = lesson_path(level, area, language, index, route_kind)
            current_attr = ' aria-current="page"' if current else ""
            entries.append(
                f'<li><a href="{href}"{current_attr}><span class="course-unit-code">'
                f'{course_code}-{letter}{index:03d}</span><span>{html.escape(unit["title"])}</span></a></li>'
            )
        sections.append(f'<h3>{html.escape(title)}</h3><ol>{"".join(entries)}</ol>')
    return ''.join(sections)


def render_lesson_page(lesson: dict, course: dict, level_name: str, kind: str = "lesson",
                       guide: dict | None = None, available_test_chapters: set[int] | None = None) -> str:
    level, area, language = (lesson["course"][key] for key in ("level", "area", "language"))
    number = lesson["chapter"]
    ui = PAGE_TEXT.get(language, PAGE_TEXT["en"])
    chrome = PAGE_CHROME.get(language, PAGE_CHROME["en"])
    label = ui["lesson" if kind in {"lesson", "chapter_lesson"} else "chapter"]
    course_code = f'OCA-{int(course["number"]):03d}'
    unit_letter = "A" if kind in {"lesson", "chapter_lesson"} else "C"
    unit_code = f"{course_code}-{unit_letter}{number:03d}"
    path = lesson_path(level, area, language, number, kind)
    markdown_path = lesson.get("markdown_url") or path.rstrip("/") + ".md"
    locale_site = site_for_language(language)
    canonical = locale_site + path
    course_url = locale_site + f"/courses/{level}/{area}/"
    name = course.get("titles", {}).get(language, course["title"])
    title = f"{lesson['title']} | {level_name} {name} | OpenCyber Academy"
    fallback_description = {
        "en": f"Study {lesson['title']} in the free {name} course. Read the lesson, solve exercises and compare worked answers.",
        "pt": f"Estude {lesson['title']} no curso gratuito de {name}. Leia a aula, resolva os exercícios e confira as respostas comentadas.",
        "es": f"Estudia {lesson['title']} en el curso gratuito de {name}. Lee la lección, resuelve los ejercicios y consulta las respuestas desarrolladas.",
    }
    excerpt = plain_description(lesson["markdown"], fallback_description.get(language, fallback_description["en"]))
    description = f"{unit_code} · {lesson['title']}. {excerpt}"[:160].rstrip(" .,;:")
    escaped = {key: html.escape(value, quote=True) for key, value in {"canonical": canonical, "course_url": course_url, "title": title, "description": description, "name": name, "level_name": level_name, "lesson_title": lesson["title"]}.items()}
    structured = [
        {"@context": "https://schema.org", "@type": "LearningResource", "name": lesson["title"], "identifier": unit_code, "description": description, "url": canonical,
         "mainEntityOfPage": canonical, "inLanguage": language, "learningResourceType": label, "educationalLevel": level_name,
         "isAccessibleForFree": True, "provider": {"@type": "Organization", "name": "OpenCyber Academy", "url": SITE},
         "isPartOf": {"@type": "Course", "name": name, "courseCode": course_code, "url": course_url, "inLanguage": language, "isAccessibleForFree": True}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "OpenCyber Academy", "item": locale_site + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": course_url},
            {"@type": "ListItem", "position": 3, "name": lesson["title"], "item": canonical},
        ]},
    ]
    def direction_text(direction: str) -> str:
        if language == "pt":
            return f'{label} anterior' if direction == "previous" else f'{"Próxima" if unit_letter == "A" else "Próximo"} {label.lower()}'
        if language == "es":
            return f'{label} {"anterior" if direction == "previous" else "siguiente"}'
        return f'{ui[direction]} {label.lower()}'
    previous = (f'<a href="{lesson_path(level, area, language, lesson["previous"], kind)}">'
                f'<small>{course_code}-{unit_letter}{lesson["previous"]:03d}</small><span>← {direction_text("previous")}</span></a>') if lesson["previous"] else "<span></span>"
    following = (f'<a href="{lesson_path(level, area, language, lesson["next"], kind)}">'
                 f'<small>{course_code}-{unit_letter}{lesson["next"]:03d}</small><span>{direction_text("next")} →</span></a>') if lesson["next"] else "<span></span>"
    previous_link = (f'<link rel="prev" href="{locale_site + lesson_path(level, area, language, lesson["previous"], kind)}">'
                     if lesson["previous"] else "")
    next_link = (f'<link rel="next" href="{locale_site + lesson_path(level, area, language, lesson["next"], kind)}">'
                 if lesson["next"] else "")
    study = STUDY_TEXT.get(language, STUDY_TEXT["en"])
    course_navigation = render_course_sidebar(guide, level, area, language, number, kind, course_code) if guide else ""
    sign_in_url = f"/account/?next={quote(path, safe='')}"
    test_chapter = lesson.get("week_chapter") if kind == "lesson" else number
    test_chapter = test_chapter or number
    test_url = (f"/tests/?lang={quote(language)}&amp;area={quote(area)}&amp;level={quote(level)}"
                f"&amp;chapter={test_chapter}")
    test_action = (f'<a href="{test_url}">{html.escape(study["tests"])} →</a>'
                   if test_chapter in (available_test_chapters or set())
                   else f'<p class="muted">{html.escape(study["tests_unavailable"])}</p>')
    can_mark = kind in {"lesson", "chapter_lesson"} or not (guide and guide["has_daily_lessons"])
    mark_button = f'<button id="mark-lesson-complete" type="button" hidden>{html.escape(study["mark"])}</button>' if can_mark else ""
    body_source = lesson["markdown"]
    # The book's navigation block is for Markdown readers. This page has its
    # own persistent previous/guide/next navigation above and below the text.
    body_source = re.sub(
        r'<!-- open-cyber-academy:(chapter|lesson)-navigation:start[^\n]*-->.*?'
        r'<!-- open-cyber-academy:\1-navigation:end -->',
        '', body_source, flags=re.S,
    )
    first_heading = re.match(r'\A\s*(?:<a\s+id="(?:ch|lesson)-\d{2,4}"></a>\s*)?#{1,4}\s+([^\n]+)\n', body_source)
    if first_heading:
        def heading_subject(value: str) -> str:
            return re.sub(r'^(?:Chapter|Capítulo|Lesson|Aula|Lección)\s+\d+\s*[—-]\s*', '', value.strip(), flags=re.I).casefold()
        if heading_subject(first_heading.group(1)) == heading_subject(lesson["title"]):
            body_source = body_source[first_heading.end():]
    body = render_markdown(body_source, lesson["source_url"], level, area, language)
    answers = render_markdown(lesson["worked_answers"], lesson["source_url"], level, area, language,
                              exercise_anchors=False) if lesson["worked_answers"] else ""
    answers_html = f'<section class="answers"><details><summary>{ui["answers"]}</summary><div class="prose">{answers}</div></details></section>' if answers else ""
    practice_copy = {
        "en": ("Practice the exercises", "Open the prompt", "Compare with the worked answer", "Checking for a reviewed five-choice question…"),
        "pt": ("Pratique os exercícios", "Ver o enunciado", "Comparar com a resposta comentada", "Verificando se há uma questão revisada com cinco alternativas…"),
        "es": ("Practica los ejercicios", "Ver el enunciado", "Comparar con la respuesta desarrollada", "Buscando una pregunta revisada con cinco opciones…"),
    }.get(language, ("Practice the exercises", "Open the prompt", "Compare with the worked answer", "Checking for a reviewed five-choice question…"))
    usage_copy = {
        "en": ("Public activity", "Page views", "Reading sessions", "Exercise opens", "Opens in 30 days", "Counts reflect browsers that allowed analytics. A reading session requires 30 seconds on a visible page. Browsers are not people.", "Participating browsers", "browsers"),
        "pt": ("Atividade pública", "Visualizações", "Sessões de leitura", "Exercícios abertos", "Aberturas em 30 dias", "Contagens incluem navegadores que permitiram análise de uso. Uma sessão de leitura exige 30 segundos com a página visível. Navegadores não equivalem a pessoas.", "Navegadores participantes", "navegadores"),
        "es": ("Actividad pública", "Visualizaciones", "Sesiones de lectura", "Ejercicios abiertos", "Aperturas en 30 días", "Los recuentos incluyen navegadores que permitieron el análisis de uso. Una sesión de lectura exige 30 segundos con la página visible. Los navegadores no equivalen a personas.", "Navegadores participantes", "navegadores"),
    }.get(language, ("Public activity", "Page views", "Reading sessions", "Exercise opens", "Opens in 30 days", "Counts reflect browsers that allowed analytics. A reading session requires 30 seconds on a visible page. Browsers are not people.", "Participating browsers", "browsers"))
    practice_intro = {
        "en": "Open a prompt, write your response, then compare it with the worked answer. Five-choice practice appears where a reviewed question is available.",
        "pt": "Leia o enunciado, escreva sua resposta e compare com a resolução. Questões de cinco alternativas aparecem onde já há revisão.",
        "es": "Lee el enunciado, escribe tu respuesta y compárala con la solución. Las preguntas de cinco opciones aparecen donde ya fueron revisadas.",
    }.get(language, "Open a prompt, write your response, then compare it with the worked answer. Five-choice practice appears where a reviewed question is available.")
    practice_cards = []
    for digits in lesson.get("exercise_ids", []):
        exercise_id = f"EX{digits}"
        prompt_link = (f'<a href="#exercise-ex{digits}">{html.escape(practice_copy[1])} →</a>'
                       if f'id="exercise-ex{digits}"' in body else "")
        answer_link = (f'<a href="#answer-ex{digits}">{html.escape(practice_copy[2])} →</a>'
                       if f'id="answer-ex{digits}"' in answers else "")
        practice_cards.append(
            f'<section class="exercise-attempt" data-exercise-id="{exercise_id}">'
            f'<h3>{exercise_id}</h3><div class="exercise-links">{prompt_link}{answer_link}</div>'
            f'<small class="exercise-public-count">{html.escape(usage_copy[4])}: <strong data-exercise-insight="{exercise_id}">—</strong> · {html.escape(usage_copy[7])}: <strong data-exercise-browsers="{exercise_id}">—</strong></small>'
            f'<div class="exercise-choice-options"></div>'
            f'<p class="exercise-attempt-status" role="status">{html.escape(practice_copy[3])}</p></section>'
        )
    practice_html = (f'<section id="lesson-practice" class="lesson-practice" aria-label="{html.escape(practice_copy[0], quote=True)}">'
                     f'<h2>{html.escape(practice_copy[0])}</h2><p class="practice-intro">{html.escape(practice_intro)}</p>{"".join(practice_cards)}</section>') if practice_cards else ""
    diagram_script = '<script src="/seo-diagrams.js" defer></script>' if 'class="language-mermaid"' in body or 'class="language-mermaid"' in answers else ''
    language_name = html.escape(LANGUAGE_NAMES.get(language, language))
    share_copy = {
        "en": ("Share this lesson", "Permanent link", "Link copied", "Copy the permanent link"),
        "pt": ("Compartilhar esta aula", "Link permanente", "Link copiado", "Copie o link permanente"),
        "es": ("Compartir esta lección", "Enlace permanente", "Enlace copiado", "Copia el enlace permanente"),
    }.get(language, ("Share this lesson", "Permanent link", "Link copied", "Copy the permanent link"))
    return f'''<!doctype html>
<html lang="{html.escape(language)}" dir="{'rtl' if language == 'he' else 'ltr'}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped['title']}</title><meta name="description" content="{escaped['description']}"><meta name="author" content="OpenCyber Academy">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#070e1c"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="canonical" href="{escaped['canonical']}">
  {previous_link}{next_link}
  <link rel="alternate" type="text/markdown" href="{html.escape(markdown_path, quote=True)}" title="{unit_code} Markdown">
  <meta property="og:type" content="article"><meta property="og:site_name" content="OpenCyber Academy">
  <meta property="og:title" content="{escaped['title']}"><meta property="og:description" content="{escaped['description']}">
  <meta property="og:url" content="{escaped['canonical']}"><meta property="og:image" content="{SITE}/social-card.png">
  <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="OpenCyber Academy — free cybersecurity education">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escaped['title']}">
  <meta name="twitter:description" content="{escaped['description']}"><meta name="twitter:image" content="{SITE}/social-card.png">
  <script type="application/ld+json">{json_script(structured)}</script>
  <link rel="stylesheet" href="/seo-lesson.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('open-cyber-academy-theme')||'dark'}}catch(_){{document.documentElement.dataset.theme='dark'}}</script>
  <script src="/seo-lesson.js" defer></script>{diagram_script}<script src="/analytics.js" defer></script><script src="/insights.js" defer></script>
</head>
<body><a class="skip" href="#lesson-content">{chrome['skip']}</a>
<header class="header"><div class="shell header-row"><a class="brand" href="/"><img src="/favicon.svg" alt="" width="28" height="28">OpenCyber Academy</a><nav aria-label="{chrome['navigation']}"><a href="/levels/">{chrome['levels']}</a><a href="/subjects/">{chrome['subjects']}</a><a href="/tests/">{study['tests']}</a><a href="/tabletop/">TableTop</a><a href="/account/">{study['dashboard']}</a><button id="theme-toggle" type="button" aria-label="{chrome['theme']}">◐</button></nav></div></header>
<main id="lesson-content" class="shell">
  <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">{ui['home']}</a><span>›</span><a href="{escaped['course_url']}">{escaped['name']}</a><span>›</span><span>{label} {number}</span></nav>
  <div class="eyebrow">{escaped['level_name']} · {label} {number} · {language_name}</div>
  <div class="unit-identity"><span>{ui['course_code']}: <strong>{course_code}</strong></span><span>{label} {number:02d}: <strong>{unit_code}</strong></span></div>
  <h1 id="{'lesson' if kind == 'lesson' else 'ch'}-{number:02d}">{escaped['lesson_title']}</h1>
  <p class="intro">{ui['free']}</p>
  <div class="lesson-share"><button id="share-lesson" type="button" data-url="{escaped['canonical']}" data-title="{escaped['title']}" data-copied="{html.escape(share_copy[2], quote=True)}" data-copy-hint="{html.escape(share_copy[3], quote=True)}">{html.escape(share_copy[0])}</button><a href="{escaped['canonical']}">{html.escape(share_copy[1])}</a><span id="share-status" role="status" aria-live="polite"></span></div>
  <section class="reader-public-usage" aria-label="{html.escape(usage_copy[0], quote=True)}">
    <h2>{html.escape(usage_copy[0])} · 30d</h2>
    <div class="reader-usage-metrics">
      <p><strong data-insight="page.browsers">—</strong><span>{html.escape(usage_copy[6])}</span></p>
      <p><strong data-insight="page.views">—</strong><span>{html.escape(usage_copy[1])}</span></p>
      <p><strong data-insight="page.reads">—</strong><span>{html.escape(usage_copy[2])}</span></p>
      <p><strong data-insight="page.exercises">—</strong><span>{html.escape(usage_copy[3])}</span></p>
    </div>
    <small>{html.escape(usage_copy[5])}</small><small data-insight-status role="status"></small>
  </section>
  <nav class="lesson-nav" aria-label="{chrome['lesson_navigation']}">{previous}<a href="{escaped['course_url']}">{ui['guide']}</a>{following}</nav>
  <div class="lesson-layout">
  <div class="lesson-main">
  <article class="prose" lang="{html.escape(language)}">{body}</article>
  {practice_html}
  {answers_html}
  <nav class="lesson-nav" aria-label="{chrome['next_step']}">{previous}<a href="{escaped['course_url']}">{ui['all']}</a>{following}</nav>
  </div>
  <aside class="course-sidebar" aria-label="{html.escape(study['published'], quote=True)}"><div class="sidebar-inner">
    <h2>{html.escape(ui['guide'])}</h2><a class="course-home-link" href="{escaped['course_url']}">{escaped['name']}</a>
    <nav aria-label="{html.escape(study['published'], quote=True)}">{course_navigation}</nav>
  </div></aside>
  <aside class="progress-sidebar" aria-label="{html.escape(study['progress'], quote=True)}"
         data-level="{html.escape(level, quote=True)}" data-area="{html.escape(area, quote=True)}"
         data-language="{html.escape(language, quote=True)}" data-chapter="{number}"
         data-published="{len([unit for unit in guide['daily_slots'] if unit['published']]) if guide and not guide['chapter_lessons'] else len([unit for unit in guide['legacy_chapters'] if unit['published']]) if guide else 0}">
    <div class="sidebar-inner"><h2>{html.escape(study['progress'])}</h2>
      <p id="progress-status">{html.escape(study['loading'])}</p>
      <div id="progress-metrics" hidden>
        <p><strong id="progress-completed">0</strong> {html.escape(study['completed'])}</p>
        <p><strong id="progress-exercises">0</strong> {html.escape(study['exercises'])}</p>
        <p><strong id="progress-correct">0/0</strong> {html.escape(study['correct'])}</p>
      </div>
      {mark_button}
      <a id="progress-signin" href="{sign_in_url}" hidden>{html.escape(study['sign_in'])} →</a>
      <a id="progress-dashboard" href="/account/" hidden>{html.escape(study['dashboard'])} →</a>
      {test_action}
    </div>
  </aside>
  </div>
</main>
<footer class="footer"><div class="shell">© OpenCyber Academy · {chrome['footer']} · <a href="/for-ai/">{chrome['api']}</a></div></footer>
</body></html>'''


def render_planned_lesson_page(course: dict, slot: dict, language: str,
                               level_name: str, published_chapter: dict | None) -> str:
    """A navigable study slot, explicitly excluded from search until teaching exists."""
    level, area = course["level"], course["area"]
    number, week = slot["chapter"], slot["module"]
    ui = PAGE_TEXT.get(language, PAGE_TEXT["en"])
    chrome = PAGE_CHROME.get(language, PAGE_CHROME["en"])
    course_code = f'OCA-{int(course["number"]):03d}'
    unit_code = f'{course_code}-A{number:03d}'
    site = site_for_language(language)
    path = lesson_path(level, area, language, number)
    title = html.escape(slot["title"])
    name = html.escape(course.get("titles", {}).get(language, course["title"]))
    course_path = f"/courses/{level}/{area}/"
    messages = {
        "en": ("Planned study day", "This lesson's teaching, example and exercise have not been published yet.", "The course guide records its place in the curriculum. Read a published chapter while the daily lesson is being written.", "Read the published chapter"),
        "pt": ("Dia de estudo planejado", "O conteúdo, o exemplo e o exercício desta aula ainda não foram publicados.", "O guia do curso mostra sua posição no currículo. Leia um capítulo publicado enquanto esta aula é escrita.", "Ler o capítulo publicado"),
        "es": ("Día de estudio planificado", "La explicación, el ejemplo y el ejercicio de esta lección aún no se han publicado.", "La guía del curso indica su lugar en el programa. Lee un capítulo publicado mientras se redacta esta lección.", "Leer el capítulo publicado"),
    }
    label, notice, guidance, chapter_label = messages.get(language, messages["en"])
    chapter_link = (f'<p><a href="{lesson_path(level, area, language, published_chapter["chapter"], "chapter")}">'
                    f'{html.escape(chapter_label)}: {html.escape(published_chapter["title"])}</a></p>') if published_chapter else ""
    previous = f'<a href="{lesson_path(level, area, language, number - 1)}"><small>{course_code}-A{number - 1:03d}</small><span>← {ui["previous"]}</span></a>' if number > 1 else "<span></span>"
    following = f'<a href="{lesson_path(level, area, language, number + 1)}"><small>{course_code}-A{number + 1:03d}</small><span>{ui["next"]} →</span></a>' if number < course["daily_lesson_target"] else "<span></span>"
    return f'''<!doctype html>
<html lang="{html.escape(language)}" dir="{'rtl' if language == 'he' else 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{number}. {title} | {name} | OpenCyber Academy</title>
<meta name="robots" content="noindex,follow"><meta name="description" content="{html.escape(notice)}">
<link rel="canonical" href="{site}{path}"><link rel="stylesheet" href="/seo-lesson.css">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
</head><body><header class="header"><div class="shell header-row"><a class="brand" href="/"><img src="/favicon.svg" alt="" width="28" height="28">OpenCyber Academy</a></div></header>
<main class="shell"><nav class="breadcrumbs"><a href="/">{ui['home']}</a><span>›</span><a href="{course_path}">{name}</a></nav>
<div class="eyebrow">{html.escape(level_name)} · {html.escape(label)} {number} · {html.escape(language.upper())}</div>
<div class="unit-identity"><span>{ui['course_code']}: <strong>{course_code}</strong></span><span>{ui['lesson']} {number:02d}: <strong>{unit_code}</strong></span></div>
<h1>{title}</h1><p class="intro">{html.escape(notice)}</p>
<article class="prose"><p>{html.escape(guidance)}</p><p>{html.escape(label)} {number} · {ui['chapter']} {week} · {name}.</p>{chapter_link}</article>
<nav class="lesson-nav" aria-label="{chrome['lesson_navigation']}">{previous}<a href="{course_path}">{ui['guide']}</a>{following}</nav>
</main><footer class="footer"><div class="shell">© OpenCyber Academy · {html.escape(ui['free'])}</div></footer>
</body></html>'''
