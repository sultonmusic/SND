/**
 * Script to generate individual HTML pages for each movie
 * Run this with Node.js: node generate-movie-pages.js
 */

const fs = require('fs');
const path = require('path');

// Read the movies data from Firebase or your data source
// For now, we'll create a template that works with the existing system

const templateHTML = `<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title id="page-title">{{MOVIE_TITLE}} ({{MOVIE_YEAR}}) - SND</title>
    <meta id="meta-description" name="description" content="{{MOVIE_DESCRIPTION}}">
    <meta id="meta-keywords" name="keywords" content="{{MOVIE_TITLE}}, {{MOVIE_ORIGINAL_TITLE}}, {{MOVIE_GENRE}}, смотреть онлайн, SND, фильм, кино">
    
    <!-- Open Graph / Facebook -->
    <meta id="og-type" property="og:type" content="video.movie">
    <meta id="og-url" property="og:url" content="{{PAGE_URL}}">
    <meta id="og-title" property="og:title" content="{{MOVIE_TITLE}} ({{MOVIE_YEAR}}) - SND">
    <meta id="og-description" property="og:description" content="{{MOVIE_DESCRIPTION}}">
    <meta id="og-image" property="og:image" content="{{MOVIE_POSTER}}">
    <meta property="og:site_name" content="SND - Streaming Network of Dreams">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta id="twitter-url" name="twitter:url" content="{{PAGE_URL}}">
    <meta id="twitter-title" name="twitter:title" content="{{MOVIE_TITLE}} ({{MOVIE_YEAR}}) - SND">
    <meta id="twitter-description" name="twitter:description" content="{{MOVIE_DESCRIPTION}}">
    <meta id="twitter-image" name="twitter:image" content="{{MOVIE_POSTER}}">
    
    <!-- Canonical URL -->
    <link id="canonical-url" rel="canonical" href="{{PAGE_URL}}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Movie",
        "name": "{{MOVIE_TITLE}}",
        "alternateName": "{{MOVIE_ORIGINAL_TITLE}}",
        "image": "{{MOVIE_POSTER}}",
        "description": "{{MOVIE_DESCRIPTION}}",
        "datePublished": "{{MOVIE_YEAR}}-01-01",
        "genre": "{{MOVIE_GENRE}}",
        "url": "{{PAGE_URL}}",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "{{MOVIE_RATING}}",
            "bestRating": "10",
            "ratingCount": "{{MOVIE_VOTES}}"
        }
    }
    </script>
    
    <style>
        body {
            background: #000;
            color: #fff;
            font-family: system-ui, -apple-system, sans-serif;
        }
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="loading">
        <i class="fas fa-spinner fa-spin text-white text-4xl"></i>
    </div>
    
    <script>
        // Redirect to main app with movie details hash
        const movieId = '{{MOVIE_ID}}';
        const movieSlug = '{{MOVIE_SLUG}}';
        
        // Redirect to index.html with hash
        window.location.href = '/index.html#' + movieSlug + '.html';
    </script>
</body>
</html>`;

// Function to create HTML file for a movie
function generateMoviePage(movie) {
    const movieSlug = movie.slug || movie.id;
    const fileName = `${movieSlug}.html`;
    const filePath = path.join(__dirname, 'app', 'src', 'main', 'assets', fileName);
    
    let html = templateHTML;
    
    // Replace placeholders
    html = html.replace(/{{MOVIE_ID}}/g, movie.id || '');
    html = html.replace(/{{MOVIE_SLUG}}/g, movieSlug);
    html = html.replace(/{{MOVIE_TITLE}}/g, movie.title || 'Movie');
    html = html.replace(/{{MOVIE_YEAR}}/g, movie.year || '');
    html = html.replace(/{{MOVIE_ORIGINAL_TITLE}}/g, movie.originalTitle || movie.title || '');
    html = html.replace(/{{MOVIE_DESCRIPTION}}/g, movie.description || `Watch ${movie.title} online`);
    html = html.replace(/{{MOVIE_GENRE}}/g, movie.genre || '');
    html = html.replace(/{{MOVIE_POSTER}}/g, movie.poster || '');
    html = html.replace(/{{MOVIE_RATING}}/g, movie.rating?.split('/')[0] || '0');
    html = html.replace(/{{MOVIE_VOTES}}/g, movie.sndVotes || '0');
    html = html.replace(/{{PAGE_URL}}/g, `https://www.soundora-music.com/${fileName}`);
    
    // Write file
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Created: ${fileName}`);
}

// Example: Generate pages for sample movies
const sampleMovies = [
    {
        id: '9-jumboq',
        slug: '9-jumboq',
        title: '9 Jumboq',
        year: '2024',
        originalTitle: '9 Jumboq',
        description: 'Hayotiy drama haqida',
        genre: 'Drama',
        poster: 'https://example.com/poster.jpg',
        rating: '7.5/10',
        sndVotes: 100
    },
    {
        id: 'jin-tilak-tila',
        slug: 'jin-tilak-tila',
        title: 'Jin, Tilak tila!',
        year: '2024',
        originalTitle: 'Jin, Tilak tila!',
        description: 'Fantastik komediya',
        genre: 'Fantasy, Comedy',
        poster: 'https://example.com/jin.jpg',
        rating: '8.0/10',
        sndVotes: 150
    }
];

// Generate pages
console.log('Generating movie HTML pages...');
sampleMovies.forEach(generateMoviePage);
console.log('Done!');

// Export for use as module
module.exports = { generateMoviePage };
