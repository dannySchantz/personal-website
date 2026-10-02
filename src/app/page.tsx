import Navigation from '@/components/Navigation';
import Masthead from '@/components/Masthead';
import About from '@/components/About';
import Research from '@/components/Research';
import Projects from '@/components/Projects';
import Experience from '@/components/Experience';
import Skills from '@/components/Skills';
import Contact from '@/components/Contact';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <>
      <Navigation />
      <main id="main" tabIndex={-1}>
        <Masthead />
        <About />
        <Research />
        <Projects />
        <Experience />
        <Skills />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
