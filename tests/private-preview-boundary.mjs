import assert from 'node:assert/strict';
import fs from 'node:fs';

const ignore = fs.readFileSync('.gitignore', 'utf8');
const build = fs.readFileSync('scripts/build.mjs', 'utf8');
const preview = fs.readFileSync('scripts/preview.mjs', 'utf8');
const privatePreview = fs.readFileSync('scripts/prepare-private-preview.mjs', 'utf8');
const home = fs.readFileSync('src/pages/index.html', 'utf8');

assert.match(ignore, /^\/\.private-media\/$/m, 'private source media directory must be ignored');
assert.doesNotMatch(build, /\.private-media|private-media/, 'the public build must not know about private preview media');
assert.match(preview, /process\.env\.PRIVATE_PREVIEW === '1'/, 'private injection must require an explicit local flag');
assert.match(privatePreview, /path\.join\(ROOT, '\.private-media'\)/, 'private preview must read from the ignored local directory');
assert.doesNotMatch(home, /src="[^"]*(?:\.private-media|private-media)\//, 'public source must not reference private media URLs');

for (const file of ['villino-florio-F0027-facade.jpg', 'maison-bastin-F0394-facade.jpg']) {
  assert.ok(privatePreview.includes(file), file + ' should be mapped only by the private helper');
}
