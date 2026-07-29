import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Danny Schantz | Nuclear Engineering Researcher & Developer',
  description: 'Personal portfolio of Danny Schantz - Nuclear Engineering Graduate Student at University of Florida, specializing in Physics-Informed Neural Networks and Plasma Physics.',
  keywords: ['Danny Schantz', 'Nuclear Engineering', 'Machine Learning', 'Physics-Informed Neural Networks', 'Plasma Physics', 'University of Florida'],
  authors: [{ name: 'Danny Schantz' }],
  openGraph: {
    title: 'Danny Schantz | Nuclear Engineering Researcher & Developer',
    description: 'Personal portfolio of Danny Schantz - Nuclear Engineering Graduate Student at University of Florida.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
