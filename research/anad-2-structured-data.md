# ANAD 2.0 - Structured data contract

Date: 2026-09-16  
Branch: `anad-2.0/structured-data`  
Status: minimal Article and Place implementation

## Purpose

Expose a machine-readable description of each canonical article without extending
the factual claims already present in the runtime article model. The structured
data is generated deterministically during the static build.

## Public graph

Each canonical localized article page contains one `application/ld+json` script
with an `@graph` composed of:

1. `Article`
   - canonical URL and stable fragment identifier;
   - canonical page as `mainEntityOfPage`;
   - localized headline and meta description;
   - actual rendered language, including French fallback when required;
   - absolute hero-image URL when present;
   - `Person` author only when `editorial.author` is present;
   - publication dates only when explicit valid ISO values exist;
   - an `about` link only when a stable place name exists.
2. `Place`
   - stable name from `identity.canonical_name` or `identity.exact_name`;
   - address fields only when present in `facts.location`.

Compatibility pages marked `noindex` do not receive this graph.

## Evidence boundaries

The first contract deliberately omits:

- publisher or organization claims;
- architect and creator relations;
- building construction dates;
- heritage or landmark status;
- keywords and inferred categories;
- breadcrumbs and site-level graphs.

Current article publication dates are null. Consequently no current page emits
`datePublished` or `dateModified`. A construction date must never be reused as an
article publication date.

## Safety and determinism

- The serializer escapes `<`, U+2028 and U+2029 before insertion in HTML.
- Property order is deterministic and no build timestamp is emitted.
- Deployment URLs reuse the same site-origin and public-base-path contract as
  canonical and Open Graph metadata.
- No structured-data dependency or runtime JavaScript is added.

## Test coverage

`tests/structured-data.mjs` covers:

- complete v2 Article and Place output;
- null, valid and invalid dates;
- absent author and partial address;
- French locale fallback;
- v1 verified-place compatibility;
- safe deterministic serialization;
- exactly one parseable graph on all 42 canonical article pages;
- absence on noindex compatibility pages.

The root and GitHub Pages deployment profiles must both pass `npm run quality`.

## Future extensions

Add new schema types only in separate reviewed changes after their source contract
is explicit. In particular, `publisher`, site identity, architect relations and
breadcrumbs must not be introduced as constants or editorial guesses.

