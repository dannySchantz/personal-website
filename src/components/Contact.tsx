import Section from './Section';
import { profile } from '@/data/profile';

export default function Contact() {
  return (
    <Section id="contact" label="Contact">
      <p className="max-w-measure text-[17px] leading-[1.75] text-ink-soft">
        The quickest way to reach me is email. I&rsquo;m glad to talk about
        physics-informed machine learning, fusion and plasma physics, reactor
        operations, or scientific computing in general.
      </p>

      <p className="mt-8 text-2xl md:text-3xl">
        <a href={`mailto:${profile.email}`} className="prose-link">
          {profile.email}
        </a>
      </p>

      <dl className="mt-12 max-w-md divide-y divide-line border-y border-line">
        <div className="grid grid-cols-[6rem_minmax(0,1fr)] gap-4 py-3">
          <dt className="pt-0.5 font-mono text-xs uppercase tracking-[0.14em] text-faint">
            GitHub
          </dt>
          <dd className="font-mono text-[13px]">
            <a
              href={profile.github}
              target="_blank"
              rel="noopener noreferrer"
              className="prose-link"
            >
              github.com/dannySchantz
            </a>
          </dd>
        </div>
        <div className="grid grid-cols-[6rem_minmax(0,1fr)] gap-4 py-3">
          <dt className="pt-0.5 font-mono text-xs uppercase tracking-[0.14em] text-faint">
            LinkedIn
          </dt>
          <dd className="font-mono text-[13px]">
            <a
              href={profile.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="prose-link"
            >
              linkedin.com/in/dannyschantz
            </a>
          </dd>
        </div>
        <div className="grid grid-cols-[6rem_minmax(0,1fr)] gap-4 py-3">
          <dt className="pt-0.5 font-mono text-xs uppercase tracking-[0.14em] text-faint">
            Location
          </dt>
          <dd className="pt-0.5 text-[15px] text-ink-soft">{profile.location}</dd>
        </div>
        <div className="grid grid-cols-[6rem_minmax(0,1fr)] gap-4 py-3">
          <dt className="pt-0.5 font-mono text-xs uppercase tracking-[0.14em] text-faint">
            CV
          </dt>
          <dd className="font-mono text-[13px]">
            <a href={profile.resumeUrl} className="prose-link">
              Download PDF
            </a>
          </dd>
        </div>
      </dl>
    </Section>
  );
}
