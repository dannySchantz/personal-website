import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowLeft, Atom, Code2, Layers, Target } from 'lucide-react';
import Navigation from '@/components/Navigation';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: '1-D Monte Carlo Neutron Transport | Danny Schantz',
  description:
    'A Python Monte Carlo solver for one-dimensional neutron transport in slab geometries — particle tracking, tallies, and transport estimates.',
  openGraph: {
    title: '1-D Monte Carlo Neutron Transport | Danny Schantz',
    description:
      'A Python Monte Carlo solver for one-dimensional neutron transport in slab geometries.',
    type: 'article',
    url: 'https://dannyschantz.com/1dMC',
  },
};

const highlights = [
  {
    icon: Atom,
    title: 'Particle Tracking',
    description:
      'Simulates individual neutron histories through a 1-D slab, sampling free paths and interaction outcomes.',
  },
  {
    icon: Target,
    title: 'Tallies & Estimates',
    description:
      'Accumulates transmission, reflection, and flux estimators with statistical uncertainty from many histories.',
  },
  {
    icon: Layers,
    title: 'Slab Geometry',
    description:
      'Models layered materials with position-dependent cross sections across a one-dimensional domain.',
  },
  {
    icon: Code2,
    title: 'Python Stack',
    description:
      'Built with Python, NumPy for vectorized sampling, and Matplotlib for flux and convergence plots.',
  },
];

const methods = [
  {
    title: 'Source sampling',
    body: 'Neutrons are born from a defined source (e.g. isotropic or beam-like) with an initial position and direction cosine μ.',
  },
  {
    title: 'Free-flight sampling',
    body: 'The distance to the next collision is sampled from an exponential distribution using the total macroscopic cross section Σ_t.',
  },
  {
    title: 'Collision treatment',
    body: 'At each interaction, absorption or scatter is chosen from material probabilities; scatters update direction before the history continues.',
  },
  {
    title: 'Boundary & scoring',
    body: 'Histories that leave left or right faces contribute to reflection or transmission tallies; track-length or collision estimators score flux in bins.',
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
            1-D Monte Carlo Neutron Transport
          </h1>
          <p className="text-gray-300 text-lg md:text-xl leading-relaxed mb-8 max-w-3xl">
            A from-scratch Python Monte Carlo code that transports neutrons through a
            one-dimensional slab, estimates leakage and flux, and demonstrates the
            statistical foundations of particle transport methods used in reactor analysis.
          </p>

          <div className="flex flex-wrap gap-2 mb-16">
            {['Python', 'Monte Carlo', 'Neutron Transport', 'NumPy', 'Matplotlib'].map(
              (tag) => (
                <span
                  key={tag}
                  className="text-xs font-mono text-gray-300 bg-white/5 border border-white/10 px-3 py-1.5 rounded"
                >
                  {tag}
                </span>
              )
            )}
          </div>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Overview</h2>
            <div className="space-y-4 text-gray-400 leading-relaxed">
              <p>
                Monte Carlo methods solve the neutron transport equation by simulating
                large numbers of random particle histories rather than discretizing the
                integro-differential Boltzmann equation directly. In one dimension, the
                geometry collapses to a slab (or stack of slabs) along{' '}
                <span className="text-gray-300 font-mono">x</span>, which makes the
                algorithm transparent while still capturing the essential physics:
                streaming, collision, absorption, and scatter.
              </p>
              <p>
                This project implements that workflow in Python — sampling paths,
                applying material interactions, and tallying quantities of interest with
                accompanying statistical error bars as the number of histories grows.
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
            <h2 className="text-2xl font-semibold text-white mb-4">Method</h2>
            <p className="text-gray-400 leading-relaxed mb-8">
              Each neutron history follows a simple loop until it is absorbed or escapes
              the domain:
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
            <h2 className="text-2xl font-semibold text-white mb-4">
              Why one dimension first
            </h2>
            <div className="glass rounded-xl p-6 md:p-8 space-y-4 text-gray-400 leading-relaxed">
              <p>
                A 1-D slab is the classic teaching and verification problem for Monte
                Carlo transport: the geometry is simple enough to reason about by hand,
                yet rich enough to compare against analytic solutions (pure absorbers,
                isotropic scattering slabs) and deterministic discrete-ordinates
                benchmarks.
              </p>
              <p>
                Building the solver this way also sets up natural extensions — energy
                groups, anisotropic scatter, variance reduction, and eventually
                multi-dimensional geometries — without losing sight of how each random
                sample contributes to a physical estimate.
              </p>
            </div>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold text-white mb-4">Tech stack</h2>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-start gap-3">
                <span className="text-primary-500 mt-1.5">▹</span>
                <span>
                  <span className="text-gray-300">Python</span> — core simulation loop
                  and history management
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary-500 mt-1.5">▹</span>
                <span>
                  <span className="text-gray-300">NumPy</span> — random sampling and
                  array-based tallies
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary-500 mt-1.5">▹</span>
                <span>
                  <span className="text-gray-300">Matplotlib</span> — flux profiles,
                  leakage estimates, and convergence diagnostics
                </span>
              </li>
            </ul>
          </section>

          <div className="glass rounded-xl p-6 md:p-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h2 className="text-white font-semibold mb-1">Want to dig deeper?</h2>
              <p className="text-gray-400 text-sm">
                Reach out if you&apos;d like to discuss the implementation or related
                transport work.
              </p>
            </div>
            <Link
              href="/#contact"
              className="inline-flex items-center justify-center px-6 py-3 text-sm font-medium rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white hover:opacity-90 transition-opacity"
            >
              Get in touch
            </Link>
          </div>
        </div>
      </article>

      <Footer />
    </main>
  );
}
