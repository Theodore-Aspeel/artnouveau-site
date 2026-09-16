# ANAD 2.0 - Mobile editorial pilot

Date: 2026-09-16
Branch: `anad-2.0/mobile-editorial-pilot`
Scope: homepage and shared article presentation, with Maison Coilliot as the article pilot

## Objective

Improve the narrow-screen reading experience without redesigning the desktop site
or changing published content. The mobile treatment should feel like an authored
architecture publication rather than a stack of application cards.

## Decisions implemented

- Original photography becomes the first narrow-screen entry point on the homepage
  and article pages.
- Lead images use an edge-to-edge treatment below 700 px, without decorative shadow
  or large rounding, and remain capped at 72 percent of the small viewport height.
- The article image and header are explicitly placed in the same responsive grid
  column. This closes the implicit second-column defect that survived below 960 px.
- Dense tag sets become one horizontal row instead of several tall wrapped rows.
- All mobile tag, language and navigation controls keep at least 44 px of touch
  height.
- City/rhythm cards, mobile menu links and secondary editorial panels use flatter
  surfaces with fewer shadows and smaller or no corner radii.
- The full navigation collapses below 800 px so it does not compress at tablet
  widths.
- Keyboard focus remains visible, including inside horizontally scrollable tag rows.
- Reduced-motion mode disables smooth scrolling and transition/animation duration.

## Automated coverage

`tests/mobile-editorial-layout.mjs` protects the structural responsive decisions:

- single-column article placement;
- image-first order;
- viewport-height cap;
- horizontal tag rows and 44 px targets;
- simplified mobile menu treatment;
- 800 px navigation collapse;
- narrow-screen action wrapping;
- keyboard focus and reduced-motion behavior.

The complete project quality command and GitHub Pages deployment profile must both
pass before this branch is considered ready.

## Human validation gate

The change is intentionally not self-approved for production. Before merge, check
the deployed preview or branch result on a real phone at approximately 390 px:

1. Homepage closed menu: image, caption and headline appear in the intended order.
2. Homepage open menu: all links remain easy to tap and the page does not shift
   horizontally.
3. Article Maison Coilliot: the lead photo is visible, followed by the title and
   introduction, with no blank or collapsed implicit column.
4. Tag rows can be swiped horizontally and do not trap vertical page scrolling.
5. No horizontal overflow appears in the article, supporting gallery or footer.
6. At a tablet width near 768 px, the compact navigation is used instead of a
   compressed desktop menu.

## Deliberately unchanged

- desktop layout and card hierarchy;
- article text, translations and photographs;
- publication statuses;
- routes, SEO metadata and build behavior;
- social/Reel and commercial workflows.
