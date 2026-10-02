import Section from './Section';
import { skills } from '@/data/profile';

export default function Skills() {
  return (
    <Section id="skills" label="Skills">
      <dl className="max-w-3xl divide-y divide-line border-y border-line">
        {skills.map((group) => (
          <div
            key={group.category}
            data-print-avoid-break
            className="grid gap-x-8 gap-y-1 py-4 md:grid-cols-[8rem_minmax(0,1fr)]"
          >
            <dt className="pt-1 font-mono text-xs uppercase tracking-[0.14em] text-faint md:text-right">
              {group.category}
            </dt>
            <dd className="text-[16px] leading-relaxed text-ink-soft">{group.items}</dd>
          </div>
        ))}
      </dl>
    </Section>
  );
}
