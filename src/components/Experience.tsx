'use client';

import { Briefcase, GraduationCap } from 'lucide-react';

const experiences = [
  {
    type: 'work',
    title: 'Research Assistant',
    organization: 'Plasma and Fusion Group, University of Florida',
    period: 'Present',
    description: [
      'Develop Physics-Informed Neural Networks (PINNs) to solve the relativistic Fokker-Planck equation',
      'Utilize UF HiPerGator HPC resources for large-scale neural network training',
      'Design deep learning workflows in Python and PyTorch for plasma physics simulations',
      'Model Dreicer generation mechanisms and predict primary runaway electron formation rates',
    ],
  },
];

const education = [
  {
    type: 'education',
    title: 'Master of Science in Nuclear Engineering Sciences',
    organization: 'University of Florida',
    period: 'Current',
    description: [
      'Focus on plasma physics and computational methods',
      'Research in Physics-Informed Neural Networks for fusion applications',
      'Coursework in advanced nuclear engineering and machine learning',
    ],
  },
  {
    type: 'education',
    title: 'Bachelor of Science in Chemical Engineering',
    organization: 'University',
    period: 'Completed',
    description: [
      'Strong foundation in thermodynamics and transport phenomena',
      'Developed analytical and problem-solving skills',
      'Background in mathematical modeling and computational methods',
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
            <li key={idx} className="flex items-start gap-3 text-gray-400">
              <span className="text-primary-500 mt-1.5">▹</span>
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
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
          Experience & <span className="text-gradient">Education</span>
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
