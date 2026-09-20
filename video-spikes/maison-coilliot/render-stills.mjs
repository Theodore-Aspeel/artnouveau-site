import {mkdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';

const frames = [0, 37, 74, 111, 149];
const outputDirectory = 'video-spikes/maison-coilliot/output/keyframes';
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE;

await mkdir(outputDirectory, {recursive: true});

for (const [index, frame] of frames.entries()) {
  const number = String(index + 1).padStart(2, '0');
  const output = `${outputDirectory}/${number}-frame-${String(frame).padStart(3, '0')}.png`;
  const browserArguments = browserExecutable
    ? [`--browser-executable=${browserExecutable}`]
    : [];
  const result = spawnSync(
    'npx',
    [
      'remotion',
      'still',
      'video-spikes/maison-coilliot/index.ts',
      'MaisonCoilliotStandardSpike',
      output,
      `--frame=${frame}`,
      ...browserArguments,
    ],
    {stdio: 'inherit'},
  );

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}
