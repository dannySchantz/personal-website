import Section from './Section';
import { appointments, education } from '@/data/profile';
import type { Entry } from '@/data/profile';

function EntryRow({ entry }: { entry: Entry }) {
  return (
    <li
      data-print-avoid-break
      className="grid gap-x-8 gap-y-1 py-6 md:grid-cols-[8rem_minmax(0,1fr)]"
    >
      <span className="pt-1 font-mono text-xs leading-relaxed text-faint md:text-right">
        {entry.period}
      </span>
      <div>
        <h4 className="text-lg font-semibold leading-snug">{entry.title}</h4>
        <p className="mt-0.5 text-[15px] italic text-muted">{entry.organization}</p>

        {entry.details && (
          <div className="mt-3 max-w-measure space-y-1.5">
            {entry.details.map((detail, index) => (
              <p key={index} className="text-[15px] leading-relaxed text-ink-soft">
                {detail}
              </p>
            ))}
          </div>
        )}

        {entry.bullets && (
          <ul className="mt-3 max-w-measure list-disc space-y-1.5 pl-5 marker:text-faint">
            {entry.bullets.map((bullet, index) => (
              <li key={index} className="text-[15px] leading-relaxed text-ink-soft">
                {bullet}
              </li>
            ))}
          </ul>
        )}
      </div>
    </li>
  );
}

export default function Experience() {
  return (
    <Section id="experience" label="Experience">
      <h3 className="font-mono text-[11px] font-medium uppercase tracking-[0.22em] text-muted">
        Education
      </h3>
      <ul className="mt-2 divide-y divide-line">
        {education.map((entry) => (
          <EntryRow key={entry.title} entry={entry} />
        ))}
      </ul>

      <h3 className="mt-14 font-mono text-[11px] font-medium uppercase tracking-[0.22em] text-muted">
        Appointments
      </h3>
      <ul className="mt-2 divide-y divide-line">
        {appointments.map((entry) => (
          <EntryRow key={entry.title} entry={entry} />
        ))}
      </ul>
    </Section>
  );
}
