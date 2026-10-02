import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://dannyschantz.com',
      lastModified: new Date('2026-10-02'),
      changeFrequency: 'monthly',
      priority: 1,
    },
    {
      url: 'https://dannyschantz.com/1dMC',
      lastModified: new Date('2026-10-02'),
      changeFrequency: 'yearly',
      priority: 0.7,
    },
  ];
}
