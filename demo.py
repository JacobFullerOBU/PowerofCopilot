#!/usr/bin/env python3
"""
Demo script showing sample output of the Spotify Reader tool.
This demonstrates the expected format and functionality without requiring Spotify credentials.
"""

def demo_spotify_reader():
    """Demonstrate the Spotify Reader output format with mock data."""
    
    print("🎶 Spotify Reader - Analyzing Your Music Taste")
    print("=" * 50)
    print("📊 Analyzing data for: Demo User")
    print("🆔 User ID: demo_user_123")
    print("\n🔄 Fetching your top tracks and artists...")
    print("📅 Using long-term data (several years of listening history)")
    
    # Mock top tracks
    mock_tracks = [
        {"name": "Bohemian Rhapsody", "artists": [{"name": "Queen"}], "album": {"name": "A Night at the Opera"}, "popularity": 95},
        {"name": "Imagine", "artists": [{"name": "John Lennon"}], "album": {"name": "Imagine"}, "popularity": 92},
        {"name": "Hotel California", "artists": [{"name": "Eagles"}], "album": {"name": "Hotel California"}, "popularity": 90},
        {"name": "Stairway to Heaven", "artists": [{"name": "Led Zeppelin"}], "album": {"name": "Led Zeppelin IV"}, "popularity": 88},
        {"name": "Sweet Child O' Mine", "artists": [{"name": "Guns N' Roses"}], "album": {"name": "Appetite for Destruction"}, "popularity": 87},
        {"name": "Billie Jean", "artists": [{"name": "Michael Jackson"}], "album": {"name": "Thriller"}, "popularity": 86},
        {"name": "Like a Rolling Stone", "artists": [{"name": "Bob Dylan"}], "album": {"name": "Highway 61 Revisited"}, "popularity": 85},
        {"name": "Smells Like Teen Spirit", "artists": [{"name": "Nirvana"}], "album": {"name": "Nevermind"}, "popularity": 84},
        {"name": "Yesterday", "artists": [{"name": "The Beatles"}], "album": {"name": "Help!"}, "popularity": 83},
        {"name": "Purple Haze", "artists": [{"name": "Jimi Hendrix"}], "album": {"name": "Are You Experienced"}, "popularity": 82}
    ]
    
    # Mock top artists
    mock_artists = [
        {"name": "The Beatles", "genres": ["rock", "pop", "british invasion"], "followers": {"total": 22000000}, "popularity": 95},
        {"name": "Queen", "genres": ["rock", "glam rock", "arena rock"], "followers": {"total": 18000000}, "popularity": 92},
        {"name": "Led Zeppelin", "genres": ["rock", "hard rock", "heavy metal"], "followers": {"total": 15000000}, "popularity": 90},
        {"name": "Pink Floyd", "genres": ["progressive rock", "psychedelic rock"], "followers": {"total": 14000000}, "popularity": 88},
        {"name": "Michael Jackson", "genres": ["pop", "r&b", "soul"], "followers": {"total": 13000000}, "popularity": 87},
        {"name": "Bob Dylan", "genres": ["folk", "rock", "country"], "followers": {"total": 12000000}, "popularity": 86},
        {"name": "The Rolling Stones", "genres": ["rock", "blues rock"], "followers": {"total": 11000000}, "popularity": 85},
        {"name": "David Bowie", "genres": ["rock", "glam rock", "art rock"], "followers": {"total": 10000000}, "popularity": 84},
        {"name": "Eagles", "genres": ["rock", "country rock"], "followers": {"total": 9000000}, "popularity": 83},
        {"name": "Nirvana", "genres": ["grunge", "alternative rock"], "followers": {"total": 8000000}, "popularity": 82}
    ]
    
    # Format and display tracks
    print("\n🎵 TOP 10 SONGS OF ALL TIME")
    print("=" * 50)
    
    for i, track in enumerate(mock_tracks, 1):
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album = track['album']['name']
        popularity = track['popularity']
        
        print(f"{i:2d}. {track_name}")
        print(f"    Artist(s): {artists}")
        print(f"    Album: {album}")
        print(f"    Popularity: {popularity}/100\n")
    
    # Format and display artists
    print("🎤 TOP 10 ARTISTS OF ALL TIME")
    print("=" * 50)
    
    for i, artist in enumerate(mock_artists, 1):
        name = artist['name']
        genres = ', '.join(artist['genres'][:3]) if artist['genres'] else 'No genres listed'
        followers = artist['followers']['total']
        popularity = artist['popularity']
        
        print(f"{i:2d}. {name}")
        print(f"    Genres: {genres}")
        print(f"    Followers: {followers:,}")
        print(f"    Popularity: {popularity}/100\n")
    
    print("=" * 50)
    print("✨ Analysis complete!")
    print("\nNote: Rankings are based on Spotify's popularity algorithm")
    print("which considers your long-term listening patterns and preferences.")
    print("\n📝 This is a demo with sample data. Run spotify_reader.py with")
    print("   proper credentials to analyze your actual Spotify data.")


if __name__ == "__main__":
    demo_spotify_reader()