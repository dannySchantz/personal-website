import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowLeft, Github } from 'lucide-react';
import Navigation from '@/components/Navigation';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: '1-D Fission Reactor Monte Carlo',
  description:
    'Multigroup 1-D Monte Carlo neutron transport with a finite-difference diffusion reference for UO₂/MOX assembly slab geometries.',
  openGraph: {
    title: '1-D Fission Reactor Monte Carlo · Danny Schantz',
    description:
      'Multigroup 1-D Monte Carlo neutron transport with a finite-difference diffusion reference.',
    type: 'article',
    url: 'https://dannyschantz.com/1dMC',
  },
};

const REPO_URL = 'https://github.com/dannySchantz/1-D-Fission-Reactor-MC';

const stack = ['Python', 'Monte Carlo', 'Diffusion', 'NumPy', 'Numba', 'Matplotlib'];

const capabilities = [
  {
    title: 'Monte Carlo k-eigenvalue',
    body: 'History-based particle tracking with fission-source iteration, track-length flux tallies, and surface current scoring.',
  },
  {
    title: 'Diffusion reference',
    body: 'Paired multigroup finite-difference diffusion solver with power iteration, for verification and mesh studies.',
  },
  {
    title: 'Assembly slab geometry',
    body: '1-D pin-cell and assembly models with UO₂ and MOX fuels, water, and control-rod materials in 2- and 7-group libraries.',
  },
  {
    title: 'Python + Numba',
    body: 'NumPy-based core with optional Numba kernels for faster tracking, plus Matplotlib analysis scripts.',
  },
];

const method = [
  {
    title: 'Fission birth & banking',
    body: 'Generations start from a fuel-region guess, then from a fission bank. Each history samples position, energy group (χ), and direction cosine μ.',
  },
  {
    title: 'Free flight & collisions',
    body: 'Path lengths are sampled from Σ_t. Particles either collide in a mesh cell (capture, fission, in-scatter, or down-scatter) or cross mesh and material interfaces.',
  },
  {
    title: 'Boundaries & tallies',
    body: 'Reflective or vacuum faces are applied per energy group. Track-length flux and signed surface currents accumulate every generation.',
  },
  {
    title: 'k-effective estimate',
    body: 'k is the fission-bank size divided by histories per generation. Inactive generations are skipped before averaging active-generation statistics.',
  },
];

export default function OneDMonteCarloPage() {
  return (
    <>
      <Navigation />

      <main id="main" tabIndex={-1} className="mx-auto max-w-5xl px-6 pb-24 pt-10 md:pt-16">
        <Link
          href="/#projects"
          className="inline-flex items-center gap-2 font-mono text-xs text-muted transition-colors hover:text-ink"
        >
          <ArrowLeft className="h-3.5 w-3.5" aria-hidden="true" />
          Back to projects
        </Link>

        <header className="mt-10">
          <h1 className="max-w-3xl text-3xl font-semibold leading-tight tracking-tight md:text-5xl">
            1-D Fission Reactor Monte Carlo
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-soft">
            A multigroup Monte Carlo neutron transport code for one-dimensional
            fission-reactor slabs, with a finite-difference diffusion solver for
            reference solutions, flux and current plots, and convergence studies.
          </p>

          <p className="mt-6 font-mono text-xs leading-relaxed text-muted">
            {stack.map((tag, index) => (
              <span key={tag}>
                {tag}
                {index < stack.length - 1 && (
                  <span className="px-2 text-faint" aria-hidden="true">
                    &middot;
                  </span>
                )}
              </span>
            ))}
          </p>

          <p className="mt-4 font-mono text-xs">
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="prose-link"
            >
              View on GitHub <span aria-hidden="true">&nearr;</span>
            </a>
          </p>

          <hr className="rule-double mt-12" />
        </header>

        <section aria-labelledby="overview" className="mt-14">
          <h2 id="overview" className="text-2xl font-semibold tracking-tight">
            Overview
          </h2>
          <div className="mt-5 max-w-measure space-y-4 leading-[1.75] text-ink-soft">
            <p>
              This project solves multigroup neutron transport in a 1-D assembly
              geometry representing UO₂ and MOX pin lattices. The Monte Carlo
              solver tracks individual neutron histories generation by generation
              to estimate k-effective, group fluxes, and currents.
            </p>
            <p>
              A companion finite-difference diffusion eigenvalue solver provides
              deterministic reference solutions on the same mesh and cross-section
              data, useful for verification, mesh refinement studies, and
              comparing transport versus diffusion behavior.
            </p>
          </div>
        </section>

        <section aria-labelledby="capabilities" className="mt-14">
          <h2 id="capabilities" className="text-2xl font-semibold tracking-tight">
            What it does
          </h2>
          <ul className="mt-5 divide-y divide-line border-y border-line">
            {capabilities.map((item) => (
              <li
                key={item.title}
                data-print-avoid-break
                className="grid gap-x-8 gap-y-1 py-5 md:grid-cols-[11rem_minmax(0,1fr)]"
              >
                <h3 className="pt-0.5 font-semibold md:text-right">{item.title}</h3>
                <p className="max-w-measure text-[15px] leading-relaxed text-ink-soft">
                  {item.body}
                </p>
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="method" className="mt-14">
          <h2 id="method" className="text-2xl font-semibold tracking-tight">
            Monte Carlo method
          </h2>
          <p className="mt-4 max-w-measure leading-relaxed text-ink-soft">
            Each generation follows the classic fission-source iteration loop:
          </p>
          <ol className="mt-6 max-w-measure space-y-6">
            {method.map((step, index) => (
              <li key={step.title} className="flex gap-5">
                <span
                  className="w-6 shrink-0 pt-0.5 text-right font-serif text-lg italic leading-snug text-accent"
                  aria-hidden="true"
                >
                  {index + 1}.
                </span>
                <div>
                  <h3 className="font-semibold">{step.title}</h3>
                  <p className="mt-1 text-[15px] leading-relaxed text-ink-soft">
                    {step.body}
                  </p>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section aria-labelledby="setups" className="mt-14">
          <h2 id="setups" className="text-2xl font-semibold tracking-tight">
            Problem setups
          </h2>
          <div className="mt-5 max-w-measure space-y-4 leading-[1.75] text-ink-soft">
            <p>
              Input decks cover 2-group and 7-group cross sections with
              configurations such as UO₂–UO₂, MOX–MOX, and UO₂–MOX assembly pairs.
              Mesh density is controlled by meshes-per-fuel-rod and
              meshes-per-water-rod settings in the deck.
            </p>
            <p>
              Analysis scripts plot power-normalized fluxes and currents, run mesh
              and generation convergence studies, collapse 7-group results to
              2-group, and explore extra configurations such as reflectors and
              control rods.
            </p>
          </div>
        </section>

        <div className="mt-16 border-4 border-double border-line-strong px-6 py-6 md:flex md:items-center md:justify-between md:gap-8">
          <div>
            <h2 className="font-semibold">See the code</h2>
            <p className="mt-1 text-sm text-ink-soft">
              Full solvers, input decks, and plotting scripts are on GitHub.
            </p>
          </div>
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 border border-line-strong px-5 py-2.5 font-mono text-xs uppercase tracking-[0.14em] text-ink transition-colors hover:border-accent hover:text-accent md:mt-0"
          >
            <Github className="h-3.5 w-3.5" aria-hidden="true" />
            Open repository
          </a>
        </div>
      </main>

      <Footer />
    </>
  );
}
