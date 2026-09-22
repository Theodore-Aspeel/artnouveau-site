import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const SOURCE = path.resolve(process.env.PRIVATE_PREVIEW_MEDIA_DIR || path.join(ROOT, '.private-media'));
const TARGET = path.join(DIST, 'private-media');

const FILES = [
  'villino-florio-F0027-facade.jpg',
  'villino-florio-F0005-escalier.jpg',
  'villino-florio-F0013-cheminee.jpg',
  'villino-florio-F0018-vitrail.jpg',
  'maison-bastin-F0394-facade.jpg',
  'maison-bastin-F0717-oriel.jpg',
  'maison-bastin-F0729-vitrail.jpg',
  'maison-bastin-F0746-interieur.jpg',
  'maison-bastin-F0751-portes.jpg',
];

const ALTS = {
  en: {
    'villino-florio-F0027-facade.jpg': 'Exterior view of Villino Florio in Palermo, with its monumental staircase.',
    'villino-florio-F0005-escalier.jpg': 'Interior staircase and decorated ceiling at Villino Florio.',
    'villino-florio-F0013-cheminee.jpg': 'Fireplace and ceramic decoration at Villino Florio.',
    'villino-florio-F0018-vitrail.jpg': 'Stained glass and floral decoration at Villino Florio.',
    'maison-bastin-F0394-facade.jpg': 'Complete facade of Maison des Médecins in Charleroi.',
    'maison-bastin-F0717-oriel.jpg': 'Detail of the projecting bay window at Maison des Médecins.',
    'maison-bastin-F0729-vitrail.jpg': 'Floral stained-glass detail at Maison des Médecins.',
    'maison-bastin-F0746-interieur.jpg': 'Rounded interior perspective at Maison des Médecins.',
    'maison-bastin-F0751-portes.jpg': 'Interior doors at Maison des Médecins.',
  },
  fr: {
    'villino-florio-F0027-facade.jpg': 'Vue extérieure du Villino Florio à Palerme, avec son escalier monumental.',
    'villino-florio-F0005-escalier.jpg': 'Escalier intérieur et plafond décoré du Villino Florio.',
    'villino-florio-F0013-cheminee.jpg': 'Cheminée et décor de céramique du Villino Florio.',
    'villino-florio-F0018-vitrail.jpg': 'Vitrail et décor floral du Villino Florio.',
    'maison-bastin-F0394-facade.jpg': 'Façade complète de la Maison des Médecins à Charleroi.',
    'maison-bastin-F0717-oriel.jpg': 'Détail de l’oriel de la Maison des Médecins.',
    'maison-bastin-F0729-vitrail.jpg': 'Détail du vitrail floral de la Maison des Médecins.',
    'maison-bastin-F0746-interieur.jpg': 'Perspective intérieure arrondie de la Maison des Médecins.',
    'maison-bastin-F0751-portes.jpg': 'Portes intérieures de la Maison des Médecins.',
  },
  nl: {
    'villino-florio-F0027-facade.jpg': 'Buitenaanzicht van Villino Florio in Palermo, met de monumentale trap.',
    'villino-florio-F0005-escalier.jpg': 'Binnentrap en versierd plafond van Villino Florio.',
    'villino-florio-F0013-cheminee.jpg': 'Schouw en keramische decoratie van Villino Florio.',
    'villino-florio-F0018-vitrail.jpg': 'Glas-in-lood en bloemendecoratie van Villino Florio.',
    'maison-bastin-F0394-facade.jpg': 'Volledige gevel van Maison des Médecins in Charleroi.',
    'maison-bastin-F0717-oriel.jpg': 'Detail van de erker van Maison des Médecins.',
    'maison-bastin-F0729-vitrail.jpg': 'Detail van het florale glas-in-lood van Maison des Médecins.',
    'maison-bastin-F0746-interieur.jpg': 'Afgerond interieurperspectief van Maison des Médecins.',
    'maison-bastin-F0751-portes.jpg': 'Binnendeuren van Maison des Médecins.',
  },
};

async function assertSources() {
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

function escapeAttribute(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function injectPrivateMedia(html, locale) {
  let injected = html;
  for (const file of FILES) {
    if (!injected.includes(`data-private-media="${file}"`)) continue;
    const pattern = new RegExp(`(<div[^>]*class="[^"]*mag-private-slot[^"]*"[^>]*data-private-media="${file}"[^>]*>)[\\s\\S]*?(</div>)`, 'g');
    const alt = ALTS[locale]?.[file] || ALTS.en[file] || '';
    injected = injected.replace(pattern, `$1<img src="../private-media/${file}" alt="${escapeAttribute(alt)}" loading="lazy" decoding="async">$2`);
  }

  return injected.replace(
    '<body class="page-home">',
    '<body class="page-home private-review"><p class="private-review__banner">Private local review · Do not publish</p>',
  );
}

await assertSources();
await fs.rm(TARGET, { recursive: true, force: true });
await fs.mkdir(TARGET, { recursive: true });
await Promise.all(FILES.map((file) => fs.copyFile(path.join(SOURCE, file), path.join(TARGET, file))));

for (const locale of ['en', 'fr', 'nl']) {
  const pagePath = path.join(DIST, locale, 'index.html');
  const page = await fs.readFile(pagePath, 'utf8');
  await fs.writeFile(pagePath, injectPrivateMedia(page, locale), 'utf8');
}

console.log(`Private homepage review prepared from ${SOURCE}`);
console.log('Private media exists only in dist/private-media for this local run.');
