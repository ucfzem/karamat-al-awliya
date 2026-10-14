# Conversation backup — سياق كرامات الأولياء (Karamat al-Awliya)

## Summary
Création d'une **PWA offline-first** dédiée à « **سياق كرامات الأولياء** » de l'Imam
**أبو القاسم اللالكائي (ت 418 هـ)**, extrait de son *شرح أصول اعتقاد أهل السنة والجماعة*.
Design « manuscrit » (papier `#f8f6f0`, vert profond `#1b4332`, or `#d4af37`), RTL, mobile-first,
fonctionnement **100 % hors-ligne** après la première visite en ligne.

## Repo
- **Repo** : `ucfzem/karamat-al-awliya` (public)
- **Live** : https://ucfzem.github.io/karamat-al-awliya/
- **Deploy** : GitHub Pages — `main` / `/` (build legacy, `.nojekyll`)
- **Commit initial** : `7fea8b1`

## Fichiers (structure demandée, 4 fichiers + icônes)
| Fichier | Rôle |
|---------|------|
| `index.html` | App shell : recherche instantanée, filtres, partage, thème, favoris |
| `data.json` | Base des récits (`id, title, category, era, isnad, text, source_num, verified`) |
| `sw.js` | Service Worker (cache `karamat-cache-v1.0.0`, scopé `karamat-`) |
| `manifest.json` | PWA (`display: standalone`, `dir: rtl`, thème `#1b4332`) |
| `icon.svg`, `icon-192.png`, `icon-512.png` | Icône : carré vert + étoile 8 branches dorée (rub el hizb) |
| `tools/make_icons.py` | Générateur d'icônes PNG (stdlib uniquement, sans Pillow) |

## Fonctionnalités vérifiées
- **Recherche** par titre, texte, isnad, catégorie, région, **et numéro d'effet**.
- **Filtres** générés dynamiquement : *الفئة* (الصحابة / التابعون / أتباع التابعين) + *الموطن/العصر* (مكة/الشام/الكوفة/البصرة/بغداد/خراسان/اليمن…).
- **Partage / copie** d'un أثر avec référence (« كرامات الأولياء للالكائي، أثر رقم N »).
- **Thème** clair/sombre + **taille de police** (A− / A+) + **favoris** (localStorage) persistants.

## Données (transparence sur l'authenticité)
- **5 récits authentiques fournis** intégrés verbatim (`verified: true`, avec `source_num`).
- **5 entrées supplémentaires** d'épisodes connus/notoires, marquées **`verified: false`** et affichées avec le badge « بانتظار التوثيق » (`source_num: null`) — **aucune chaîne de transmission n'a été inventée**.
- **Corpus complet (250+ روايات) non inclus** : `data.json` est structuré pour l'import intégral depuis la source (Shamela). Aucun texte/isnad fabriqué.

## Offline — architecture
- First load **en ligne** → installation du SW : précache de `index.html`, `data.json`, `manifest.json`, icônes, polices Google (Amiri/Cairo/Aref Ruqaa).
- Ensuite **hors-ligne** : navigate → cache ; assets locaux → cache-first ; polices → cache puis réseau.
- Intégration au SW racine de `ucfzem.github.io` : ajout à `SHELLS` et `APPS`, `DATA_MARKER` `v4 → v5`, CDN fonts ajouté.

## Vérification (Playwright, live)
- Page /works : carte présente dans **Maktaba** (section publique/déverrouillée), `#f-maktaba` ouverte, 11 entrées, icône OK, absente de la section verrouillée.
- En ligne : SW contrôle la page, 10 cartes, recherche `سارية`→1, filtre `التابعون`→3, recherche `2235`→1, thème light↔dark, favori→1, copie avec référence OK, 0 erreur.
- Hors-ligne (reload) : 10 cartes, recherche OK, 12 puces de filtre, polices chargées, favori persistant, icônes OK, 0 erreur.

## Lien
- Tree : https://ucfzem.github.io/works/ → **Maktaba · المكتبة** → كرامات الأولياء

---

# Addendum — Corpus complet (extraction verbatim)

- **220 récits** extraits de **Shamela book 13150** (« كتاب كرامات الأولياء للالكائي », pages `id 1..318`), numérotation imprimée **1→230**, **92 chapitres**.
- **Tout `verified: true`** : texte et chaînes repris **verbatim** de la source imprimée — **aucun texte/isnad fabriqué**.
- Catégories : الصحابة 73 · التابعون 86 · أتباع التابعين 21 · القرآن والتفسير 28 · الأنبياء والأمم السابقة 12.
- Découpe isnâd/matn automatique au dernier connecteur de chaîne (`أخبرنا/حدثنا/ثنا/أنا/قال…`) avant 70 % du texte.
- Outils : `scrape13150.mjs` (scrape) + `build13150b.py` (build) ; `data.json` ≈ 434 Ko.
- SW : `karamat-cache` `v1.0.0 → v1.1.0`.
- Vérifié live (Playwright) : en ligne **220 cartes**, 19 puces, recherches `سارية`→2 · `النار`→6 · `230`→1, filtre `التابعون`→86 ; hors-ligne **220 cartes**, polices/favoris/icônes OK, 0 erreur.
- Commit : `a5d2e73`.
