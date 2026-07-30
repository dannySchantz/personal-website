'use client';

import { Github, Linkedin, Mail, ChevronDown, FileText } from 'lucide-react';

export default function Hero() {
  return (
    <section className="relative flex min-h-[100svh] flex-col items-center justify-start px-5 pb-10 pt-28 sm:px-6 sm:pb-16 md:justify-center md:pt-24">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-primary-500/5 to-accent-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto w-full max-w-4xl animate-fade-in text-center">
        <p className="mb-2 font-mono text-sm tracking-wider text-primary-400 sm:mb-4 md:text-base">
          Hello, I&apos;m
        </p>

        <h1 className="mb-3 text-4xl font-bold text-gradient sm:mb-6 md:text-6xl lg:text-7xl">
          Danny Schantz
        </h1>

        <h2 className="mb-4 text-lg font-light text-gray-300 sm:mb-8 sm:text-xl md:text-2xl lg:text-3xl">
          Nuclear Engineering Researcher & Machine Learning Developer
        </h2>

        <p className="mx-auto mb-6 max-w-2xl text-base leading-relaxed text-gray-400 sm:mb-10 sm:text-lg md:text-xl">
          Graduate student at the University of Florida, developing
          Physics-Informed Neural Networks to solve complex plasma physics
          problems.
        </p>

        {/* Social Links */}
        <div className="mb-8 flex items-center justify-center gap-4 sm:mb-12 sm:gap-6">
          <a
            href="https://github.com/dannySchantz"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full p-3 glass transition-all duration-300 hover:scale-110 hover:bg-white/10 group"
            aria-label="GitHub Profile"
          >
            <Github className="h-5 w-5 text-gray-400 transition-colors group-hover:text-white sm:h-6 sm:w-6" />
          </a>
          <a
            href="https://linkedin.com/in/dannyschantz"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full p-3 glass transition-all duration-300 hover:scale-110 hover:bg-white/10 group"
            aria-label="LinkedIn Profile"
          >
            <Linkedin className="h-5 w-5 text-gray-400 transition-colors group-hover:text-white sm:h-6 sm:w-6" />
          </a>
          <a
            href="mailto:dannyschantz1@icloud.com"
            className="rounded-full p-3 glass transition-all duration-300 hover:scale-110 hover:bg-white/10 group"
            aria-label="Email"
          >
            <Mail className="h-5 w-5 text-gray-400 transition-colors group-hover:text-white sm:h-6 sm:w-6" />
          </a>
        </div>

        {/* CTA Buttons */}
        <div className="flex w-full flex-col items-stretch justify-center gap-3 sm:w-auto sm:flex-row sm:items-center sm:gap-4">
          <a
            href="#projects"
            className="rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 px-6 py-3 text-center text-sm font-medium text-white shadow-lg shadow-primary-500/25 transition-all duration-300 hover:scale-105 hover:opacity-90 sm:px-8 sm:text-base"
          >
            View My Work
          </a>
          <a
            href="/DanielSchantz_Resume.pdf"
            download
            className="flex items-center justify-center gap-2 rounded-lg px-6 py-3 text-sm font-medium text-white glass transition-all duration-300 hover:bg-white/10 sm:px-8 sm:text-base"
          >
            <FileText className="h-4 w-4" />
            Download Resume
          </a>
          <a
            href="#contact"
            className="rounded-lg px-6 py-3 text-center text-sm font-medium text-white glass transition-all duration-300 hover:bg-white/10 sm:px-8 sm:text-base"
          >
            Get In Touch
          </a>
        </div>
      </div>

      {/* Scroll indicator — in flow on mobile so it never overlaps CTAs */}
      <a
        href="#about"
        className="relative z-10 mt-10 animate-bounce md:absolute md:bottom-8 md:left-1/2 md:mt-0 md:-translate-x-1/2"
        aria-label="Scroll to About section"
      >
        <ChevronDown className="h-7 w-7 text-gray-500 sm:h-8 sm:w-8" />
      </a>
    </section>
  );
}
