import assert from 'node:assert/strict';
import fs from 'node:fs';

const workflow = fs.readFileSync('.github/workflows/prepare-publication-pr.yml', 'utf8');
const deployWorkflow = fs.readFileSync('.github/workflows/pages.yml', 'utf8');

assert.match(workflow, /workflow_dispatch:/, 'publication workflow must be manually triggered');
assert.match(workflow, /default: dry-run/, 'the safe default must remain a dry run');
assert.match(workflow, /- dry-run\s+- create-pr/, 'only the two reviewed modes are allowed');
assert.match(workflow, /PUBLICATION_CONFIRMATION.*PUBLISH/s, 'write mode must require explicit confirmation');
assert.match(workflow, /publish-article[\s\S]*--json/, 'the read-only preflight must use the guarded transition');
assert.match(workflow, /--write[\s\S]*--approve/, 'the write must reuse explicit CLI approval');
assert.match(workflow, /git diff --quiet -- src\/data\/articles\.json/, 'a real article change must be required');
assert.match(workflow, /awk '\$2 != "src\/data\/articles\.json"/, 'unexpected changed files must block the release');
assert.match(workflow, /actions: write/, 'the workflow must be allowed to dispatch branch CI');
assert.match(workflow, /gh workflow run quality\.yml/, 'the pushed branch must run the existing quality workflow');
assert.match(workflow, /gh run watch[\s\S]*--exit-status/, 'all branch quality profiles must pass before PR creation');
assert.ok(
  workflow.indexOf('gh run watch') < workflow.indexOf('gh pr create'),
  'the pull request must open only after branch CI passes'
);
assert.match(workflow, /gh pr create/, 'approved mode must open a pull request');
assert.doesNotMatch(workflow, /gh pr merge|git push origin main/, 'publication workflow must never merge or push main');

assert.match(deployWorkflow, /push:\s+branches:\s+- main/s, 'deployment must remain tied to main');
assert.doesNotMatch(deployWorkflow, /workflow_run|pull_request:/, 'a publication branch or PR must not deploy');

console.log('Publication PR workflow is manual, guarded and separated from deployment.');
