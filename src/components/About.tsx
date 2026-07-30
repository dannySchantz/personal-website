'use client';

import { Atom, Brain, Code2, FlaskConical } from 'lucide-react';

const highlights = [
  {
    icon: Atom,
    title: 'Plasma Physics',
    description: 'Researching runaway electron dynamics and Fokker-Planck equations',
  },
  {
    icon: Brain,
    title: 'Machine Learning',
    description: 'Developing Physics-Informed Neural Networks (PINNs) for scientific computing',
  },
  {
    icon: Code2,
    title: 'Software Development',
    description: 'Building deep learning workflows with Python, PyTorch, and HPC systems',
  },
  {
    icon: FlaskConical,
    title: 'Research',
    description: 'Investigating Dreicer generation mechanisms and electron formation rates',
  },
];

export default function About() {
  return (
    <section id="about" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gradient mb-4">
          About Me
        </h2>
        <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
          Bridging the gap between theoretical physics and computational solutions
        </p>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Image/Visual Section */}
          <div className="relative">
            <div className="aspect-square max-w-md mx-auto relative">
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 to-accent-500/20 rounded-2xl" />
              <div className="absolute inset-4 glass rounded-xl flex items-center justify-center">
                <div className="text-center p-8">
                  <div className="w-32 h-32 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                    <span className="text-5xl font-bold text-white">DS</span>
                  </div>
                  <p className="text-gray-300 font-medium">Nuclear Engineering</p>
                  <p className="text-primary-400 text-sm">University of Florida</p>
                </div>
              </div>
            </div>
          </div>

          {/* Text Content */}
          <div className="space-y-6">
            <p className="text-gray-300 text-lg leading-relaxed">
              I&apos;m a Nuclear Engineering graduate student at the University of Florida with a
              background in Chemical Engineering. My research focuses on developing innovative
              computational methods to solve complex problems in plasma physics.
            </p>
            
            <p className="text-gray-300 text-lg leading-relaxed">
              Currently, I work as a Research Assistant in the Plasma and Fusion Group, where I
              develop Physics-Informed Neural Networks (PINNs) to solve the relativistic
              Fokker-Planck equation. I leverage UF&apos;s HiPerGator HPC resources for large-scale
              model training.
            </p>

            <p className="text-gray-300 text-lg leading-relaxed">
              My work combines deep expertise in plasma physics with cutting-edge machine learning
              techniques to predict primary runaway electron formation rates and model Dreicer
              generation mechanisms.
            </p>

            <div className="pt-4">
              <a
                href="#contact"
                className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors"
              >
                Let&apos;s connect
                <span className="text-xl">→</span>
              </a>
            </div>
          </div>
        </div>

        {/* Highlights Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          {highlights.map((item, index) => (
            <div
              key={index}
              className="glass rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group"
            >
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary-500/20 to-accent-500/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <item.icon className="w-6 h-6 text-primary-400" />
              </div>
              <h3 className="text-white font-semibold mb-2">{item.title}</h3>
              <p className="text-gray-400 text-sm">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
