# PowerofCopilot
This is completely developed by copilot btw

## Spotify Reader

A Python tool that connects to your Spotify account and analyzes your listening habits to provide:

1. **Top 10 songs of all time** - Based on your long-term listening patterns
2. **Top 10 artists of all time** - Based on your long-term listening patterns

### Features

- 🎵 **Top Songs Analysis**: Discover your most-played tracks with detailed information
- 🎤 **Top Artists Analysis**: See your favorite artists with genre and popularity data
- 📊 **User Profile Info**: Display your Spotify profile information
- 🔐 **Secure Authentication**: Uses OAuth 2.0 for secure Spotify API access
- 📅 **Long-term Data**: Analyzes several years of listening history

### Prerequisites

1. **Python 3.6+** installed on your system
2. **Spotify Account** (free or premium)
3. **Spotify Developer App** credentials

### Setup Instructions

#### 1. Get Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - App name: "Spotify Reader" (or any name you prefer)
   - App description: "Personal music analysis tool"
   - Redirect URI: `http://localhost:8080`
5. Save your **Client ID** and **Client Secret**

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Spotify credentials:
```
SPOTIPY_CLIENT_ID=your_actual_client_id
SPOTIPY_CLIENT_SECRET=your_actual_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080
```

### Usage

Run the Spotify Reader:

```bash
python spotify_reader.py
```

**First-time usage:**
1. The tool will open your web browser for Spotify authentication
2. Log in to Spotify and authorize the application
3. You'll be redirected to localhost - copy the full URL from your browser
4. Paste the URL back in the terminal when prompted
5. Your analysis will begin automatically

**Subsequent usage:**
- The tool will remember your authorization
- Analysis will start immediately

### Sample Output

```
🎶 Spotify Reader - Analyzing Your Music Taste
==================================================
📊 Analyzing data for: Your Name
🆔 User ID: your_spotify_id

🔄 Fetching your top tracks and artists...
📅 Using long-term data (several years of listening history)

🎵 TOP 10 SONGS OF ALL TIME
==================================================
 1. Song Name
    Artist(s): Artist Name
    Album: Album Name
    Popularity: 85/100

 2. Another Song
    Artist(s): Another Artist
    Album: Another Album
    Popularity: 82/100

...

🎤 TOP 10 ARTISTS OF ALL TIME
==================================================
 1. Artist Name
    Genres: pop, indie rock, alternative
    Followers: 1,234,567
    Popularity: 88/100

 2. Another Artist
    Genres: hip hop, rap, trap
    Followers: 2,345,678
    Popularity: 85/100

...
```

### Technical Notes

**About "Total Time Listened":**
The Spotify Web API doesn't provide exact listening time data. Instead, this tool uses Spotify's "top tracks" and "top artists" endpoints with the `long_term` time range, which analyzes several years of your listening history and ranks items based on Spotify's popularity algorithm that considers your personal listening patterns.

**Time Ranges:**
- `long_term`: Several years of data (default)
- `medium_term`: Approximately last 6 months
- `short_term`: Approximately last 4 weeks

### Dependencies

- `spotipy`: Official Spotify Web API wrapper for Python
- `python-dotenv`: Environment variable management

### Security

- Your Spotify credentials are stored locally in `.env` (not committed to git)
- OAuth 2.0 authentication ensures secure API access
- No personal data is stored or transmitted outside of Spotify's official API

### Troubleshooting

**"Credentials not found" error:**
- Ensure your `.env` file exists and contains valid Spotify API credentials
- Check that your Client ID and Client Secret are correct

**Authentication issues:**
- Verify your Redirect URI in both `.env` and your Spotify app settings
- Make sure `http://localhost:8080` is exactly as configured in your Spotify app

**No data returned:**
- New Spotify accounts may have limited listening history
- Try changing the time range in the code from `long_term` to `medium_term` or `short_term`

### License

This project is open source and available under the MIT License.
