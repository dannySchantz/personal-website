/**
 * All of the site's content lives here so updates happen in one place.
 * Facts, dates, and links, no styling.
 */

export const profile = {
  name: 'Danny Schantz',
  role: 'Nuclear engineering graduate student at the University of Florida, building physics-informed neural networks to model runaway electrons in fusion plasmas.',
  location: 'Gainesville, Florida',
  email: 'danny.schantz@ufl.edu',
  github: 'https://github.com/dannySchantz',
  linkedin: 'https://linkedin.com/in/dannyschantz',
  resumeUrl: '/DanielSchantz_Resume.pdf',
  lastUpdated: 'October 2026',
};

export const about = {
  paragraphs: [
    'I\u2019m a graduate student in nuclear engineering at the University of Florida, working in the Plasma and Fusion Group under the supervision of Dr. McDevitt. My research sits at the intersection of plasma physics and machine learning: I build physics-informed neural networks (PINNs) that learn to solve the kinetic equations governing fusion plasmas.',
    'The current focus is the relativistic Fokker\u2013Planck equation, which describes how runaway-electron populations form and evolve in tokamak plasmas. Within a single PINN framework I model Dreicer generation and primary formation rates, training at scale on UF\u2019s HiPerGator cluster with PyTorch.',
    'Before UF I studied chemical engineering at Calvin University and spent a year and a half doing materials R&D at Mackinac Technology, on a DOE-funded liquid silicone rubber project. Alongside my research I train toward reactor-operator licensure at the UF Training Reactor (UFTR).',
  ],
};

export const updates = [
  {
    date: 'Sep 2025',
    text: 'Joined the UF Training Reactor staff and began NRC-certified reactor-operator training.',
  },
  {
    date: 'Aug 2025',
    text: 'Started the M.S. in Nuclear Engineering Sciences at UF; joined the Plasma and Fusion Group.',
  },
  {
    date: 'May 2025',
    text: 'Graduated from Calvin University with a B.S. in Chemical Engineering.',
  },
  {
    date: 'Feb 2025',
    text: 'Began an Open Avenues research project simulating quantum systems in Python.',
  },
  {
    date: 'Jan 2024',
    text: 'Joined Mackinac Technology as a Materials Science R&D intern.',
  },
];

export const research = {
  lead: 'My thesis develops physics-informed neural networks (PINNs) for kinetic plasma physics: training networks that respect the governing equations, then using them where classical solvers get expensive.',
  paragraphs: [
    'Runaway electrons are relativistic particles that can form during tokamak disruptions, and they threaten plasma-facing components, so predicting their formation matters for present and future devices, including spherical tokamaks. Their dynamics are governed by the relativistic Fokker\u2013Planck equation, which couples electric-field acceleration, collisional slowing-down, and pitch-angle scattering.',
    'In the Plasma and Fusion Group I am building a unified PINN framework for Dreicer generation and primary runaway formation rates. The models are trained on UF\u2019s HiPerGator cluster using PyTorch, with deep-learning workflows built around Python and HPC job scheduling.',
  ],
  interests: [
    'Fusion plasma physics',
    'Physics-informed machine learning',
    'Computational neutron transport',
    'Reactor operations',
  ],
};

export type Project = {
  kind: string;
  title: string;
  description: string;
  stack: string;
  github?: string;
  href?: string;
};

export const projects: Project[] = [
  {
    kind: 'Thesis',
    title: 'Physics-Informed Neural Networks for Runaway Electrons',
    description:
      'PINNs that solve the relativistic Fokker\u2013Planck equation to model runaway-electron dynamics in fusion plasmas: Dreicer generation and primary formation rates in a unified framework, trained at scale on UF HiPerGator.',
    stack: 'Python \u00b7 PyTorch \u00b7 HiPerGator HPC',
  },
  {
    kind: 'Reactor physics',
    title: '1-D Fission Reactor Monte Carlo',
    description:
      'Multigroup Monte Carlo neutron transport for 1-D UO\u2082/MOX assembly slabs, with a finite-difference diffusion reference solver, flux and current tallies, convergence studies, and optional Numba acceleration.',
    stack: 'Python \u00b7 NumPy \u00b7 Numba \u00b7 Matplotlib',
    github: 'https://github.com/dannySchantz/1-D-Fission-Reactor-MC',
    href: '/1dMC',
  },
  {
    kind: 'Research',
    title: 'Quantum Physics Simulation, Open Avenues',
    description:
      'Modeled atomic behavior in Python, simulating wave functions and energy states to explore fundamental quantum mechanical principles.',
    stack: 'Python',
  },
  {
    kind: 'Research',
    title: 'Sustainable Ferrovanadium Production, Open Avenues',
    description:
      'Studied process optimization and environmental impact of ferrovanadium production with a mentor, culminating in a 30-minute presentation to company executives at Phoenix Tailings, Inc.',
    stack: 'Process optimization',
  },
  {
    kind: 'Outreach',
    title: 'HardlyHard',
    description:
      'Turning difficult-to-understand research into simple, actionable, teachable material and making complex scientific concepts accessible.',
    stack: 'Science communication',
    github: 'https://github.com/dannySchantz/HardlyHard',
  },
  {
    kind: 'Software',
    title: 'Full-Stack Web Application',
    description:
      'A complete web application with separate frontend and backend repositories, built to learn the whole request lifecycle.',
    stack: 'JavaScript \u00b7 React \u00b7 Node.js',
    github: 'https://github.com/dannySchantz/final-project-frontend',
  },
  {
    kind: 'This site',
    title: 'Personal Website',
    description:
      'The page you are reading. Typeset like the CV it doubles as; the source is open.',
    stack: 'Next.js \u00b7 TypeScript \u00b7 Tailwind CSS',
    github: 'https://github.com/dannySchantz/personal-website',
  },
  {
    kind: 'Exercises',
    title: 'Interactive Coding Challenges',
    description:
      'Coding challenges and exercises from the NEXT Academy bootcamp, kept around as problem-solving practice.',
    stack: 'JavaScript \u00b7 Algorithms',
    github: 'https://github.com/dannySchantz/challenge-elusive-button-javascript',
  },
];

export type Entry = {
  period: string;
  title: string;
  organization: string;
  details?: string[];
  bullets?: string[];
};

export const education: Entry[] = [
  {
    period: 'Aug 2025 \u2013 May 2027',
    title: 'M.S., Nuclear Engineering Sciences (thesis track)',
    organization: 'University of Florida',
    details: [
      'GPA 4.0. Thesis research on runaway-electron generation in spherical tokamak plasmas under Dr. McDevitt.',
      'Focus: physics-informed neural networks for fusion applications.',
    ],
  },
  {
    period: 'Aug 2021 \u2013 May 2025',
    title: 'B.S. in Engineering, Chemical Engineering',
    organization: 'Calvin University',
    details: [
      'GPA 3.47. Coursework in process design, thermodynamics, transport phenomena, unit operations, and reaction engineering.',
      'Served as a student supervisor, mentoring peers.',
    ],
  },
];

export const appointments: Entry[] = [
  {
    period: 'Aug 2025 \u2013 present',
    title: 'Graduate Research Assistant',
    organization: 'Plasma and Fusion Group, University of Florida',
    bullets: [
      'Develop physics-informed neural networks that solve plasma-physics partial differential equations, trained on UF HiPerGator HPC resources.',
      'Design deep-learning workflows in Python and PyTorch to model plasma dynamics in tokamak fusion devices, with a focus on relativistic electron formation and electron distribution evolution.',
      'Write Matplotlib scripts for data visualization and validation of neural network output.',
    ],
  },
  {
    period: 'Sep 2025 \u2013 present',
    title: 'Student Assistant, Reactor Operations',
    organization: 'University of Florida Training Reactor (UFTR)',
    bullets: [
      'Completing the NRC-certified training curriculum in preparation for Reactor Operator licensure.',
      'Studying reactor systems: radiation detection, thermal-hydraulics, instrumentation and controls, reactor design, and standard and emergency operating procedures.',
      'Assist with daily reactor operations as a qualified second person, execute experimental data collection, and perform instrumentation maintenance and repair.',
    ],
  },
  {
    period: 'Jan 2024 \u2013 Aug 2025',
    title: 'Materials Science R&D Intern',
    organization: 'Mackinac Technology Company',
    bullets: [
      'Led experimental design and process optimization for a DOE-funded liquid silicone rubber window project, focused on enhancing tensile strength while maintaining high optical clarity.',
      'Eliminated 99.6% of bubble formation while increasing surface uniformity by 92%.',
      'Conducted literature reviews on LSR surface and structural modification and contributed to SBIR grant writing for ongoing research funding.',
    ],
  },
  {
    period: 'Jan 2023 \u2013 May 2025',
    title: 'Engineering Grader',
    organization: 'Calvin University',
    bullets: [
      'Evaluated coursework and provided academic support for three engineering courses.',
      'Guided students in identifying and correcting errors, fostering skill development and improved academic performance.',
    ],
  },
];

export const skills = [
  {
    category: 'Languages',
    items: 'Python (PyTorch, NumPy, SciPy, Matplotlib, JAX), JavaScript, TypeScript, HTML/CSS, MATLAB',
  },
  {
    category: 'Machine learning',
    items:
      'Physics-informed neural networks, deep learning, large-scale training on HPC',
  },
  {
    category: 'Scientific computing',
    items:
      'Numerical methods, Monte Carlo methods, finite-difference solvers, parallel computing, UF HiPerGator',
  },
  {
    category: 'Domain',
    items:
      'Nuclear engineering, plasma physics, runaway-electron dynamics, chemical engineering, thermodynamics, transport phenomena',
  },
  {
    category: 'HPC & tools',
    items: 'Linux (Bash), Slurm, Git/GitHub, Docker, Jupyter, LaTeX',
  },
  {
    category: 'Engineering software',
    items: 'AutoCAD, Inventor, UNISIM',
  },
  {
    category: 'Communication',
    items:
      'Technical writing, literature review, SBIR grant writing, presentation, mentoring',
  },
];
