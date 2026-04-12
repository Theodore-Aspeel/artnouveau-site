# PLANS.md

## Purpose

Use this template for tasks that are multi-step, risky, cross-file, or architecture-sensitive.

## Expected structure of a plan

1. Goal
   - What is the exact outcome?

2. Current state
   - Which files, flows, or constraints matter?
   - What is the current behavior?

3. Risks
   - What could break?
   - What must remain backward compatible?

4. Proposed approach
   - Step-by-step implementation plan
   - Why this order?

5. Validation
   - Which commands must pass?
   - What manual checks are required?
   - For read-only reviews, is source inspection or `npm run validate` enough instead of `npm run build`?

6. Out of scope
   - What is explicitly not part of this task?

7. Deliverables
   - Which files are expected to change?
   - What should be true when the task is done?

## Rules for this repository

- Prefer conservative, progressive changes.
- Do not mix data-model work with visual redesign.
- Do not migrate all articles at once unless explicitly requested.
- Keep v1/v2 compatibility when working on article-model migration.
- Use helpers instead of direct legacy field access when available; tolerate direct access only when no helper exists yet and the fallback stays local.
- Preserve FR fallback unless the task is explicitly about real EN behavior.
- Keep internal workflow metadata out of public runtime data unless it is deliberately publishable.
