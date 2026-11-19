# VirtuO weboldal

A VirtuO app (virtuális tájfutó pályák iPhone-ra, Apple Watch-ra és Androidra) weboldala, 10 nyelven.
Cím: https://virtuo.run – GitHub Pages szolgálja ki a `main` ág gyökeréből (nincs build szerver).

Az app kódja: tcsikos/VirtuO (privát).

## Felépítés

| Mi | Hol |
|---|---|
| Sablonok (oldalanként egy) | `tools/templates/index.html`, `privacy.html`, `support.html` |
| Közös darabok (fejléc, CSS, nyelvválasztó, zászlók, szkriptek) | `tools/templates/partials/` |
| Fordítások, nyelvenként egy fájl | `i18n/en.json`, `hu.json`, `de.json`, `fr.json`, `es.json`, `nb.json`, `sv.json`, `pl.json`, `fi.json`, `cs.json` |
| Generátor (Python 3, csak a standard könyvtár) | `tools/build.py` |
| Kész oldalak (ezeket is commitoljuk) | angol: `/index.html`, `/privacy.html`, `/support.html`; a többi nyelv: `/<nyelv>/index.html` stb. |

A kész HTML fájlokat NE szerkeszd kézzel: a következő build felülírja őket.

## Szöveg szerkesztése

1. Nyisd meg a nyelv fájlját az `i18n/` mappában (pl. `i18n/hu.json`), és írd át az értéket a kulcs mellett.
   Az érték HTML-t is tartalmazhat (`<a>`, `<strong>`, `<br>`, listaelemek `<li>`): a címkéket és a linkeket hagyd meg.
2. Az angol (`en.json`) a forrás: új szöveghez előbb ott vegyél fel kulcsot, és tedd a sablonba `{{kulcs}}` formában.
   A kép-alt szövegeknél `{{kulcs|e}}` kell (ez escape-eli az idézőjeleket).
3. Futtasd a generátort:

```
python3 tools/build.py
```

4. Nézd meg helyben: `python3 -m http.server 8765`, majd http://localhost:8765 (a nyelvválasztó gyökér-hivatkozásokat használ, ezért a mappa gyökeréből kell kiszolgálni).
5. Commit + push (csak ha tényleg publikálni akarod).

## Hiányzó fordítások

Ha egy kulcs hiányzik egy nyelvi fájlból, a build az angol szöveget használja (és kiírja, hány kulcs hiányzik).
A még nem lefordított nyelvekben (`de, fr, es, nb, sv, pl, fi, cs`) a fájl elején egy `_untranslated` lista van:
ezeket a kulcsokat kell lefordítani. Fordítás után töröld a kulcsot a listáról. A `_` jellel kezdődő kulcsokat a build figyelmen kívül hagyja.

## Nyelvválasztás

- Csak a gyökér (angol) oldalak irányítanak át a böngésző nyelvére (kis beágyazott szkript, `tools/templates/partials/redirect.js`).
  A `/<nyelv>/` oldalakon nincs automatikus átirányítás.
- A fejlécben a nyelvválasztó a választást a böngésző `localStorage` tárába menti (`virtuo-lang-choice`), csak kattintásra.
- Minden oldalon van `canonical`, `hreflang` (mind a 10 nyelv + `x-default`) és Open Graph meta.
- Új nyelv: add hozzá a `LANGS` listához a `tools/build.py`-ban, a zászlót a `partials/flags.svg`-ben, a szkript `OK` listáját a `redirect.js`-ben, és hozz létre egy `i18n/<kód>.json` fájlt.
