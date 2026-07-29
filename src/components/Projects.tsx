'use client';

import { ExternalLink, Github, Folder } from 'lucide-react';

const projects = [
  {
    title: 'Physics-Informed Neural Networks for Plasma Physics',
    description:
      'Developing PINNs to solve the relativistic Fokker-Planck equation for modeling runaway electron dynamics in fusion plasmas. Utilizes PyTorch and HiPerGator HPC for large-scale training.',
    tags: ['Python', 'PyTorch', 'HPC', 'Physics', 'Deep Learning'],
    github: null,
    external: null,
    featured: true,
  },
  {
    title: 'HardlyHard',
    description:
      'A project focused on converting difficult-to-understand research into simple, actionable, and teachable information. Making complex scientific concepts accessible.',
    tags: ['Research', 'Education', 'Science Communication'],
    github: 'https://github.com/dannySchantz/HardlyHard',
    external: null,
    featured: true,
  },
  {
    title: 'Dreicer Generation Modeling',
    description:
      'Deep learning workflows designed to accurately model Dreicer generation mechanisms and predict primary runaway electron formation rates in plasma systems.',
    tags: ['Machine Learning', 'Plasma Physics', 'Numerical Methods'],
    github: null,
    external: null,
    featured: true,
  },
  {
    title: 'Full-Stack Web Application',
    description:
      'A complete web application with separate frontend and backend repositories, demonstrating full-stack development capabilities.',
    tags: ['JavaScript', 'React', 'Node.js', 'Full-Stack'],
    github: 'https://github.com/dannySchantz/final-project-frontend',
    external: null,
    featured: false,
  },
  {
    title: 'Personal Portfolio Website',
    description:
      'This very website! Built with Next.js, TypeScript, and Tailwind CSS. Features a modern, responsive design with smooth animations.',
    tags: ['Next.js', 'TypeScript', 'Tailwind CSS', 'React'],
    github: 'https://github.com/dannySchantz/personal-website',
    external: null,
    featured: false,
  },
  {
    title: 'Interactive Coding Challenges',
    description:
      'Collection of coding challenges and exercises from NEXT Academy Coding Bootcamp, showcasing problem-solving skills and JavaScript proficiency.',
    tags: ['JavaScript', 'Problem Solving', 'Algorithms'],
    github: 'https://github.com/dannySchantz/challenge-elusive-button-javascript',
    external: null,
    featured: false,
  },
];

function ProjectCard({
  project,
  featured = false,
}: {
  project: typeof projects[0];
  featured?: boolean;
}) {
  return (
    <div
      className={`glass rounded-xl overflow-hidden group hover:bg-white/10 transition-all duration-300 ${
        featured ? 'md:col-span-2 lg:col-span-1' : ''
      }`}
    >
      <div className="p-6 h-full flex flex-col">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <Folder className="w-10 h-10 text-primary-400" />
          <div className="flex items-center gap-3">
            {project.github && (
              <a
                href={project.github}
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="GitHub Repository"
              >
                <Github className="w-5 h-5" />
              </a>
            )}
            {project.external && (
              <a
                href={project.external}
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Live Demo"
              >
                <ExternalLink className="w-5 h-5" />
              </a>
            )}
          </div>
        </div>

        {/* Content */}
        <h3 className="text-white font-semibold text-lg mb-3 group-hover:text-primary-400 transition-colors">
          {project.title}
        </h3>
        <p className="text-gray-400 text-sm flex-grow mb-4">{project.description}</p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mt-auto">
          {project.tags.map((tag) => (
            <span
              key={tag}
              className="text-xs font-mono text-gray-400 bg-white/5 px-2 py-1 rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function Projects() {
  const featuredProjects = projects.filter((p) => p.featured);
  const otherProjects = projects.filter((p) => !p.featured);

  return (
    <section id="projects" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
          Featured <span className="text-gradient">Projects</span>
        </h2>
        <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
          A selection of my research projects and personal work in computational physics and software development
        </p>

        {/* Featured Projects */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {featuredProjects.map((project, index) => (
            <ProjectCard key={index} project={project} featured />
          ))}
        </div>

        {/* Other Projects */}
        <h3 className="text-xl font-semibold text-white mb-8 text-center">
          Other Notable Projects
        </h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {otherProjects.map((project, index) => (
            <ProjectCard key={index} project={project} />
          ))}
        </div>

        {/* View More Link */}
        <div className="text-center mt-12">
          <a
            href="https://github.com/dannySchantz"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors"
          >
            View more on GitHub
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </section>
  );
}
