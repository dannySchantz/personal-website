'use client';

import { Github, Linkedin, Mail, ChevronDown, FileText } from 'lucide-react';

export default function Hero() {
  return (
    <section className="min-h-screen flex flex-col justify-center items-center relative px-6 pt-20">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-primary-500/5 to-accent-500/5 rounded-full blur-3xl" />
      </div>

      <div className="max-w-4xl mx-auto text-center relative z-10 animate-fade-in">
        <p className="text-primary-400 font-mono text-sm md:text-base mb-4 tracking-wider">
          Hello, I&apos;m
        </p>
        
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6">
          <span className="text-white">Danny </span>
          <span className="text-gradient">Schantz</span>
        </h1>
        
        <h2 className="text-xl md:text-2xl lg:text-3xl text-gray-400 mb-8 font-light">
          Nuclear Engineering Researcher &{' '}
          <span className="text-white">Machine Learning Developer</span>
        </h2>
        
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          Graduate student at the{' '}
          <span className="text-primary-400">University of Florida</span>,
          developing Physics-Informed Neural Networks to solve complex plasma physics problems.
        </p>

        {/* Social Links */}
        <div className="flex items-center justify-center gap-6 mb-12">
          <a
            href="https://github.com/dannySchantz"
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 glass rounded-full hover:bg-white/10 transition-all duration-300 hover:scale-110 group"
            aria-label="GitHub Profile"
          >
            <Github className="w-6 h-6 text-gray-400 group-hover:text-white transition-colors" />
          </a>
          <a
            href="https://linkedin.com/in/dannyschantz"
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 glass rounded-full hover:bg-white/10 transition-all duration-300 hover:scale-110 group"
            aria-label="LinkedIn Profile"
          >
            <Linkedin className="w-6 h-6 text-gray-400 group-hover:text-white transition-colors" />
          </a>
          <a
            href="mailto:dannyschantz1@icloud.com"
            className="p-3 glass rounded-full hover:bg-white/10 transition-all duration-300 hover:scale-110 group"
            aria-label="Email"
          >
            <Mail className="w-6 h-6 text-gray-400 group-hover:text-white transition-colors" />
          </a>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="#projects"
            className="px-8 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium rounded-lg hover:opacity-90 transition-all duration-300 hover:scale-105 shadow-lg shadow-primary-500/25"
          >
            View My Work
          </a>
          <a
            href="/DanielSchantz_Resume.pdf"
            download
            className="px-8 py-3 glass text-white font-medium rounded-lg hover:bg-white/10 transition-all duration-300 flex items-center gap-2"
          >
            <FileText className="w-4 h-4" />
            Download Resume
          </a>
          <a
            href="#contact"
            className="px-8 py-3 glass text-white font-medium rounded-lg hover:bg-white/10 transition-all duration-300"
          >
            Get In Touch
          </a>
        </div>
      </div>

      {/* Scroll indicator */}
      <a
        href="#about"
        className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce"
        aria-label="Scroll to About section"
      >
        <ChevronDown className="w-8 h-8 text-gray-500" />
      </a>
    </section>
  );
}
