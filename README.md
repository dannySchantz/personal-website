# Danny Schantz - Personal Portfolio

A modern, responsive personal portfolio website built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Modern Design**: Clean, dark-themed interface with gradient accents and glassmorphism effects
- **Fully Responsive**: Optimized for all screen sizes from mobile to desktop
- **Smooth Animations**: Subtle animations and transitions for enhanced user experience
- **SEO Optimized**: Proper meta tags and semantic HTML structure
- **Static Export**: Can be deployed to any static hosting service
- **Fast Performance**: Optimized for Core Web Vitals

## Sections

- **Hero**: Introduction with social links and call-to-action
- **About**: Personal bio and research highlights
- **Experience**: Work experience and education timeline
- **Projects**: Featured research projects and personal work
- **Skills**: Technical skills and tools organized by category
- **Contact**: Contact form and social links

## Tech Stack

- [Next.js 14](https://nextjs.org/) - React framework with App Router
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Lucide React](https://lucide.dev/) - Beautiful, consistent icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
# Create production build
npm run build

# Start production server (for SSR)
npm run start

# Or export as static site
# The static files will be in the 'out' directory
```

## Deployment

This site is configured for static export and can be deployed to:

- **GitHub Pages**: Push to a `gh-pages` branch
- **Vercel**: Connect your repository for automatic deployments
- **Netlify**: Drag and drop the `out` folder or connect your repo
- **Any static host**: Upload the contents of `out` folder

## Customization

### Personal Information

Update your personal information in the component files:

- `src/components/Hero.tsx` - Name, title, intro text
- `src/components/About.tsx` - Bio and highlights
- `src/components/Experience.tsx` - Work and education history
- `src/components/Projects.tsx` - Project details and links
- `src/components/Skills.tsx` - Technical skills
- `src/components/Contact.tsx` - Contact information
- `src/app/layout.tsx` - SEO metadata

### Styling

- Colors and theme: `tailwind.config.ts`
- Global styles: `src/app/globals.css`

## License

MIT License - feel free to use this as a template for your own portfolio!

## Contact

- **Email**: danny.schantz@ufl.edu
- **LinkedIn**: [linkedin.com/in/dannyschantz](https://linkedin.com/in/dannyschantz)
- **GitHub**: [github.com/dannySchantz](https://github.com/dannySchantz)
