import Section from './Section';
import { about, updates } from '@/data/profile';

export default function About() {
  return (
    <Section id="about" label="About">
      <div className="max-w-measure space-y-5 text-[17px] leading-[1.75] text-ink-soft">
        {about.paragraphs.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>

      <h3 className="mt-14 font-mono text-[11px] font-medium uppercase tracking-[0.22em] text-muted">
        Recent updates
      </h3>
      <ul className="mt-4 max-w-2xl divide-y divide-line border-y border-line">
        {updates.map((update) => (
          <li key={update.date} className="grid grid-cols-[5.5rem_minmax(0,1fr)] gap-4 py-3">
            <span className="pt-0.5 font-mono text-xs text-faint">{update.date}</span>
            <span className="text-[15px] leading-relaxed text-ink-soft">{update.text}</span>
          </li>
        ))}
      </ul>
    </Section>
  );
}
