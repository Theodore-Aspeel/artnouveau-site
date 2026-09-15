import path from 'node:path';
import sharp from 'sharp';

const results = {};

for (const candidate of process.argv.slice(2)) {
  const absolutePath = path.resolve(candidate);
  try {
    const metadata = await sharp(absolutePath).metadata();
    results[absolutePath] = Boolean(metadata.format && metadata.width && metadata.height);
  } catch {
    results[absolutePath] = false;
  }
}

process.stdout.write(JSON.stringify(results));
