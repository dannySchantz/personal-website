import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowLeft, Atom, Code2, Github, Layers, Target } from 'lucide-react';
import Navigation from '@/components/Navigation';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: '1-D Fission Reactor Monte Carlo | Danny Schantz',
  description:
    'Multigroup 1-D Monte Carlo neutron transport with a finite-difference diffusion reference for UO₂/MOX assembly slab geometries.',
  openGraph: {
    title: '1-D Fission Reactor Monte Carlo | Danny Schantz',
    description:
      'Multigroup 1-D Monte Carlo neutron transport with a finite-difference diffusion reference.',
    type: 'article',
    url: 'https://dannyschantz.com/1dMC',
  },
};

const REPO_URL = 'https://github.com/dannySchantz/1-D-Fission-Reactor-MC';

const highlights = [
  {
    icon: Atom,
    title: 'Monte Carlo k-eigenvalue',
    description:
      'History-based particle tracking with fission-source iteration, track-length flux tallies, and surface current scoring.',
  },
  {
    icon: Target,
    title: 'Diffusion reference',
    description:
      'Paired multigroup finite-difference diffusion solver with power iteration for verification and mesh studies.',
  },
  {
    icon: Layers,
    title: 'Assembly slab geometry',
    description:
      '1-D pin-cell / assembly models with UO₂ and MOX fuels, water, and control-rod materials in 2- and 7-group libraries.',
  },
  {
    icon: Code2,
    title: 'Python + Numba',
    description:
      'NumPy-based core with optional Numba kernels for faster tracking, plus Matplotlib analysis scripts.',
  },
];

const methods = [
  {
    title: 'Fission birth & banking',
    body: 'Generations start from a fuel-region guess, then from a fission bank. Each history samples position, energy group (χ), and direction cosine μ.',
  },
  {
    title: 'Free flight & collisions',
    body: 'Path lengths are sampled from Σ_t. Particles either collide in a mesh (capture, fission, in-scatter, or down-scatter) or cross mesh / material interfaces.',
  },
  {
    title: 'Boundaries & tallies',
    body: 'Reflective or vacuum faces are applied per energy group. Track-length flux and signed surface currents accumulate every generation.',
  },
  {
    title: 'k-effective estimate',
    body: 'k is the fission-bank size over histories per generation. Inactive generations are skipped before averaging active-generation statistics.',
  },
];

export default function OneDMonteCarloPage() {
  return (
    <main className="min-h-screen">
      <Navigation />

      <article className="pt-28 pb-24 px-6">
        <div className="max-w-4xl mx-auto">
          <Link
            href="/#projects"
            className="inline-flex items-center gap-2 text-sm text-primary-400 hover:text-primary-300 transition-colors mb-10"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to projects
          </Link>

          <p className="font-mono text-sm tracking-wider text-primary-400 mb-3">
            Computational Nuclear Engineering
          </p>
          <h1 className="text-3xl md:text-5xl font-bold text-gradient mb-6">
            1-D Fission Reactor Monte Carlo
          </h1>
          <p className="text-gray-300 text-lg md:text-xl leading-relaxed mb-8 max-w-3xl">
            A multigroup Monte Carlo neutron transport code for one-dimensional
            fission-reactor slabs — with a finite-difference diffusion solver for
            reference solutions, flux/current plots, and convergence studies.
          </p>

          <div className="flex flex-wrap items-center gap-3 mb-16">
            {['Python', 'Monte Carlo', 'Diffusion', 'NumPy', 'Numba', 'Matplotlib'].map(
              (tag) => (
                <span
                  key={tag}
                  className="text-xs font-mono text-gray-300 bg-white/5 border border-white/10 px-3 py-1.5 rounded"
                >
                  {tag}
                </span>
              )
            )}
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-primary-400 hover:text-primary-300 transition-colors ml-1"
            >
              <Github className="w-4 h-4" />
              View on GitHub
            </a>
          </div>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Overview</h2>
            <div className="space-y-4 text-gray-400 leading-relaxed">
              <p>
                This project solves multigroup neutron transport in a 1-D assembly
                geometry representing UO₂ and MOX pin lattices. The Monte Carlo
                solver tracks individual neutron histories generation by generation
                to estimate k-effective, group fluxes, and currents.
              </p>
              <p>
                A companion finite-difference diffusion eigenvalue solver provides
                deterministic reference solutions on the same mesh and cross-section
                data — useful for verification, mesh refinement studies, and
                comparing transport versus diffusion behavior.
              </p>
            </div>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-8">What it does</h2>
            <div className="grid sm:grid-cols-2 gap-6">
              {highlights.map((item) => (
                <div
                  key={item.title}
                  className="glass rounded-xl p-6 hover:bg-white/10 transition-all duration-300"
                >
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary-500/20 to-accent-500/20 flex items-center justify-center mb-4">
                    <item.icon className="w-6 h-6 text-primary-400" />
                  </div>
                  <h3 className="text-white font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">
                    {item.description}
                  </p>
                </div>
              ))}
            </div>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Monte Carlo method</h2>
            <p className="text-gray-400 leading-relaxed mb-8">
              Each generation follows the classic fission-source iteration loop:
            </p>
            <ol className="space-y-6">
              {methods.map((step, index) => (
                <li key={step.title} className="flex gap-4">
                  <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-500/20 text-primary-400 font-mono text-sm flex items-center justify-center">
                    {index + 1}
                  </span>
                  <div>
                    <h3 className="text-white font-medium mb-1">{step.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{step.body}</p>
                  </div>
                </li>
              ))}
            </ol>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Problem setups</h2>
            <div className="glass rounded-xl p-6 md:p-8 space-y-4 text-gray-400 leading-relaxed">
              <p>
                Input decks cover <span className="text-gray-300">2-group</span> and{' '}
                <span className="text-gray-300">7-group</span> cross sections with
                configurations such as UO₂–UO₂, MOX–MOX, and UO₂–MOX assembly pairs.
                Mesh density is controlled by meshes-per-fuel-rod and
                meshes-per-water-rod settings in the deck.
              </p>
              <p>
                Analysis scripts plot power-normalized fluxes and currents, run mesh
                / generation convergence studies, collapse 7-group results to 2-group,
                and explore extra configurations (reflectors, control rods).
              </p>
            </div>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Tech stack</h2>
            <ul className="space-y-3 text-gray-400">
              <li className="grid grid-cols-[1rem_minmax(0,1fr)] gap-x-3 leading-relaxed">
                <span className="text-primary-500 text-center leading-relaxed select-none" aria-hidden="true">▹</span>
                <span>
                  <span className="text-gray-300">Python</span> — Monte Carlo and
                  diffusion solvers, input parsing, analysis CLIs
                </span>
              </li>
              <li className="grid grid-cols-[1rem_minmax(0,1fr)] gap-x-3 leading-relaxed">
                <span className="text-primary-500 text-center leading-relaxed select-none" aria-hidden="true">▹</span>
                <span>
                  <span className="text-gray-300">NumPy / Numba</span> — array tallies
                  and optional JIT particle tracking
                </span>
              </li>
              <li className="grid grid-cols-[1rem_minmax(0,1fr)] gap-x-3 leading-relaxed">
                <span className="text-primary-500 text-center leading-relaxed select-none" aria-hidden="true">▹</span>
                <span>
                  <span className="text-gray-300">Matplotlib</span> — flux, current,
                  and convergence diagnostics
                </span>
              </li>
            </ul>
          </section>

          <div className="glass rounded-xl p-6 md:p-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h2 className="text-white font-semibold mb-1">See the code</h2>
              <p className="text-gray-400 text-sm">
                Full solvers, input decks, and plotting scripts are on GitHub.
              </p>
            </div>
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 text-sm font-medium rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white hover:opacity-90 transition-opacity"
            >
              <Github className="w-4 h-4" />
              Open repository
            </a>
          </div>
        </div>
      </article>

      <Footer />
    </main>
  );
}
