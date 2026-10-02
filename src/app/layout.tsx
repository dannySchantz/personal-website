import type { Metadata, Viewport } from 'next';
import localFont from 'next/font/local';
import './globals.css';

/* Self-hosted fonts (no runtime or build-time dependency on Google Fonts). */
const serif = localFont({
  src: [
    {
      path: '../fonts/source-serif-4-normal.woff2',
      style: 'normal',
    },
    {
      path: '../fonts/source-serif-4-italic.woff2',
      style: 'italic',
    },
  ],
  variable: '--font-serif',
  display: 'swap',
});

const mono = localFont({
  src: [
    { path: '../fonts/ibm-plex-mono-400.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/ibm-plex-mono-500.woff2', weight: '500', style: 'normal' },
    { path: '../fonts/ibm-plex-mono-600.woff2', weight: '600', style: 'normal' },
  ],
  variable: '--font-mono',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL('https://dannyschantz.com'),
  title: {
    default: 'Danny Schantz — Nuclear Engineering, University of Florida',
    template: '%s · Danny Schantz',
  },
  description:
    'Danny Schantz is a nuclear engineering graduate student at the University of Florida, building physics-informed neural networks to model runaway-electron dynamics in fusion plasmas.',
  keywords: [
    'Danny Schantz',
    'Nuclear Engineering',
    'University of Florida',
    'Physics-Informed Neural Networks',
    'Plasma Physics',
    'Runaway Electrons',
    'Machine Learning',
  ],
  authors: [{ name: 'Danny Schantz' }],
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Danny Schantz — Nuclear Engineering, University of Florida',
    description:
      'Graduate student in nuclear engineering at the University of Florida, working on physics-informed machine learning for fusion plasmas.',
    type: 'website',
    url: 'https://dannyschantz.com',
    siteName: 'Danny Schantz',
    locale: 'en_US',
    images: [
      {
        url: '/og.png',
        width: 1200,
        height: 630,
        alt: 'Danny Schantz — Nuclear Engineering, University of Florida',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Danny Schantz — Nuclear Engineering, University of Florida',
    description:
      'Graduate student in nuclear engineering at the University of Florida, working on physics-informed machine learning for fusion plasmas.',
    images: ['/og.png'],
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#faf9f5' },
    { media: '(prefers-color-scheme: dark)', color: '#17171a' },
  ],
};

/* Runs before first paint so the theme toggle never flashes the wrong theme. */
const themeInitScript = `(function () {
  try {
    var stored = localStorage.getItem('theme');
    var dark = stored
      ? stored === 'dark'
      : window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.classList.toggle('dark', dark);
  } catch (e) {}
})();`;

const personJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: 'Danny Schantz',
  url: 'https://dannyschantz.com',
  email: 'mailto:danny.schantz@ufl.edu',
  jobTitle: 'Graduate Research Assistant',
  description:
    'Nuclear engineering graduate student at the University of Florida, working on physics-informed neural networks for fusion plasma physics.',
  affiliation: {
    '@type': 'CollegeOrUniversity',
    name: 'University of Florida',
  },
  alumniOf: {
    '@type': 'CollegeOrUniversity',
    name: 'Calvin University',
  },
  address: {
    '@type': 'PostalAddress',
    addressLocality: 'Gainesville',
    addressRegion: 'FL',
    addressCountry: 'US',
  },
  sameAs: [
    'https://github.com/dannySchantz',
    'https://www.linkedin.com/in/dannyschantz',
  ],
  knowsAbout: [
    'Nuclear Engineering',
    'Plasma Physics',
    'Physics-Informed Neural Networks',
    'Machine Learning',
    'Monte Carlo Methods',
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${serif.variable} ${mono.variable}`}
      suppressHydrationWarning
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body>
        <a href="#main" className="skip-link no-print">
          Skip to content
        </a>
        {children}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(personJsonLd) }}
        />
      </body>
    </html>
  );
}
