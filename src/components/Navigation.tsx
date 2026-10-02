'use client';

import { useEffect, useState } from 'react';
import { Menu, Moon, Sun, X } from 'lucide-react';
import { profile } from '@/data/profile';

const navItems = [
  { id: 'about', label: 'About' },
  { id: 'research', label: 'Research' },
  { id: 'projects', label: 'Projects' },
  { id: 'experience', label: 'Experience' },
  { id: 'skills', label: 'Skills' },
  { id: 'contact', label: 'Contact' },
];

export default function Navigation() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState('');
  const [theme, setTheme] = useState<'light' | 'dark' | null>(null);

  useEffect(() => {
    setTheme(document.documentElement.classList.contains('dark') ? 'dark' : 'light');
  }, []);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    const sections = navItems
      .map((item) => document.getElementById(item.id))
      .filter((el): el is HTMLElement => el !== null);

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) setActive(entry.target.id);
        }
      },
      { rootMargin: '-35% 0px -60% 0px', threshold: 0 },
    );

    sections.forEach((section) => observer.observe(section));
    return () => observer.disconnect();
  }, []);

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    document.documentElement.classList.toggle('dark', next === 'dark');
    try {
      localStorage.setItem('theme', next);
    } catch {
      /* storage unavailable */
    }
    setTheme(next);
  };

  const linkClass = (id: string) =>
    `font-mono text-xs uppercase tracking-[0.14em] transition-colors ${
      active === id ? 'text-accent' : 'text-muted hover:text-ink'
    }`;

  return (
    <header
      className={`no-print sticky top-0 z-40 border-b bg-paper transition-colors ${
        scrolled || open ? 'border-line' : 'border-transparent'
      }`}
    >
      <nav
        className="mx-auto flex h-14 max-w-5xl items-center justify-between px-6"
        aria-label="Primary"
      >
        <a href="/" className="font-serif text-[17px] font-semibold tracking-tight">
          Danny Schantz
        </a>

        <ul className="hidden items-center gap-6 md:flex">
          {navItems.map((item) => (
            <li key={item.id}>
              <a href={`/#${item.id}`} className={linkClass(item.id)}>
                {item.label}
              </a>
            </li>
          ))}
          <li>
            <a
              href={profile.resumeUrl}
              className="font-mono text-xs uppercase tracking-[0.14em] text-accent hover:text-accent-strong"
            >
              CV&nbsp;&darr;
            </a>
          </li>
        </ul>

        <div className="flex items-center gap-1">
          {theme === null ? (
            <span className="block h-8 w-8" aria-hidden="true" />
          ) : (
            <button
              type="button"
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
              className="flex h-8 w-8 items-center justify-center rounded-full text-muted transition-colors hover:text-ink"
            >
              {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
            </button>
          )}
          <button
            type="button"
            onClick={() => setOpen(!open)}
            aria-expanded={open}
            aria-controls="mobile-menu"
            aria-label={open ? 'Close menu' : 'Open menu'}
            className="flex h-8 w-8 items-center justify-center text-muted transition-colors hover:text-ink md:hidden"
          >
            {open ? <X size={17} /> : <Menu size={17} />}
          </button>
        </div>
      </nav>

      {open && (
        <div id="mobile-menu" className="border-t border-line bg-paper md:hidden">
          <ul className="mx-auto max-w-5xl px-6 py-4">
            {navItems.map((item) => (
              <li key={item.id}>
                <a
                  href={`/#${item.id}`}
                  onClick={() => setOpen(false)}
                  className="block border-b border-line py-3 font-mono text-xs uppercase tracking-[0.14em] text-muted last:border-b-0 hover:text-ink"
                >
                  {item.label}
                </a>
              </li>
            ))}
            <li>
              <a
                href={profile.resumeUrl}
                onClick={() => setOpen(false)}
                className="block py-3 font-mono text-xs uppercase tracking-[0.14em] text-accent"
              >
                CV (PDF)
              </a>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
