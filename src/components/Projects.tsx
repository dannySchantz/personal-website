'use client';

import { useRouter } from 'next/navigation';
import { ExternalLink, Github, Folder, ArrowRight } from 'lucide-react';

type Project = {
  title: string;
  description: string;
  tags: string[];
  github: string | null;
  external: string | null;
  href: string | null;
  featured: boolean;
};

const projects: Project[] = [
  {
    title: '1-D Monte Carlo Neutron Transport',
    description:
      'A Python Monte Carlo solver for one-dimensional neutron transport. Tracks particle histories to estimate flux, transmission, and reflection in slab geometries.',
    tags: ['Python', 'Monte Carlo', 'Neutron Transport', 'NumPy'],
    github: null,
    external: null,
    href: '/1dMC',
    featured: true,
  },
  {
    title: 'Physics-Informed Neural Networks for Plasma Physics',
    description:
      'Developing PINNs to solve the relativistic Fokker-Planck equation for modeling runaway electron dynamics in fusion plasmas. Utilizes PyTorch and HiPerGator HPC for large-scale training.',
    tags: ['Python', 'PyTorch', 'HPC', 'Physics', 'Deep Learning'],
    github: null,
    external: null,
    href: null,
    featured: true,
  },
  {
    title: 'HardlyHard',
    description:
      'A project focused on converting difficult-to-understand research into simple, actionable, and teachable information. Making complex scientific concepts accessible.',
    tags: ['Research', 'Education', 'Science Communication'],
    github: 'https://github.com/dannySchantz/HardlyHard',
    external: null,
    href: null,
    featured: true,
  },
  {
    title: 'Dreicer Generation Modeling',
    description:
      'Deep learning workflows designed to accurately model Dreicer generation mechanisms and predict primary runaway electron formation rates in plasma systems.',
    tags: ['Machine Learning', 'Plasma Physics', 'Numerical Methods'],
    github: null,
    external: null,
    href: null,
    featured: false,
  },
  {
    title: 'Full-Stack Web Application',
    description:
      'A complete web application with separate frontend and backend repositories, demonstrating full-stack development capabilities.',
    tags: ['JavaScript', 'React', 'Node.js', 'Full-Stack'],
    github: 'https://github.com/dannySchantz/final-project-frontend',
    external: null,
    href: null,
    featured: false,
  },
  {
    title: 'Personal Portfolio Website',
    description:
      'This very website! Built with Next.js, TypeScript, and Tailwind CSS. Features a modern, responsive design with smooth animations.',
    tags: ['Next.js', 'TypeScript', 'Tailwind CSS', 'React'],
    github: 'https://github.com/dannySchantz/personal-website',
    external: null,
    href: null,
    featured: false,
  },
  {
    title: 'Interactive Coding Challenges',
    description:
      'Collection of coding challenges and exercises from NEXT Academy Coding Bootcamp, showcasing problem-solving skills and JavaScript proficiency.',
    tags: ['JavaScript', 'Problem Solving', 'Algorithms'],
    github: 'https://github.com/dannySchantz/challenge-elusive-button-javascript',
    external: null,
    href: null,
    featured: false,
  },
];

function ProjectCard({
  project,
  featured = false,
}: {
  project: Project;
  featured?: boolean;
}) {
  const router = useRouter();

  const handleCardActivate = () => {
    if (project.href) {
      router.push(project.href);
    }
  };

  return (
    <div
      role={project.href ? 'link' : undefined}
      tabIndex={project.href ? 0 : undefined}
      onClick={project.href ? handleCardActivate : undefined}
      onKeyDown={
        project.href
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleCardActivate();
              }
            }
          : undefined
      }
      className={`glass rounded-xl overflow-hidden group hover:bg-white/10 transition-all duration-300 h-full focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 ${
        featured ? 'md:col-span-2 lg:col-span-1' : ''
      } ${project.href ? 'cursor-pointer' : ''}`}
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
                onClick={(e) => e.stopPropagation()}
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
                onClick={(e) => e.stopPropagation()}
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

        {project.href && (
          <div className="mt-4 flex items-center gap-2 text-sm text-primary-400 group-hover:text-primary-300 transition-colors">
            Learn more
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </div>
        )}
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
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gradient mb-4">
          Featured Projects
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
