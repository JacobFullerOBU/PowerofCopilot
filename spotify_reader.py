#!/usr/bin/env python3
"""
Spotify Reader - A tool to analyze your Spotify listening habits

This tool connects to your Spotify account and provides:
1. Top 10 songs of all time (based on long-term listening patterns)
2. Top 10 artists of all time (based on long-term listening patterns)

Note: Due to Spotify API limitations, "total time listened" is approximated
using Spotify's popularity-based rankings over long-term listening patterns.
"""

import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyReader:
    def __init__(self):
        """Initialize the Spotify Reader with authentication."""
        load_dotenv()
        
        # Get credentials from environment variables
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8080')
        
        if not self.client_id or not self.client_secret:
            print("❌ Error: Spotify API credentials not found!")
            print("Please set up your .env file with your Spotify API credentials.")
            print("See .env.example for the required format.")
            sys.exit(1)
        
        # Set up Spotify authentication
        scope = "user-top-read user-read-recently-played"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope
        ))
        
    def get_top_tracks(self, limit=10, time_range='long_term'):
        """
        Get top tracks for the user.
        
        Args:
            limit: Number of tracks to return (max 50)
            time_range: 'short_term', 'medium_term', or 'long_term'
        
        Returns:
            List of track data
        """
        try:
            results = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
            return results['items']
        except Exception as e:
            print(f"❌ Error fetching top tracks: {e}")
            return []
    
    def get_top_artists(self, limit=10, time_range='long_term'):
        """
        Get top artists for the user.
        
        Args:
            limit: Number of artists to return (max 50)
            time_range: 'short_term', 'medium_term', or 'long_term'
        
        Returns:
            List of artist data
        """
        try:
            results = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
            return results['items']
        except Exception as e:
            print(f"❌ Error fetching top artists: {e}")
            return []
    
    def format_tracks(self, tracks):
        """Format track data for display."""
        if not tracks:
            return "No tracks found."
        
        output = "\n🎵 TOP 10 SONGS OF ALL TIME\n"
        output += "=" * 50 + "\n"
        
        for i, track in enumerate(tracks, 1):
            track_name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            album = track['album']['name']
            popularity = track['popularity']
            
            output += f"{i:2d}. {track_name}\n"
            output += f"    Artist(s): {artists}\n"
            output += f"    Album: {album}\n"
            output += f"    Popularity: {popularity}/100\n\n"
        
        return output
    
    def format_artists(self, artists):
        """Format artist data for display."""
        if not artists:
            return "No artists found."
        
        output = "\n🎤 TOP 10 ARTISTS OF ALL TIME\n"
        output += "=" * 50 + "\n"
        
        for i, artist in enumerate(artists, 1):
            name = artist['name']
            genres = ', '.join(artist['genres'][:3]) if artist['genres'] else 'No genres listed'
            followers = artist['followers']['total']
            popularity = artist['popularity']
            
            output += f"{i:2d}. {name}\n"
            output += f"    Genres: {genres}\n"
            output += f"    Followers: {followers:,}\n"
            output += f"    Popularity: {popularity}/100\n\n"
        
        return output
    
    def get_user_profile(self):
        """Get current user's profile information."""
        try:
            user = self.sp.current_user()
            return user
        except Exception as e:
            print(f"❌ Error fetching user profile: {e}")
            return None
    
    def run(self):
        """Run the main Spotify Reader analysis."""
        print("🎶 Spotify Reader - Analyzing Your Music Taste")
        print("=" * 50)
        
        # Get user profile
        user = self.get_user_profile()
        if user:
            print(f"📊 Analyzing data for: {user.get('display_name', 'Unknown User')}")
            print(f"🆔 User ID: {user.get('id', 'Unknown')}")
        
        print("\n🔄 Fetching your top tracks and artists...")
        print("📅 Using long-term data (several years of listening history)")
        
        # Get top tracks and artists
        top_tracks = self.get_top_tracks()
        top_artists = self.get_top_artists()
        
        # Display results
        print(self.format_tracks(top_tracks))
        print(self.format_artists(top_artists))
        
        print("=" * 50)
        print("✨ Analysis complete!")
        print("\nNote: Rankings are based on Spotify's popularity algorithm")
        print("which considers your long-term listening patterns and preferences.")


def main():
    """Main entry point for the Spotify Reader."""
    try:
        reader = SpotifyReader()
        reader.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check your internet connection and Spotify API credentials.")


if __name__ == "__main__":
    main()