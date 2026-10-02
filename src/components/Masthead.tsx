'use client';

import { profile } from '@/data/profile';

export default function Masthead() {
  const separator = <span className="px-2 text-faint" aria-hidden="true">/</span>;

  return (
    <section aria-label="Introduction">
      <div className="mx-auto max-w-5xl px-6 pb-12 pt-16 md:pt-24">
        <h1 className="text-4xl font-semibold leading-tight tracking-tight md:text-5xl lg:text-6xl">
          Danny Schantz
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-soft md:text-xl">
          {profile.role}
        </p>

        <p className="mt-8 font-mono text-[13px] text-muted">
          <a href={`mailto:${profile.email}`} className="prose-link">
            Email
          </a>
          {separator}
          <a href={profile.github} target="_blank" rel="noopener noreferrer" className="prose-link">
            GitHub
          </a>
          {separator}
          <a href={profile.linkedin} target="_blank" rel="noopener noreferrer" className="prose-link">
            LinkedIn
          </a>
          {separator}
          <a href={profile.resumeUrl} className="prose-link">
            CV&nbsp;(PDF)
          </a>
          {separator}
          <button
            type="button"
            onClick={() => window.print()}
            className="prose-link no-print cursor-pointer"
          >
            Print
          </button>
        </p>

        <p className="mt-3 font-mono text-xs text-faint">{profile.location}</p>
      </div>

      <div className="mx-auto max-w-5xl px-6">
        <hr className="rule-double" />
      </div>
    </section>
  );
}
