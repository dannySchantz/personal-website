import Section from './Section';
import { research } from '@/data/profile';

export default function Research() {
  return (
    <Section id="research" label="Research">
      <p className="max-w-measure text-lg leading-relaxed text-ink md:text-xl">
        {research.lead}
      </p>

      <div className="mt-6 max-w-measure space-y-5 text-[17px] leading-[1.75] text-ink-soft">
        {research.paragraphs.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>

      <h3 className="mt-14 font-mono text-[11px] font-medium uppercase tracking-[0.22em] text-muted">
        Interests
      </h3>
      <p className="mt-3 max-w-measure text-[17px] leading-relaxed text-ink-soft">
        {research.interests.map((interest, index) => (
          <span key={interest}>
            {interest}
            {index < research.interests.length - 1 && (
              <span className="px-2 text-faint" aria-hidden="true">
                &middot;
              </span>
            )}
          </span>
        ))}
      </p>
    </Section>
  );
}
