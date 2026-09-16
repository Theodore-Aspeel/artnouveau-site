import assert from 'node:assert/strict';
import fs from 'node:fs';

const css = fs.readFileSync('src/assets/styles/main.css', 'utf8');

function mediaBlock(maxWidth) {
  const marker = `@media (max-width: ${maxWidth}px)`;
  const start = css.indexOf(marker);
  assert.notEqual(start, -1, `${marker} should exist`);

  const open = css.indexOf('{', start);
  let depth = 0;

  for (let index = open; index < css.length; index += 1) {
    if (css[index] === '{') depth += 1;
    if (css[index] === '}') depth -= 1;
    if (depth === 0) return css.slice(open + 1, index);
  }

  assert.fail(`${marker} should have a closing brace`);
}

const tablet = mediaBlock(960);
const editorialMobile = mediaBlock(700);
const compactMobile = mediaBlock(800);
const narrowMobile = mediaBlock(380);

assert.match(
  tablet,
  /\.article-intake__header,\s*\.article-intake__figure\s*{\s*grid-column:\s*1;/,
  'article header and image should stay in the explicit single responsive column'
);
assert.match(
  tablet,
  /\.article-intake__figure\s*{[^}]*order:\s*-1;/s,
  'article image should lead the responsive article intake'
);
assert.match(
  editorialMobile,
  /\.home-hero__figure\s*{[^}]*order:\s*-1;/s,
  'home photography should lead the narrow-screen editorial hierarchy'
);
assert.match(
  editorialMobile,
  /\.home-hero__image,\s*\.article-intake__image\s*{[^}]*max-height:\s*72svh;[^}]*border-radius:\s*0;[^}]*box-shadow:\s*none;/s,
  'mobile lead images should be immersive without covering more than 72svh'
);
assert.match(
  editorialMobile,
  /\.home-journal__tags,\s*\.article-header__meta\s*{[^}]*flex-wrap:\s*nowrap;[^}]*overflow-x:\s*auto;/s,
  'dense mobile filters should use a single scrollable row'
);
assert.match(
  editorialMobile,
  /\.tag-chip\s*{[^}]*min-height:\s*44px;[^}]*border-radius:\s*4px;[^}]*box-shadow:\s*none;/s,
  'all mobile tags should preserve a 44px touch target and a restrained surface'
);
assert.match(
  editorialMobile,
  /\.tag-chip:focus-visible\s*{[^}]*outline:\s*2px solid #845f26;[^}]*outline-offset:\s*-3px;/s,
  'scrollable mobile tags should keep a visible unclipped keyboard focus indicator'
);
assert.match(
  editorialMobile,
  /\.article-verified-quote\s*{[^}]*padding-left:\s*1rem;/s,
  'mobile verified quotes should keep breathing room beside their rule'
);
assert.match(
  compactMobile,
  /\.site-nav__list a\s*{[^}]*min-height:\s*44px;[^}]*border-radius:\s*0;[^}]*background:\s*transparent;/s,
  'mobile menu links should be touchable and visually editorial rather than card-like'
);
assert.match(
  compactMobile,
  /\.site-nav__lang-link\s*{[^}]*min-height:\s*44px;/s,
  'mobile language controls should keep a 44px touch height'
);
assert.match(
  compactMobile,
  /\.site-nav\s*{[^}]*background:\s*var\(--an-bg-soft\);[^}]*backdrop-filter:\s*none;/s,
  'mobile navigation should use a stable opaque surface'
);
assert.match(
  narrowMobile,
  /\.site-nav__actions\s*{[^}]*width:\s*100%;[^}]*justify-content:\s*space-between;/s,
  'very narrow screens should move navigation actions to a safe full-width row'
);
assert.match(css, /:where\(a, button, \[tabindex\]\):focus-visible/, 'interactive controls should expose keyboard focus');
assert.match(
  css,
  /@media \(prefers-reduced-motion: reduce\)[\s\S]*?html\s*{\s*scroll-behavior:\s*auto;/,
  'reduced-motion users should not receive smooth scrolling'
);
