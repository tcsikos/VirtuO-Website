#!/usr/bin/env python3
"""VirtuO website generator (Python 3, standard library only).

    python3 tools/build.py

Reads tools/templates/*.html (+ partials/) and i18n/<lang>.json and writes the
finished static pages:
    English  -> /index.html, /privacy.html, /support.html
    others   -> /<lang>/index.html, /<lang>/privacy.html, /<lang>/support.html
The generated HTML is committed too (GitHub Pages serves it as is).

Template syntax
    {{key}}        translated text from i18n (raw HTML allowed in the value)
    {{key|e}}      same, HTML-escaped (for attributes such as alt="")
    {{$name}}      build variable (lang, root, canonical, ...)
    {{>file}}      include tools/templates/partials/<file>
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "templates")
PARTIALS = os.path.join(TPL, "partials")
I18N = os.path.join(ROOT, "i18n")
SITE = "https://virtuo.run"
PAGES = ["index", "faq", "privacy", "support"]

# code, own-language name, short code shown in the button, og:locale
LANGS = [
    ("en", "English", "EN", "en_US"),
    ("hu", "Magyar", "HU", "hu_HU"),
    ("de", "Deutsch", "DE", "de_DE"),
    ("fr", "Français", "FR", "fr_FR"),
    ("es", "Español", "ES", "es_ES"),
    ("nb", "Norsk", "NO", "nb_NO"),
    ("sv", "Svenska", "SV", "sv_SE"),
    ("pl", "Polski", "PL", "pl_PL"),
    ("fi", "Suomi", "FI", "fi_FI"),
    ("cs", "Čeština", "CS", "cs_CZ"),
]

TOKEN = re.compile(r"\{\{\s*([>$]?)\s*([^}|\s]+)\s*(?:\|\s*(e)\s*)?\}\}")
warnings = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_lang(code, en):
    """Return (strings, untranslated_keys). Missing keys fall back to English."""
    if code == "en":
        return dict(en), []
    data = json.loads(read(os.path.join(I18N, code + ".json")))
    todo = list(data.get("_untranslated", []))
    out = dict(en)
    for k, v in data.items():
        if k.startswith("_"):
            continue
        if k not in en:
            warnings.append("%s.json: unknown key %r (not in en.json)" % (code, k))
            continue
        out[k] = v
    missing = [k for k in en if k not in data]
    for k in missing:
        if k not in todo:
            todo.append(k)
    return out, todo


def url_path(code, page):
    """Public path of a page. Index pages use the folder URL."""
    base = "/" if code == "en" else "/%s/" % code
    return base if page == "index" else base + page + ".html"


def render(text, strings, ctx):
    def sub(m):
        kind, name, flt = m.group(1), m.group(2), m.group(3)
        if kind == ">":
            return render(read(os.path.join(PARTIALS, name)).rstrip("\n"), strings, ctx)
        if kind == "$":
            if name not in ctx:
                raise KeyError("unknown variable $" + name)
            return ctx[name]
        if name not in strings:
            raise KeyError("missing translation key " + name)
        val = strings[name]
        return html.escape(val, quote=True) if flt else val
    return TOKEN.sub(sub, text)


def build_context(code, page, strings):
    name, short, locale = [(n, s, o) for c, n, s, o in LANGS if c == code][0]
    esc = lambda s: html.escape(s, quote=True)
    alts = []
    for c, _, _, _ in LANGS:
        alts.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (c, SITE, url_path(c, page)))
    alts.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, url_path("en", page)))
    items = []
    for c, n, s, _ in LANGS:
        cur = ' aria-current="true"' if c == code else ""
        items.append(
            '        <li><a href="%s" lang="%s" hreflang="%s" data-lang="%s"%s>'
            '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true" focusable="false"><use href="#flag-%s"/></svg>%s</a></li>'
            % (url_path(c, page), c, c, c, cur, c, n))
    title = strings["meta.%s.title" % page]
    desc = strings["meta.%s.description" % page]
    redirect = ""
    if code == "en":
        redirect = read(os.path.join(PARTIALS, "redirect.js")).rstrip("\n")
    return {
        "lang": code,
        "root": "" if code == "en" else "../",
        "lang_name": name,
        "lang_code": short,
        "lang_items": "\n".join(items),
        "canonical": SITE + url_path(code, page),
        "alternates": "\n".join(alts),
        "redirect": redirect,
        "title": esc(title),
        "description": esc(desc),
        "og_title": esc(strings.get("meta.%s.og_title" % page, title)),
        "og_description": esc(strings.get("meta.%s.og_description" % page, desc)),
        "og_locale": locale,
    }


def main():
    en = json.loads(read(os.path.join(I18N, "en.json")))
    count = 0
    for code, _, _, _ in LANGS:
        strings, todo = load_lang(code, en)
        outdir = ROOT if code == "en" else os.path.join(ROOT, code)
        os.makedirs(outdir, exist_ok=True)
        for page in PAGES:
            tpl = read(os.path.join(TPL, page + ".html"))
            out = render(tpl, strings, build_context(code, page, strings))
            with open(os.path.join(outdir, page + ".html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            count += 1
        if todo:
            print("  %s: %d of %d keys still need translation (fall back to English)" % (code, len(todo), len(en)))
    for w in warnings:
        print("WARNING:", w)
    print("Built %d pages in %d languages." % (count, len(LANGS)))


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        sys.exit("Build error: %s" % e)
