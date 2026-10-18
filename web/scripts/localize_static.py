#!/usr/bin/env python3
"""Build server-visible PT/ES HTML without changing source pages or manuscripts."""

from __future__ import annotations

import html
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
TRANSLATIONS = json.loads(subprocess.check_output(["node", "scripts/export_translations.mjs"], cwd=ROOT))
LOCALES = {"pt": 0, "es": 1}
NATIVE_LANDING = {
    "he": ("עברית", "לימודי אבטחת סייבר פתוחים", "ספרי הקורסים בשפה זו עדיין בהכנה. אפשר ללמוד כעת באנגלית, בפורטוגזית או בספרדית."),
    "fr": ("Français", "Une formation ouverte en cybersécurité", "Les livres de cours dans cette langue sont en préparation. Consultez les éditions disponibles en anglais, portugais et espagnol."),
    "ru": ("Русский", "Открытое обучение кибербезопасности", "Учебники на этом языке пока готовятся. Сейчас доступны материалы на английском, португальском и испанском языках."),
    "de": ("Deutsch", "Offene Bildung in Cybersicherheit", "Die Kursbücher in dieser Sprache werden vorbereitet. Lesen Sie die verfügbaren Ausgaben auf Englisch, Portugiesisch oder Spanisch."),
    "zh": ("中文", "开放的网络安全教育", "该语言的课程教材仍在编写中。目前可阅读英语、葡萄牙语和西班牙语版本。"),
    "ja": ("日本語", "誰でも学べるサイバーセキュリティ", "この言語の教材は現在準備中です。英語、ポルトガル語、スペイン語の公開版をご利用ください。"),
}


class Localizer(HTMLParser):
    def __init__(self, language: str):
        super().__init__(convert_charrefs=False)
        self.language = language
        self.blocked = 0
        self.parts: list[str] = []

    def handle_decl(self, decl: str) -> None:
        self.parts.append(f"<!{decl}>")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self.get_starttag_text())
        if tag in {"script", "style", "pre", "code"}:
            self.blocked += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "pre", "code"}:
            self.blocked -= 1
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        pair = TRANSLATIONS.get(stripped)
        if not self.blocked and pair:
            data = data.replace(stripped, html.escape(pair[LOCALES[self.language]], quote=False))
        self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")


def localized_page(source: str, language: str, route: str) -> str:
    parser = Localizer(language)
    parser.feed(source)
    result = "".join(parser.parts)
    result = result.replace('<html lang="en">', f'<html lang="{language}">', 1)
    origin = f"https://{language}.opencyber.academy"
    result = result.replace('<link rel="canonical" href="https://opencyber.academy', f'<link rel="canonical" href="{origin}', 1)
    result = result.replace('<meta property="og:url" content="https://opencyber.academy', f'<meta property="og:url" content="{origin}', 1)
    if route not in {"/", "/about/", "/share/"}:
        result = result.replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"', 1)
    metadata = {
        "/": {
            "pt": ("OpenCyber Academy — aulas gratuitas de cibersegurança", "Estude cibersegurança com aulas abertas, exemplos resolvidos, exercícios e respostas comentadas. Escolha um tema e avance sem cadastro."),
            "es": ("OpenCyber Academy — lecciones gratuitas de ciberseguridad", "Estudia ciberseguridad con lecciones abiertas, ejemplos resueltos, ejercicios y respuestas explicadas. Elige un tema y avanza sin registrarte."),
        },
        "/about/": {
            "pt": ("Sobre nós · OpenCyber Academy", "Conheça a OpenCyber Academy e seu fundador, Hiago Kin Levi. Livros e aulas gratuitos de cibersegurança para todos."),
            "es": ("Sobre nosotros · OpenCyber Academy", "Conoce OpenCyber Academy y a su fundador, Hiago Kin Levi. Libros y lecciones gratuitos de ciberseguridad para todos."),
        },
        "/share/": {
            "pt": ("Compartilhe uma aula gratuita · OpenCyber Academy", "Convide alguém para estudar uma aula publicada da OpenCyber Academy em inglês, português ou espanhol. Exemplos, exercícios e respostas comentadas, sem cadastro para ler."),
            "es": ("Comparte una lección gratuita · OpenCyber Academy", "Invita a alguien a estudiar una lección publicada de OpenCyber Academy en inglés, portugués o español. Ejemplos, ejercicios y respuestas explicadas, sin registro para leer."),
        },
        "/privacy/": {
            "pt": ("Privacidade e análise de uso opcional · OpenCyber Academy", "Estude sem cadastro e escolha se deseja permitir a medição opcional de visitas às aulas públicas."),
            "es": ("Privacidad y análisis de uso opcional · OpenCyber Academy", "Estudia sin registrarte y elige si deseas permitir la medición opcional de visitas a las lecciones públicas."),
        },
    }
    if route in metadata:
        title, description = metadata[route][language]
        result = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", result, count=1)
        for attribute in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            result = re.sub(rf'(<meta {attribute} content=")[^"]*', rf'\g<1>{html.escape(description, quote=True)}', result, count=1)
        for attribute in ('property="og:title"', 'name="twitter:title"'):
            result = re.sub(rf'(<meta {attribute} content=")[^"]*', rf'\g<1>{html.escape(title, quote=True)}', result, count=1)
        result = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',
                        lambda match: match.group(1) + match.group(2).replace('https://opencyber.academy/', origin + '/').replace('"inLanguage":"en"', f'"inLanguage":"{language}"') + match.group(3),
                        result, flags=re.S)
    return result


def main() -> None:
    pages = sorted(DIST.rglob("index.html"))
    pages = [page for page in pages if "_locales" not in page.parts]
    for page in pages:
        relative = page.relative_to(DIST)
        route = "/" if relative == Path("index.html") else "/" + relative.parent.as_posix() + "/"
        source = page.read_text(encoding="utf-8")
        for language in LOCALES:
            target = DIST / "_locales" / language / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(localized_page(source, language, route), encoding="utf-8")
    for language, (name, title, description) in NATIVE_LANDING.items():
        target = DIST / "_locales" / language / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'''<!doctype html><html lang="{language}" dir="{'rtl' if language == 'he' else 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,follow"><title>{html.escape(title)} · OpenCyber Academy</title>
<link rel="canonical" href="https://{language}.opencyber.academy/"><link rel="stylesheet" href="/seo-lesson.css">
</head><body><header class="header"><div class="shell header-row"><a class="brand" href="/">◇ OpenCyber Academy</a></div></header>
<main class="shell"><div class="eyebrow">{html.escape(name)} · OpenCyber Academy</div><h1>{html.escape(title)}</h1>
<p class="intro">{html.escape(description)}</p><nav class="lesson-nav"><a href="https://opencyber.academy/">English</a>
<a href="https://pt.opencyber.academy/">Português</a><a href="https://es.opencyber.academy/">Español</a></nav>
<p><a href="https://opencyber.academy/tabletop/">TableTop (English)</a></p></main>
<script src="/analytics.js" defer></script>
</body></html>''', encoding="utf-8")
    print(f"Localized {len(pages)} static pages for Portuguese and Spanish; staged six additional language home pages")


if __name__ == "__main__":
    main()
