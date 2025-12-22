#!/usr/bin/env python3
"""
Firebase Movie HTML Generator
Fetches all movies from Firestore and generates individual HTML pages
Run this: python firebase_movie_generator.py
"""

import os
import json
import re
import firebase_admin
from firebase_admin import credentials, firestore

# HTML template
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
    if not text:
        return ''
    # Convert to lowercase
    text = str(text).lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ''
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text


def generate_movie_page(movie_data, output_dir):
    """Generate HTML file for a single movie"""
    
    # Get movie data with defaults
    movie_id = str(movie_data.get('id', ''))
    movie_title = escape_html(movie_data.get('title', 'Movie'))
    movie_slug = movie_data.get('slug') or slugify(movie_id)
    movie_year = str(movie_data.get('year', ''))
    movie_original_title = escape_html(movie_data.get('originalTitle', movie_title))
    movie_description = escape_html(movie_data.get('description', f'Watch {movie_title} online'))
    movie_genre = escape_html(movie_data.get('genre', ''))
    movie_poster = movie_data.get('poster', '')
    
    # Extract rating
    rating_str = movie_data.get('rating', '0/10')
    movie_rating = rating_str.split('/')[0] if '/' in rating_str else '0'
    movie_votes = str(movie_data.get('sndVotes', 0))
    
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
    
    print(f"✓ Created: {filename}")
    return filename


def main():
    """Main function to fetch from Firebase and generate pages"""
    
    # Initialize Firebase
    print("Initializing Firebase...")
    
    # You need to download service account key from Firebase Console
    # and save it as 'serviceAccountKey.json'
    cred_path = 'serviceAccountKey.json'
    
    if not os.path.exists(cred_path):
        print(f"ERROR: {cred_path} not found!")
        print("\nPlease download your Firebase service account key:")
        print("1. Go to Firebase Console > Project Settings > Service Accounts")
        print("2. Click 'Generate New Private Key'")
        print(f"3. Save it as '{cred_path}' in this directory")
        return
    
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"ERROR initializing Firebase: {e}")
        return
    
    # Get Firestore client
    db = firestore.client()
    
    # Define output directory
    output_dir = os.path.join('app', 'src', 'main', 'assets')
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nFetching movies from Firestore...")
    
    try:
        # Fetch all movies
        movies_ref = db.collection('movies')
        movies = movies_ref.stream()
        
        count = 0
        for movie_doc in movies:
            movie_data = movie_doc.to_dict()
            if movie_data:
                generate_movie_page(movie_data, output_dir)
                count += 1
        
        print(f"\n✓ Done! Generated {count} movie HTML pages in {output_dir}")
        
    except Exception as e:
        print(f"ERROR fetching movies: {e}")


if __name__ == '__main__':
    main()
