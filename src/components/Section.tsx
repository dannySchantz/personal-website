import type { ReactNode } from 'react';

/**
 * A CV-style section: the heading sits in a right-aligned rail on wide
 * screens (and stays put while long sections scroll), with a hairline spine
 * separating it from the content. On small screens it stacks like a normal
 * document heading.
 */
export default function Section({
  id,
  label,
  children,
}: {
  id: string;
  label: string;
  children: ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-20">
      <div className="mx-auto max-w-5xl px-6 md:grid md:grid-cols-[8.5rem_minmax(0,1fr)] md:gap-x-8">
        <h2 className="self-start pt-12 font-serif text-2xl font-semibold tracking-tight md:sticky md:top-24 md:pt-20 md:text-right md:font-mono md:text-[11px] md:font-medium md:uppercase md:tracking-[0.22em] md:text-muted">
          {label}
        </h2>

        <div className="mt-6 border-t border-line pt-8 pb-16 md:mt-0 md:border-l md:border-t-0 md:py-20 md:pl-8">
          {children}
        </div>
      </div>
    </section>
  );
}
