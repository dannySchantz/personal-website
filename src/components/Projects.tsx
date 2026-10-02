import Section from './Section';
import { projects } from '@/data/profile';
import type { Project } from '@/data/profile';

function ProjectLinks({ project }: { project: Project }) {
  return (
    <p className="mt-3 flex flex-wrap items-baseline gap-x-5 gap-y-1 font-mono text-xs">
      {project.href && (
        <a href={project.href} className="prose-link">
          Details
        </a>
      )}
      {project.github && (
        <a
          href={project.github}
          target="_blank"
          rel="noopener noreferrer"
          className="prose-link"
        >
          GitHub <span aria-hidden="true">&nearr;</span>
        </a>
      )}
      <span className="text-faint">{project.stack}</span>
    </p>
  );
}

export default function Projects() {
  return (
    <Section id="projects" label="Projects">
      <p className="max-w-measure text-[17px] leading-relaxed text-ink-soft">
        A selection of research, coursework, and side projects.
      </p>

      <ul className="mt-8 divide-y divide-line border-y border-line">
        {projects.map((project) => (
          <li
            key={project.title}
            data-print-avoid-break
            className="grid gap-x-8 gap-y-1 py-7 md:grid-cols-[8rem_minmax(0,1fr)]"
          >
            <span className="pt-1 font-mono text-xs text-faint md:text-right">
              {project.kind}
            </span>
            <div>
              <h3 className="text-xl font-semibold leading-snug">
                {project.href ? (
                  <a href={project.href} className="prose-link">
                    {project.title}
                  </a>
                ) : (
                  project.title
                )}
              </h3>
              <p className="mt-2 max-w-measure text-[15px] leading-relaxed text-ink-soft">
                {project.description}
              </p>
              <ProjectLinks project={project} />
            </div>
          </li>
        ))}
      </ul>

      <p className="mt-8 font-mono text-xs text-muted">
        More on{' '}
        <a
          href="https://github.com/dannySchantz"
          target="_blank"
          rel="noopener noreferrer"
          className="prose-link"
        >
          GitHub
        </a>
        .
      </p>
    </Section>
  );
}
