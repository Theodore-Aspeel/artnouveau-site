"""Build an offline, untracked photographic review from a private JSON manifest.

Usage: python scripts/build-private-review.py .private-media/d1/site.json
The output stays beside the manifest; this script never writes to src/ or dist/.
"""
import html
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest_path = pathlib.Path(sys.argv[1]).resolve()
private_root = (ROOT / '.private-media').resolve()
if not manifest_path.is_relative_to(private_root):
    raise SystemExit('Private manifest must be under .private-media')
data = json.loads(manifest_path.read_text(encoding='utf-8'))
out = manifest_path.parent / 'site'
if out.exists():
    shutil.rmtree(out)
(out / 'images').mkdir(parents=True)
E = lambda x: html.escape(str(x), quote=True)
langs = ('en', 'fr', 'nl')
labels = {
    'en': ('Buildings', 'Places', 'Photographic dossier', 'Explore the images', 'Next places', 'Photographs by', 'About & contact', 'Private review · Do not publish', 'Photograph', 'Previous', 'Next', 'Close', 'Back to the journal'),
    'fr': ('Bâtiments', 'Lieux', 'Dossier photographique', 'Explorer les images', 'Poursuivre la visite', 'Photographies de', 'À propos et contact', 'Revue privée · Ne pas publier', 'Photographie', 'Précédent', 'Suivant', 'Fermer', 'Retour au journal'),
    'nl': ('Gebouwen', 'Plaatsen', 'Fotografisch dossier', 'Bekijk de foto’s', 'Verder kijken', 'Foto’s van', 'Over ons en contact', 'Privépreview · Niet publiceren', 'Foto', 'Vorige', 'Volgende', 'Sluiten', 'Terug naar het overzicht'),
}
for image in data['images']:
    source = pathlib.Path(image['source']).resolve()
    if not source.is_relative_to(private_root) and not source.is_relative_to(ROOT / 'src' / 'assets'):
        raise SystemExit(f'Image outside approved local roots: {source}')
    shutil.copyfile(source, out / 'images' / image['name'])

def link(slug, lang):
    return f'{slug}-{lang}.html'

def picture(image, lang, kind='single'):
    copy = image['text'][lang]
    return (f'<figure class="photo photo--{kind}"><button class="photo__open" type="button" data-open>'
            f'<img src="images/{E(image["name"])}" alt="{E(copy["alt"])}" loading="lazy" decoding="async"></button>'
            f'<figcaption><span>{E(copy["caption"])}</span><small>© Christophe Aspel</small></figcaption></figure>')

def chrome(lang, title, active):
    L = labels[lang]
    langs_html = ''.join(f'<a href="{E(link(active, lng))}" lang="{lng}" aria-current="{str(lng == lang).lower()}">{lng.upper()}</a>' for lng in langs)
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex,nofollow"><title>{E(title)} · ANAD private review</title><link rel="stylesheet" href="review.css"></head>'
            f'<body><p class="private-banner">{L[7]}</p><header class="top"><a class="brand" href="{link("index",lang)}"><b>ANAD</b><span>Art Nouveau et Art Déco</span></a>'
            f'<nav><a href="{link("index",lang)}#buildings">{L[0]}</a><a href="{link("index",lang)}#places">{L[1]}</a><a href="{link("about",lang)}">{L[6]}</a></nav><div class="languages">{langs_html}</div></header>')

def footer(lang):
    return f'<footer><strong>ANAD</strong><p>{labels[lang][5]} Christophe Aspel</p><a href="{link("about",lang)}">{labels[lang][6]} ↗</a></footer><script src="review.js"></script></body></html>'

images = {i['name']: i for i in data['images']}
for lang in langs:
    L = labels[lang]
    lead = data['articles'][0]
    leadimg = images[lead['media'][0]]
    items = []
    for j, article in enumerate(data['articles']):
        t = article['text'][lang]
        img = images[article['media'][0]]
        items.append(f'<article class="story"><a class="story__image" href="{link(article["slug"],lang)}"><img src="images/{E(img["name"])}" alt="{E(img["text"][lang]["alt"])}" loading="lazy"></a><div><p class="eyebrow">{E(article["place"][lang])} · {j+1:02d}</p><h2><a href="{link(article["slug"],lang)}">{E(t["title"])}</a></h2><p>{E(t["intro"])}</p><a class="action" href="{link(article["slug"],lang)}">{L[2]} ↗</a></div></article>')
    home = chrome(lang,'ANAD', 'index') + f'<main><section class="home-hero"><a href="{link(lead["slug"],lang)}"><img src="images/{E(leadimg["name"])}" alt="{E(leadimg["text"][lang]["alt"])}"></a><div><p class="eyebrow">{E(lead["place"][lang])} · 01</p><h1>{E(lead["text"][lang]["title"])}</h1><p>{E(lead["text"][lang]["intro"])}</p><a class="action" href="{link(lead["slug"],lang)}">{L[2]} ↗</a></div></section><section class="journal" id="buildings"><div class="section-head"><p class="eyebrow">ANAD / Christophe Aspel</p><h2>{L[0]}</h2></div>{"".join(items[1:])}</section><section class="places" id="places"><h2>{L[1]}</h2><div>'
    for city, slug in data['places']:
        home += f'<a href="{link(slug,lang)}">{E(city)} ↗</a>'
    home += f'</div></section><section class="author"><p class="eyebrow">{L[5]}</p><h2>Christophe Aspel</h2><a class="action" href="{link("about",lang)}">{L[6]} ↗</a></section></main>' + footer(lang)
    (out / link('index',lang)).write_text(home, encoding='utf-8')
    for article in data['articles']:
        t = article['text'][lang]
        sequence = article['media']
        hero = picture(images[sequence[0]],lang,'hero')
        chunks = [f'<section class="prose"><p>{E(t["paragraphs"][0])}</p></section>']
        for idx, name in enumerate(sequence[1:]):
            kind = 'wide' if idx % 3 == 0 else ('detail' if idx % 3 == 1 else 'single')
            chunks.append(picture(images[name],lang,kind))
            if idx+1 < len(t['paragraphs']):
                chunks.append(f'<section class="prose"><p>{E(t["paragraphs"][idx+1])}</p></section>')
        for para in t['paragraphs'][len(sequence):]:
            chunks.append(f'<section class="prose"><p>{E(para)}</p></section>')
        related = ''.join(f'<a href="{link(other["slug"],lang)}">{E(other["text"][lang]["title"])} <span>{E(other["place"][lang])}</span> ↗</a>' for other in data['articles'] if other != article)[:10000]
        page = chrome(lang,t['title'],article['slug']) + f'<main class="article"><div class="article-heading"><a class="back" href="{link("index",lang)}">← {L[12]}</a><p class="eyebrow">{E(article["place"][lang])} · {L[2]}</p><h1>{E(t["title"])}</h1><p class="intro">{E(t["intro"])}</p></div>{hero}<div class="article-sequence">{"".join(chunks)}</div><div class="documentary"><h2>{L[3]}</h2><p>{L[8]} · © Christophe Aspel</p><div class="thumbs">{"".join(picture(images[n],lang,"thumb") for n in sequence)}</div></div><section class="related"><h2>{L[4]}</h2><div>{related}</div><a class="action" href="{link("about",lang)}">{L[5]} Christophe Aspel ↗</a></section></main><div class="lightbox" role="dialog" aria-modal="true" aria-label="{L[3]}" hidden><button class="lightbox__close" type="button" data-close aria-label="{L[11]}">×</button><button type="button" data-prev aria-label="{L[9]}">←</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" data-next aria-label="{L[10]}">→</button></div>' + footer(lang)
        (out / link(article['slug'],lang)).write_text(page,encoding='utf-8')
    about = chrome(lang, 'Christophe Aspel', 'about') + f'<main class="about"><a class="back" href="{link("index",lang)}">← {L[12]}</a><p class="eyebrow">{L[5]}</p><h1>Christophe Aspel</h1><p>Art Nouveau et Art Déco · {L[5]} Christophe Aspel.</p><p><a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener">@artnouveauetdeco ↗</a></p><p><a href="{link("index",lang)}">{L[0]} ↗</a></p></main>' + footer(lang)
    (out / link('about',lang)).write_text(about,encoding='utf-8')
(out / 'index.html').write_text('<meta http-equiv="refresh" content="0;url=index-en.html"><a href="index-en.html">Open ANAD private review</a>',encoding='utf-8')
shutil.copyfile(ROOT / 'scripts' / 'private-review.css',out / 'review.css')
shutil.copyfile(ROOT / 'scripts' / 'private-review.js',out / 'review.js')
print(f'Private offline review: {out / "index.html"}')
