import assert from 'node:assert/strict';
import fs from 'node:fs';

const config = fs.readFileSync('netlify.toml', 'utf8');

assert.match(config, /command\s*=\s*"npm run build"/, 'Netlify should run the deterministic build');
assert.match(config, /publish\s*=\s*"dist"/, 'Netlify should publish only dist');
assert.match(config, /NODE_VERSION\s*=\s*"20"/, 'Netlify should use the project Node major');

assert.ok(fs.existsSync('dist/index.html'), 'the preview artifact should contain the homepage');
assert.ok(!fs.existsSync('dist/research'), 'internal research must not enter the preview artifact');
assert.ok(!fs.existsSync('dist/tools'), 'internal editorial tooling must not enter the preview artifact');
