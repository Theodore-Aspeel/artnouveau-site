import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const SOURCE = path.resolve(process.env.PRIVATE_PREVIEW_MEDIA_DIR || path.join(ROOT, '.private-media'));
const TARGET = path.join(DIST, 'private');
const MEDIA_TARGET = path.join(TARGET, 'media');

const FILES = [
  'blue-01-overview-19126.jpg',
  'blue-02-turret-19123.jpg',
  'blue-03-door-19122.jpg',
  'blue-04-oriel-19119.jpg',
  'blue-05-detail-19118.jpg',
  'interior-a-19136.jpg',
  'interior-b-19134.jpg',
  'interior-c-19144.jpg',
  'hall-01-interior-19157.jpg',
  'hall-02-facade-19152.jpg',
  'hall-03-detail-19148.jpg',
  'other-facade-19114.jpg',
];

async function ensurePrivateSources() {
  const missing = [];
  for (const file of FILES) {
    try {
      await fs.access(path.join(SOURCE, file));
    } catch {
      missing.push(file);
    }
  }

  if (missing.length) {
    throw new Error(`Missing private preview media in ${SOURCE}:\n- ${missing.join('\n- ')}`);
  }
}

function page({ title, current, content }) {
  const links = [
    ['index.html', 'Accueil', 'home'],
    ['portfolio.html', 'Portfolio', 'portfolio'],
    ['series-blue.html', 'Série bleue', 'series'],
  ].map(([href, label, key]) => `<a href="${href}"${current === key ? ' aria-current="page"' : ''}>${label}</a>`).join('');

  return `<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>${title} · ANAD aperçu privé</title>
  <link rel="stylesheet" href="../assets/styles/main.css">
  <style>
    :root { --private-blue: #135d78; --private-ink: #14201f; --private-paper: #f5f2eb; }
    body { margin: 0; color: var(--private-ink); background: var(--private-paper); }
    .private-banner { padding: .6rem 1rem; color: #fff; background: #7b321f; font: 600 .68rem/1.35 var(--font-ui); letter-spacing: .08em; text-align: center; text-transform: uppercase; }
    .private-nav { position: sticky; z-index: 10; top: 0; display: flex; justify-content: space-between; gap: 1rem; align-items: center; padding: .9rem clamp(1rem, 3vw, 3rem); border-bottom: 1px solid rgba(20,32,31,.2); background: rgba(250,248,243,.96); }
    .private-nav strong { font-family: var(--font-display); font-size: 1.35rem; font-weight: 400; }
    .private-nav div { display: flex; gap: 1.2rem; }
    .private-nav a { color: inherit; font: 600 .72rem/1 var(--font-ui); letter-spacing: .08em; text-decoration: none; text-transform: uppercase; }
    .private-nav a[aria-current] { color: var(--private-blue); }
    .private-hero { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(280px, .65fr); min-height: calc(100svh - 98px); }
    .private-hero figure { display: grid; place-items: center; margin: 0; background: #dce2df; }
    .private-hero img { width: 100%; height: calc(100svh - 98px); object-fit: contain; }
    .private-hero__copy { display: flex; flex-direction: column; justify-content: flex-end; padding: clamp(2rem, 5vw, 5rem) clamp(1rem, 3vw, 3rem); background: #faf8f3; }
    .private-kicker { margin: 0 0 1rem; color: var(--private-blue); font: 600 .72rem/1.2 var(--font-ui); letter-spacing: .14em; text-transform: uppercase; }
    .private-hero h1, .private-heading h1 { max-width: 8ch; margin: 0; font-family: var(--font-display); font-size: clamp(3.4rem, 6vw, 7rem); font-weight: 400; line-height: .88; letter-spacing: -.05em; }
    .private-hero p:last-of-type { max-width: 28rem; color: #505b58; }
    .private-actions { display: grid; gap: .2rem; margin-top: 2rem; }
    .private-actions a { display: flex; justify-content: space-between; padding: 1rem 0; border-top: 1px solid rgba(20,32,31,.2); color: inherit; text-decoration: none; }
    .private-actions a::after { content: '→'; }
    .private-heading { padding: clamp(4rem, 9vw, 9rem) clamp(1rem, 4vw, 4rem); }
    .private-heading p:last-child { max-width: 42rem; color: #505b58; }
    .private-sequence { display: grid; gap: clamp(5rem, 10vw, 11rem); padding: 0 clamp(1rem, 4vw, 4rem) clamp(6rem, 12vw, 12rem); }
    .private-frame { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(240px, .55fr); gap: clamp(1.5rem, 5vw, 6rem); align-items: end; }
    .private-frame:nth-child(even) img { order: 2; }
    .private-frame img { width: 100%; height: min(82svh, 900px); object-fit: contain; background: #e1e5e1; }
    .private-frame figcaption { padding: 1rem 0; border-top: 1px solid rgba(20,32,31,.2); }
    .private-frame small { display: block; margin-bottom: .6rem; color: var(--private-blue); font: 600 .7rem/1.2 var(--font-ui); letter-spacing: .12em; text-transform: uppercase; }
    .private-frame strong { display: block; font-family: var(--font-display); font-size: clamp(2rem, 3.5vw, 3.8rem); font-weight: 400; line-height: .98; }
    .private-frame p { color: #505b58; }
    .private-index { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1rem, 3vw, 3rem); padding: 0 clamp(1rem, 4vw, 4rem) clamp(6rem, 12vw, 12rem); }
    .private-index a { color: inherit; text-decoration: none; }
    .private-index img { width: 100%; height: min(68svh, 680px); object-fit: contain; background: #e1e5e1; }
    .private-index h2 { margin: 1rem 0 .25rem; font-family: var(--font-display); font-size: 2rem; font-weight: 400; }
    .private-index p { margin: 0; color: #505b58; }
    .private-note { margin: 0 clamp(1rem, 4vw, 4rem) clamp(5rem, 10vw, 10rem); padding: 2rem; border-left: 3px solid var(--private-blue); background: #e5e9e6; }
    @media (max-width: 760px) {
      .private-nav { align-items: flex-start; }
      .private-nav div { gap: .7rem; flex-wrap: wrap; justify-content: flex-end; }
      .private-hero { display: flex; flex-direction: column; }
      .private-hero figure { height: 72svh; min-height: 520px; }
      .private-hero img { height: 72svh; }
      .private-hero__copy { padding: 2.5rem 1rem 3.5rem; }
      .private-frame { display: flex; flex-direction: column; gap: 1rem; }
      .private-frame:nth-child(even) img { order: 0; }
      .private-frame img { height: min(74svh, 680px); }
      .private-index { grid-template-columns: 1fr; gap: 4rem; }
    }
  </style>
</head>
<body>
  <div class="private-banner">Aperçu local privé · Images extraites de la planche Drive · Ne pas publier</div>
  <nav class="private-nav" aria-label="Navigation de la maquette privée"><strong>ANAD / regard photographique</strong><div>${links}</div></nav>
  <main>${content}</main>
</body>
</html>`;
}

const home = page({
  title: 'Accueil',
  current: 'home',
  content: `
    <section class="private-hero">
      <figure><img src="media/blue-01-overview-19126.jpg" alt="Vue d’ensemble du bâtiment d’angle à structure métallique bleue"></figure>
      <div class="private-hero__copy">
        <p class="private-kicker">Photographies de Christophe Aspel</p>
        <h1>Le regard avant le récit.</h1>
        <p>Une architecture se découvre d’abord à distance, puis par ses seuils, ses matières et ses détails.</p>
        <div class="private-actions"><a href="series-blue.html">Explorer cette série</a><a href="portfolio.html">Voir le portfolio</a></div>
      </div>
    </section>`,
});

const portfolio = page({
  title: 'Portfolio',
  current: 'portfolio',
  content: `
    <header class="private-heading"><p class="private-kicker">Portfolio</p><h1>Des lieux, pas une mosaïque.</h1><p>Chaque ensemble reste séparé tant que son identification et son contexte ne sont pas vérifiés.</p></header>
    <section class="private-sequence">
      <figure class="private-frame"><img src="media/blue-01-overview-19126.jpg" alt="Vue d’ensemble du bâtiment bleu"><figcaption><small>Série cohérente · 5 vues</small><strong>Le bâtiment bleu</strong><p>Vue générale, élévation, porte, ferronnerie et décor. Identification documentaire à confirmer.</p><div class="private-actions"><a href="series-blue.html">Parcourir la série</a></div></figcaption></figure>
    </section>
    <section class="private-index" aria-label="Autres sujets distincts">
      <article><img src="media/interior-a-19136.jpg" alt="Intérieur orné avec table centrale"><h2>Intérieur A</h2><p>Identité non vérifiée.</p></article>
      <article><img src="media/hall-01-interior-19157.jpg" alt="Vue intérieure d’une halle"><h2>Halle</h2><p>Ensemble distinct, trois vues disponibles.</p></article>
      <article><img src="media/other-facade-19114.jpg" alt="Façade aux briques claires"><h2>Autre façade</h2><p>Identité non vérifiée.</p></article>
    </section>`,
});

const blueSeries = page({
  title: 'Série bleue',
  current: 'series',
  content: `
    <header class="private-heading"><p class="private-kicker">Dossier photographique pilote · identité à vérifier</p><h1>Du bâtiment au détail.</h1><p>Une séquence de découverte visuelle. Aucun nom d’édifice, architecte ou fait historique n’est déduit de l’apparence des images.</p></header>
    <section class="private-sequence">
      <figure class="private-frame"><img src="media/blue-01-overview-19126.jpg" alt="Vue d’ensemble du bâtiment d’angle à structure métallique bleue"><figcaption><small>01 · Situer</small><strong>La silhouette d’angle</strong><p>La vue générale ouvre le parcours sans recadrage décoratif.</p></figcaption></figure>
      <figure class="private-frame"><img src="media/blue-02-turret-19123.jpg" alt="Tourelle et partie haute du bâtiment bleu"><figcaption><small>02 · Lever le regard</small><strong>La partie haute</strong><p>Le changement d’échelle révèle la structure verticale et son couronnement.</p></figcaption></figure>
      <figure class="private-frame"><img src="media/blue-03-door-19122.jpg" alt="Porte et encadrement du bâtiment bleu"><figcaption><small>03 · Entrer</small><strong>Le seuil</strong><p>La porte est présentée comme une photographie à part entière.</p></figcaption></figure>
      <figure class="private-frame"><img src="media/blue-04-oriel-19119.jpg" alt="Oriel, balcon et ferronnerie du bâtiment bleu"><figcaption><small>04 · Lire la matière</small><strong>Oriel et ferronnerie</strong><p>Une vue horizontale conserve son format et sa respiration.</p></figcaption></figure>
      <figure class="private-frame"><img src="media/blue-05-detail-19118.jpg" alt="Gros plan sur le décor métallique bleu"><figcaption><small>05 · Observer</small><strong>Le décor bleu</strong><p>Le détail ferme la séquence photographique avant les futures informations documentaires.</p></figcaption></figure>
    </section>
    <aside class="private-note"><strong>Étape documentaire suivante</strong><p>Identifier le bâtiment et vérifier provenance, droits, architecte, date et sources avant toute publication. La maquette n’invente aucune de ces informations.</p></aside>`,
});

await ensurePrivateSources();
await fs.rm(TARGET, { recursive: true, force: true });
await fs.mkdir(MEDIA_TARGET, { recursive: true });
await Promise.all(FILES.map((file) => fs.copyFile(path.join(SOURCE, file), path.join(MEDIA_TARGET, file))));
await Promise.all([
  fs.writeFile(path.join(TARGET, 'index.html'), home, 'utf8'),
  fs.writeFile(path.join(TARGET, 'portfolio.html'), portfolio, 'utf8'),
  fs.writeFile(path.join(TARGET, 'series-blue.html'), blueSeries, 'utf8'),
]);

console.log(`Private preview prepared from ${SOURCE}`);
console.log('Private media exists only in dist/private for this local run.');
