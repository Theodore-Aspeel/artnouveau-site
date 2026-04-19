import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const workflowPath = new URL('../research/n8n-social-package-review-workflow.json', import.meta.url);
const workflow = JSON.parse(await readFile(workflowPath, 'utf8'));

assert.equal(workflow.name, 'Art Nouveau Local Social Package Review');
assert.ok(Array.isArray(workflow.nodes), 'workflow should contain nodes');
assert.ok(workflow.connections, 'workflow should contain connections');

const nodeNames = new Set(workflow.nodes.map((node) => node.name));
assert.ok(nodeNames.has('Manual Trigger'), 'workflow should start manually');
assert.ok(nodeNames.has('Run social-package CLI'), 'workflow should run the local social-package CLI');
assert.ok(nodeNames.has('Validate social-package contract'), 'workflow should validate the contract');
assert.ok(nodeNames.has('Candidate gate'), 'workflow should include a queue_status gate');
assert.ok(nodeNames.has('Build local review object'), 'workflow should build a candidate review object');
assert.ok(nodeNames.has('Build local stop review'), 'workflow should stop non-candidates locally');

const commandNode = workflow.nodes.find((node) => node.name === 'Run social-package CLI');
assert.equal(
  commandNode.parameters.command,
  'python -m tools.editorial_manager social-package --next --locale en',
);

const nodeTypes = workflow.nodes.map((node) => node.type);
assert.ok(nodeTypes.includes('n8n-nodes-base.manualTrigger'));
assert.ok(nodeTypes.includes('n8n-nodes-base.executeCommand'));
assert.ok(nodeTypes.includes('n8n-nodes-base.if'));

const serialized = JSON.stringify(workflow).toLowerCase();
assert.equal(serialized.includes('instagram'), false, 'prototype must not include Instagram integration');
assert.equal(serialized.includes('credential'), false, 'prototype must not include credentials');
assert.equal(serialized.includes('webhook'), false, 'prototype must not expose webhooks');
assert.equal(serialized.includes('cron'), false, 'prototype must not include scheduling');
assert.equal(serialized.includes('scheduletrigger'), false, 'prototype must not include scheduling');
assert.equal(serialized.includes('http request'), false, 'prototype must not call external APIs');

console.log('n8n prototype workflow fixture is valid and local-only.');
