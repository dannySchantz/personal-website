# Danny Schantz — Personal Website

A personal academic homepage that reads like a typeset CV, not like a template.

Production site: [https://dannyschantz.com](https://dannyschantz.com)

## Design

The site follows the conventions of classic researcher homepages (in the
tradition of Jon Barron's single-page academic site and modern Jekyll academic
templates) rather than a marketing-landing layout:

- **Light "paper" theme by default** with a warm graphite dark theme, switched
  by a toggle (persisted, respects `prefers-color-scheme`, no flash on load).
- **Two typefaces**, self-hosted: Source Serif 4 for body and headings,
  IBM Plex Mono for dates, labels, and metadata.
- **CV structure**: masthead with name and an `Email / GitHub / LinkedIn /
  CV / Print` link line over a letterhead double rule; sections with a
  right-aligned rail label and a hairline spine; dates in a left column;
  reverse-chronological education and appointments; skills as definition
  lists rather than tag pills.
- **No cards where a list will do** — no glassmorphism, gradient headlines,
  floating orbs, icon grids, or hover glows.
- **Prints as a CV**: the print stylesheet flattens the theme to black on
  white, hides chrome, and avoids page breaks inside entries. The masthead's
  *Print* action produces a paper copy straight from the browser.

## Content

All facts, dates, links, and copy live in one file:

- `src/data/profile.ts` — edit this to update the site.

Everything else (components, styles) is presentation only.

### Structure

- `src/components/Section.tsx` — the rail-label + spine section shell.
- `src/components/Masthead.tsx` — name, role, contact link line, double rule.
- `src/components/About.tsx`, `Research.tsx`, `Projects.tsx`, `Experience.tsx`,
  `Skills.tsx`, `Contact.tsx` — one file per CV section.
- `src/app/1dMC/page.tsx` — long-form project page for the 1-D fission reactor
  Monte Carlo code, in the same typographic system.
- `src/app/globals.css` — palette tokens (CSS custom properties) and print
  styles.
- `tailwind.config.ts` — maps Tailwind utilities onto those tokens.
- `src/fonts/` — self-hosted woff2 files (served by `next/font/local`, no
  dependency on Google Fonts at build or runtime).
- `public/og.png` — the Open Graph / link-preview card.

## Engineering notes

- Fully static prerender (Next.js App Router); ~90 kB first-load JS.
- `next/font/local` with `display: swap` for zero-render-blocking, no CLS.
- Semantic landmarks, single `h1`, ordered headings, skip link, visible
  `:focus-visible` rings, keyboard-operable theme and menu controls,
  `prefers-reduced-motion` respected.
- Structured data: JSON-LD `Person` schema; `sitemap.xml`, `robots.txt`, and
  `manifest.webmanifest` generated from the app.
- Metadata: per-route titles, Open Graph and Twitter cards with the preview
  image.

## Getting started

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # production build
```

## Deployment

Deployed on Vercel (`vercel.json` enables deployments from `main` only).
This repository's working branches follow Vercel's configuration; merge to
`main` to publish.

## Updating the site

1. Edit `src/data/profile.ts` (facts, dates, projects, skills).
2. If anything structural changes, keep the CV conventions above: hairlines
   over cards, serif body, mono metadata, reverse-chronological order,
   consistent `Mon YYYY` date format.
3. Update `lastUpdated` in `profile.ts` and the `lastModified` dates in
   `src/app/sitemap.ts`.

## Contact

- **Email**: danny.schantz@ufl.edu
- **LinkedIn**: [linkedin.com/in/dannyschantz](https://linkedin.com/in/dannyschantz)
- **GitHub**: [github.com/dannySchantz](https://github.com/dannySchantz)
