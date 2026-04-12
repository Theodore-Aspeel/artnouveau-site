# code_review.md

## Goal

Review code and content-model changes for correctness, regressions, maintainability, and repository-specific conventions.

## Review checklist

1. Scope
- Did the change stay within the requested scope?
- Did it avoid opportunistic refactors?

2. Backward compatibility
- Does mixed v1/v2 behavior still work when required?
- Are fallback paths still safe?

3. Data-model discipline
- Are visible texts inside content.fr / content.en when relevant?
- Are stable technical keys kept outside localized content?
- Is truth duplicated unnecessarily?
- Are internal notes such as gaps, method notes, source notes, or editorial workflow metadata kept out of public runtime data unless deliberately publishable?
- Do v2 resources keep stable URLs/identifiers separate from localized visible labels and notes?

4. Runtime safety
- Did rendering logic move toward helper-based access instead of direct legacy field access?
- If direct field access remains, is it local, fallback-safe, and only present because no helper exists yet?
- Did the change avoid hidden breakage in gallery or article pages?

5. Build and validation
- Was `npm run validate` run?
- Was `npm run build` run?
- For read-only reviews, was `npm run build` skipped unless a generated artifact was needed?
- Were results stated explicitly?

6. Diff quality
- Is the diff small and readable?
- Are comments minimal but useful?
- Are unrelated file changes absent?

7. Intentional omissions
- Does the task clearly state what was not done?

## Review output format

Return:
- files reviewed
- issues found
- risky patterns
- recommended corrections
- whether the task is acceptable as-is
