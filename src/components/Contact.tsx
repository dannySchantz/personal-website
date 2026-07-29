'use client';

import { Mail, MapPin, Github, Linkedin, Send } from 'lucide-react';

export default function Contact() {
  return (
    <section id="contact" className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
          Get In <span className="text-gradient">Touch</span>
        </h2>
        <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
          I&apos;m always open to discussing research opportunities, collaborations,
          or just having a conversation about physics and machine learning.
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Contact Info */}
          <div className="space-y-6">
            <div className="glass rounded-xl p-6">
              <h3 className="text-white font-semibold text-lg mb-6">Contact Information</h3>
              
              <div className="space-y-4">
                <a
                  href="mailto:dannyschantz1@icloud.com"
                  className="flex items-center gap-4 text-gray-400 hover:text-primary-400 transition-colors group"
                >
                  <div className="w-10 h-10 rounded-lg bg-primary-500/10 flex items-center justify-center group-hover:bg-primary-500/20 transition-colors">
                    <Mail className="w-5 h-5 text-primary-400" />
                  </div>
                  <span>dannyschantz1@icloud.com</span>
                </a>
                
                <div className="flex items-center gap-4 text-gray-400">
                  <div className="w-10 h-10 rounded-lg bg-primary-500/10 flex items-center justify-center">
                    <MapPin className="w-5 h-5 text-primary-400" />
                  </div>
                  <span>Gainesville, Florida</span>
                </div>
              </div>

              <div className="mt-8 pt-6 border-t border-white/10">
                <p className="text-gray-400 text-sm mb-4">Connect with me</p>
                <div className="flex gap-4">
                  <a
                    href="https://github.com/dannySchantz"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 glass rounded-lg flex items-center justify-center hover:bg-white/10 transition-colors group"
                    aria-label="GitHub"
                  >
                    <Github className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
                  </a>
                  <a
                    href="https://linkedin.com/in/dannyschantz"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 glass rounded-lg flex items-center justify-center hover:bg-white/10 transition-colors group"
                    aria-label="LinkedIn"
                  >
                    <Linkedin className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="glass rounded-xl p-6">
            <h3 className="text-white font-semibold text-lg mb-6">Send a Message</h3>
            
            <form
              action="https://formspree.io/f/your-form-id"
              method="POST"
              className="space-y-4"
            >
              <div>
                <label htmlFor="name" className="block text-sm text-gray-400 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  required
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 transition-colors"
                  placeholder="Your name"
                />
              </div>
              
              <div>
                <label htmlFor="email" className="block text-sm text-gray-400 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 transition-colors"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div>
                <label htmlFor="message" className="block text-sm text-gray-400 mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  required
                  rows={4}
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 transition-colors resize-none"
                  placeholder="Your message..."
                />
              </div>
              
              <button
                type="submit"
                className="w-full px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium rounded-lg hover:opacity-90 transition-all duration-300 flex items-center justify-center gap-2 group"
              >
                Send Message
                <Send className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </form>
            
            <p className="text-gray-500 text-xs mt-4 text-center">
              Or email me directly at dannyschantz1@icloud.com
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
