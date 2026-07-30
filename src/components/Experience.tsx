'use client';

import { Briefcase, GraduationCap } from 'lucide-react';

const experiences = [
  {
    type: 'work',
    title: 'Graduate Research Assistant',
    organization: 'Plasma and Fusion Group, University of Florida',
    period: 'Aug 2025 – Present',
    description: [
      'Developing Physics-Informed Neural Networks to solve plasma physics partial differential equations using UF HiPerGator HPC resources',
      'Designing deep learning workflows in Python and PyTorch to model plasma dynamics in tokamak fusion devices',
      'Focus on relativistic electron formation and electron distribution evolution',
    ],
  },
  {
    type: 'work',
    title: 'Student Assistant – Reactor Operations',
    organization: 'University of Florida Training Reactor (UFTR)',
    period: 'Sep 2025 – Present',
    description: [
      'Completing NRC-certified training curriculum in preparation for Reactor Operator licensure',
      'Acquiring knowledge of reactor systems including radiation detection, thermal-hydraulics, instrumentation and controls',
      'Assisting with daily reactor operations as a qualified second person and performing instrumentation maintenance',
    ],
  },
  {
    type: 'work',
    title: 'Materials Science R&D Intern',
    organization: 'Mackinac Technology Company',
    period: 'Jan 2024 – Aug 2025',
    description: [
      'Led experimental design and process optimization for a DOE-funded Liquid Silicone Rubber window project',
      'Eliminated 99.6% of bubble formation while increasing surface uniformity by 92%',
      'Conducted literature reviews and contributed to SBIR grant writing efforts for ongoing research funding',
    ],
  },
];

const education = [
  {
    type: 'education',
    title: 'Master of Science in Nuclear Engineering Sciences',
    organization: 'University of Florida',
    period: 'Aug 2025 – May 2027',
    description: [
      'Thesis Track with 4.0 GPA',
      'Research on runaway electron generation in spherical tokamak plasmas under Dr. McDevitt',
      'Focus on Physics-Informed Neural Networks for fusion applications',
    ],
  },
  {
    type: 'education',
    title: 'Bachelor of Science in Engineering (Chemical Engineering)',
    organization: 'Calvin University',
    period: 'Aug 2021 – May 2025',
    description: [
      'GPA: 3.47',
      'Strong foundation in process design, thermodynamics, and transport phenomena',
      'Coursework in unit operations, reaction engineering, and experimental laboratory methods',
      'Served as a student supervisor, mentoring peers and building leadership experience',
    ],
  },
];

function TimelineItem({
  item,
  isLast,
}: {
  item: typeof experiences[0];
  isLast: boolean;
}) {
  const Icon = item.type === 'work' ? Briefcase : GraduationCap;
  
  return (
    <div className="relative pl-8 pb-8">
      {/* Timeline line */}
      {!isLast && (
        <div className="absolute left-[11px] top-8 w-0.5 h-full bg-gradient-to-b from-primary-500/50 to-transparent" />
      )}
      
      {/* Timeline dot */}
      <div className="absolute left-0 top-0 w-6 h-6 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
        <Icon className="w-3 h-3 text-white" />
      </div>

      <div className="glass rounded-xl p-6 ml-4 hover:bg-white/10 transition-all duration-300">
        <div className="flex flex-wrap items-center gap-3 mb-2">
          <h3 className="text-white font-semibold text-lg">{item.title}</h3>
          <span className="px-3 py-1 text-xs font-medium bg-primary-500/20 text-primary-400 rounded-full">
            {item.period}
          </span>
        </div>
        
        <p className="text-primary-400 mb-4">{item.organization}</p>
        
        <ul className="space-y-2">
          {item.description.map((point, idx) => (
            <li
              key={idx}
              className="grid grid-cols-[1rem_minmax(0,1fr)] gap-x-3 text-gray-400 leading-relaxed"
            >
              <span
                className="text-primary-500 text-center leading-relaxed select-none"
                aria-hidden="true"
              >
                ▹
              </span>
              <span>{point}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default function Experience() {
  return (
    <section id="experience" className="py-24 px-6 relative">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary-950/20 to-transparent pointer-events-none" />
      
      <div className="max-w-4xl mx-auto relative">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gradient mb-4">
          Experience & Education
        </h2>
        <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
          My academic and professional journey in nuclear engineering and computational research
        </p>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Work Experience */}
          <div>
            <h3 className="flex items-center gap-2 text-xl font-semibold text-white mb-8">
              <Briefcase className="w-5 h-5 text-primary-400" />
              Work Experience
            </h3>
            <div>
              {experiences.map((exp, index) => (
                <TimelineItem
                  key={index}
                  item={exp}
                  isLast={index === experiences.length - 1}
                />
              ))}
            </div>
          </div>

          {/* Education */}
          <div>
            <h3 className="flex items-center gap-2 text-xl font-semibold text-white mb-8">
              <GraduationCap className="w-5 h-5 text-primary-400" />
              Education
            </h3>
            <div>
              {education.map((edu, index) => (
                <TimelineItem
                  key={index}
                  item={edu}
                  isLast={index === education.length - 1}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
