import type { Config } from 'tailwindcss';

/**
 * Design tokens for the site.
 *
 * The palette is defined as CSS custom properties (see globals.css) so that
 * a single `dark` class on <html> re-themes everything without any
 * `dark:` variant duplication in the markup.
 */
const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        paper: 'var(--bg)',
        'paper-subtle': 'var(--bg-subtle)',
        surface: 'var(--surface)',
        ink: {
          DEFAULT: 'var(--ink)',
          soft: 'var(--ink-soft)',
        },
        muted: 'var(--muted)',
        faint: 'var(--faint)',
        line: {
          DEFAULT: 'var(--line)',
          strong: 'var(--line-strong)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          strong: 'var(--accent-strong)',
          soft: 'var(--accent-soft)',
        },
      },
      fontFamily: {
        serif: [
          'var(--font-serif)',
          'Georgia',
          'Cambria',
          'Times New Roman',
          'serif',
        ],
        mono: ['var(--font-mono)', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace'],
      },
      maxWidth: {
        measure: '68ch',
      },
    },
  },
  plugins: [],
};

export default config;
