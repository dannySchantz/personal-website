'use client';

const skillCategories = [
  {
    title: 'Programming Languages',
    skills: ['Python', 'JavaScript', 'TypeScript', 'MATLAB', 'C++'],
  },
  {
    title: 'Machine Learning & AI',
    skills: ['PyTorch', 'TensorFlow', 'Physics-Informed Neural Networks', 'Deep Learning', 'Predictive Analytics'],
  },
  {
    title: 'Scientific Computing',
    skills: ['Numerical Methods', 'HPC (HiPerGator)', 'Plasma Physics Simulations', 'Fokker-Planck Solvers', 'Parallel Computing'],
  },
  {
    title: 'Domain Expertise',
    skills: ['Nuclear Engineering', 'Plasma Physics', 'Chemical Engineering', 'Thermodynamics', 'Transport Phenomena'],
  },
  {
    title: 'Tools & Technologies',
    skills: ['Git', 'Linux', 'Docker', 'Jupyter', 'LaTeX'],
  },
  {
    title: 'Soft Skills',
    skills: ['Technical Writing', 'Research', 'Problem Solving', 'Presentation', 'Collaboration'],
  },
];

export default function Skills() {
  return (
    <section id="skills" className="py-24 px-6 relative">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-accent-950/10 to-transparent pointer-events-none" />
      
      <div className="max-w-6xl mx-auto relative">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
          Skills & <span className="text-gradient">Technologies</span>
        </h2>
        <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
          A comprehensive toolkit spanning scientific computing, machine learning, and software development
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {skillCategories.map((category, index) => (
            <div
              key={index}
              className="glass rounded-xl p-6 hover:bg-white/10 transition-all duration-300"
            >
              <h3 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-gradient-to-r from-primary-500 to-accent-500" />
                {category.title}
              </h3>
              <div className="flex flex-wrap gap-2">
                {category.skills.map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1.5 text-sm bg-white/5 text-gray-300 rounded-lg hover:bg-primary-500/20 hover:text-primary-400 transition-colors cursor-default"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16">
          {[
            { value: 'M.S.', label: 'Degree in Progress' },
            { value: 'UF', label: 'University of Florida' },
            { value: 'PINNs', label: 'Research Focus' },
            { value: 'HPC', label: 'Computing Resources' },
          ].map((stat, index) => (
            <div
              key={index}
              className="text-center glass rounded-xl p-6"
            >
              <div className="text-3xl md:text-4xl font-bold text-gradient mb-2">
                {stat.value}
              </div>
              <div className="text-gray-400 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
