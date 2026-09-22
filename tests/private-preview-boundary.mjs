import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), '..');

test('the standard public build excludes the private photographic preview', () => {
  assert.equal(fs.existsSync(path.join(root, 'dist', 'private')), false);
  assert.equal(fs.existsSync(path.join(root, 'dist', '.private-media')), false);
});
