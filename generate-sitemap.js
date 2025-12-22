/**
 * Simple sitemap generator for SND movie slugs.
 * Usage (PowerShell): node generate-sitemap.js > sitemap.xml
 * Ensure you have a movies JSON export with id,title in movies.json OR adapt fetchMovies().
 */
const fs = require('fs');

// CONFIG: set your production domain and optional base path
const DOMAIN = process.env.SND_DOMAIN || 'https://YOUR_DOMAIN'; // no trailing slash
const BASE_PATH = process.env.SND_BASE_PATH || ''; // e.g. '' or '/app'
const FORCE_HASH_ROUTING = false; // keep consistent with client if needed

function slugify(str) {
  return String(str || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/--+/g, '-');
}

function loadMovies() {
  try {
    const raw = fs.readFileSync('movies.json', 'utf-8');
    const data = JSON.parse(raw);
    if (Array.isArray(data)) return data;
    if (Array.isArray(data.movies)) return data.movies;
    return [];
  } catch (e) {
    console.warn('No movies.json found; using empty list.');
    return [];
  }
}

function buildUrl(movie) {
  const slug = slugify(movie.title) || movie.id;
  if (!FORCE_HASH_ROUTING) {
    return DOMAIN + (BASE_PATH ? BASE_PATH.replace(/\/$/, '') : '') + '/' + encodeURIComponent(slug);
  }
  return DOMAIN + (BASE_PATH ? BASE_PATH.replace(/\/$/, '') : '') + '/#' + encodeURIComponent(slug);
}

function generate() {
  const movies = loadMovies();
  const urls = movies.map(m => ({ loc: buildUrl(m), lastmod: new Date().toISOString().split('T')[0] }));
  const xmlParts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  ];
  urls.forEach(u => {
    xmlParts.push('  <url>');
    xmlParts.push(`    <loc>${u.loc}</loc>`);
    xmlParts.push(`    <lastmod>${u.lastmod}</lastmod>`);
    xmlParts.push('    <changefreq>weekly</changefreq>');
    xmlParts.push('    <priority>0.7</priority>');
    xmlParts.push('  </url>');
  });
  xmlParts.push('</urlset>');
  return xmlParts.join('\n');
}

if (require.main === module) {
  process.stdout.write(generate());
}

module.exports = { generate };