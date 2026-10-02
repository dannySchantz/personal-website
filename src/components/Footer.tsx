import { profile } from '@/data/profile';

export default function Footer() {
  return (
    <footer className="no-print border-t border-line">
      <div className="mx-auto flex max-w-5xl flex-col gap-2 px-6 py-10 md:flex-row md:items-baseline md:justify-between">
        <p className="font-mono text-xs text-faint">
          &copy; 2026 {profile.name} &middot; Last updated {profile.lastUpdated}
        </p>
        <p className="font-mono text-xs text-faint">
          Built with Next.js &middot;{' '}
          <a
            href="https://github.com/dannySchantz/personal-website"
            target="_blank"
            rel="noopener noreferrer"
            className="prose-link"
          >
            Source
          </a>{' '}
          &middot; <span className="no-print">This page prints as a CV</span>
        </p>
      </div>
    </footer>
  );
}
