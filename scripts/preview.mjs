import fs from 'node:fs';
import fsPromises from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const PORT = Number(process.env.PORT || 4173);

const MIME_TYPES = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.jpeg': 'image/jpeg',
  '.jpg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.webp': 'image/webp',
};

function resolveRequestPath(urlPath) {
  const cleanPath = urlPath.split('?')[0];
  const normalized = cleanPath === '/' ? '/index.html' : cleanPath;
  return path.normalize(normalized).replace(/^(\.\.[/\\])+/, '');
}

async function pathExists(targetPath) {
  try {
    await fsPromises.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function runBuild() {
  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(ROOT, 'scripts', 'build.mjs')], {
      cwd: ROOT,
      stdio: 'inherit',
    });

    child.on('error', reject);
    child.on('exit', (code) => {
      if (code === 0) {
        resolve();
        return;
      }

      reject(new Error(`build failed with exit code ${code}`));
    });
  });
}

async function preparePrivatePreview() {
  if (process.env.PRIVATE_PREVIEW !== '1') return;

  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(ROOT, 'scripts', 'prepare-private-preview.mjs')], {
      cwd: ROOT,
      env: process.env,
      stdio: 'inherit',
    });

    child.on('error', reject);
    child.on('exit', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`private preview preparation failed with exit code ${code}`));
    });
  });
}

function openBrowser(url) {
  if (process.env.OPEN_BROWSER !== '1') return;

  let command;
  let args;

  if (process.platform === 'win32') {
    command = 'cmd';
    args = ['/c', 'start', '', url];
  } else if (process.platform === 'darwin') {
    command = 'open';
    args = [url];
  } else {
    command = 'xdg-open';
    args = [url];
  }

  const child = spawn(command, args, { detached: true, stdio: 'ignore' });
  child.on('error', () => {});
  child.unref();
}

try {
  await runBuild();
  await preparePrivatePreview();
} catch (error) {
  console.error('ERROR\nPreview aborted because the build failed.\n');
  process.exit(1);
}

if (!(await pathExists(DIST))) {
  console.error('ERROR\nMissing dist/ directory after build.\n');
  process.exit(1);
}

const server = http.createServer(async (req, res) => {
  const relativePath = resolveRequestPath(req.url || '/');
  let filePath = path.join(DIST, relativePath);

  try {
    const stat = await fsPromises.stat(filePath).catch(() => null);

    if (stat && stat.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }

    if (!(await pathExists(filePath))) {
      res.statusCode = 404;
      const fallback404 = path.join(DIST, '404.html');
      if (await pathExists(fallback404)) {
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        fs.createReadStream(fallback404).pipe(res);
        return;
      }
      res.end('Not found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    res.statusCode = 200;
    res.setHeader('Content-Type', MIME_TYPES[ext] || 'application/octet-stream');
    fs.createReadStream(filePath).pipe(res);
  } catch (error) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end('Internal server error');
  }
});

server.listen(PORT, () => {
  const route = process.env.PRIVATE_PREVIEW === '1' ? '/private/' : '/fr/';
  const url = `http://localhost:${PORT}${route}`;
  console.log(`Preview server running at ${url}`);
  openBrowser(url);
});
