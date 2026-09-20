import assert from 'node:assert/strict';
import fs from 'node:fs';

const fileName = 'google91b24d30e59135f1.html';
const expected = 'google-site-verification: google91b24d30e59135f1.html';

assert.equal(
  fs.readFileSync(`public/${fileName}`, 'utf8'),
  expected,
  'source verification file must preserve the exact Google token'
);

assert.equal(
  fs.readFileSync(`dist/${fileName}`, 'utf8'),
  expected,
  'build must publish the Search Console verification file at the site root'
);
