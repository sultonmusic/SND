#!/usr/bin/env python3
"""
Script to generate individual HTML pages for each movie
Run this: python generate_movie_pages.py
"""

import os
import json
import re

# HTML template for each movie page
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>{movie_title} ({movie_year}) - SND</title>
    <meta name="description" content="{movie_description}">
    <meta name="keywords" content="{movie_title}, {movie_original_title}, {movie_genre}, смотреть онлайн, SND, фильм, кино">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="video.movie">
    <meta property="og:url" content="{page_url}">
    <meta property="og:title" content="{movie_title} ({movie_year}) - SND">
    <meta property="og:description" content="{movie_description}">
    <meta property="og:image" content="{movie_poster}">
    <meta property="og:site_name" content="SND - Streaming Network of Dreams">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{page_url}">
    <meta name="twitter:title" content="{movie_title} ({movie_year}) - SND">
    <meta name="twitter:description" content="{movie_description}">
    <meta name="twitter:image" content="{movie_poster}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{page_url}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Movie",
        "name": "{movie_title}",
        "alternateName": "{movie_original_title}",
        "image": "{movie_poster}",
        "description": "{movie_description}",
        "datePublished": "{movie_year}-01-01",
        "genre": "{movie_genre}",
        "url": "{page_url}",
        "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": "{movie_rating}",
            "bestRating": "10",
            "ratingCount": "{movie_votes}"
        }}
    }}
    </script>
    
    <style>
        body {{
            background: #000;
            color: #fff;
            font-family: system-ui, -apple-system, sans-serif;
        }}
        .loading {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="loading">
        <i class="fas fa-spinner fa-spin text-white text-4xl"></i>
    </div>
    
    <script>
        // Redirect to main app with movie details hash
        const movieId = '{movie_id}';
        const movieSlug = '{movie_slug}';
        
        // Redirect to index.html with hash
        window.location.href = 'index.html#' + movieSlug + '.html';
    </script>
</body>
</html>"""


def slugify(text):
    """Convert text to URL-friendly slug"""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_movie_page(movie, output_dir):
    """Generate HTML file for a single movie"""
    
    # Get movie data with defaults
    movie_id = str(movie.get('id', ''))
    movie_title = movie.get('title', 'Movie')
    movie_slug = movie.get('slug', slugify(movie_id))
    movie_year = str(movie.get('year', ''))
    movie_original_title = movie.get('originalTitle', movie_title)
    movie_description = movie.get('description', f'Watch {movie_title} online')
    movie_genre = movie.get('genre', '')
    movie_poster = movie.get('poster', '')
    
    # Extract rating
    rating_str = movie.get('rating', '0/10')
    movie_rating = rating_str.split('/')[0] if '/' in rating_str else '0'
    movie_votes = str(movie.get('sndVotes', 0))
    
    # Generate filename
    filename = f"{movie_slug}.html"
    page_url = f"https://www.soundora-music.com/{filename}"
    
    # Fill template
    html = TEMPLATE_HTML.format(
        movie_id=movie_id,
        movie_slug=movie_slug,
        movie_title=movie_title,
        movie_year=movie_year,
        movie_original_title=movie_original_title,
        movie_description=movie_description,
        movie_genre=movie_genre,
        movie_poster=movie_poster,
        movie_rating=movie_rating,
        movie_votes=movie_votes,
        page_url=page_url
    )
    
    # Write file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Created: {filename}")
    return filename


def main():
    """Main function to generate all movie pages"""
    
    # Define output directory
    output_dir = os.path.join('app', 'src', 'main', 'assets')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample movies for testing
    sample_movies = [
        {
            'id': '9-jumboq',
            'slug': '9-jumboq',
            'title': '9 Jumboq',
            'year': '2024',
            'originalTitle': '9 Jumboq',
            'description': 'Hayotiy drama haqida',
            'genre': 'Drama',
            'poster': 'https://example.com/poster.jpg',
            'rating': '7.5/10',
            'sndVotes': 100
        },
        {
            'id': 'jin-tilak-tila',
            'slug': 'jin-tilak-tila',
            'title': 'Jin, Tilak tila!',
            'year': '2024',
            'originalTitle': 'Jin, Tilak tila!',
            'description': 'Fantastik komediya',
            'genre': 'Fantasy, Comedy',
            'poster': 'https://example.com/jin.jpg',
            'rating': '8.0/10',
            'sndVotes': 150
        }
    ]
    
    print('Generating movie HTML pages...')
    
    for movie in sample_movies:
        generate_movie_page(movie, output_dir)
    
    print(f'\nDone! Generated {len(sample_movies)} movie pages in {output_dir}')
    print('\nTo generate pages from Firebase data, modify the script to fetch from Firestore.')


if __name__ == '__main__':
    main()
