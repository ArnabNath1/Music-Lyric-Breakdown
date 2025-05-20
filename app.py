import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import lyricsgenius
import wikipedia
import os
from groq import Groq
from dotenv import load_dotenv
import isodate

load_dotenv()

# Configure API keys
genius = lyricsgenius.Genius("DzOBQKCGVkb6GZ6Fpybg0DMQsnzMiFtf8pqGLXxL2g7hF5eb0016P3duwrgr6UUH")
youtube_api_key = "AIzaSyD-IeL0KhdTCtkyxGt9mIHtISh2utlqIoQ"
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize Groq client
client = Groq(api_key=groq_api_key)

def get_video_info(url):
    try:
        # Extract video ID from URL
        if 'youtube.com' in url or 'youtu.be' in url:
            if 'youtube.com' in url:
                video_id = url.split('v=')[1].split('&')[0]
            else:
                video_id = url.split('/')[-1].split('?')[0]
        else:
            st.error("Please enter a valid YouTube URL")
            return None

        # Initialize YouTube API client
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)

        # Get video details
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()

        if not response['items']:
            st.error("Video not found")
            return None

        video_data = response['items'][0]
        
        return {
            'title': video_data['snippet']['title'],
            'author': video_data['snippet']['channelTitle'],
            'views': int(video_data['statistics']['viewCount']),
            'length': video_data['contentDetails']['duration'],
            'thumbnail': video_data['snippet']['thumbnails']['high']['url']
        }
    except Exception as e:
        st.error(f"Error fetching video info: {str(e)}")
        return None

def get_song_lyrics(title, artist):
    try:
        song = genius.search_song(title, artist)
        return song.lyrics if song else "Lyrics not found"
    except:
        return "Lyrics not found"

def analyze_lyrics_with_groq(lyrics, title, artist):
    prompt = f"""
    Analyze the following song:
    Title: {title}
    Artist: {artist}
    Lyrics: {lyrics}
    
    Please provide a detailed analysis in the following format:

    1. LYRICS MEANING
    - Overall message and meaning of the lyrics
    - Line-by-line interpretation of key verses
    - Hidden meanings or double entendres
    
    2. SONG ANALYSIS
    - Main theme of the song
    - Emotional tone and mood
    - Key metaphors and symbolism
    - Cultural or historical context
    - Notable musical elements

    3. PERSONAL IMPACT
    - How the song might resonate with listeners
    - Universal themes or messages
    - Cultural significance
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gemma2-9b-it",
        temperature=0.7,
        max_tokens=2048
    )
    
    # Just return the analysis content
    return response.choices[0].message.content

def get_artist_info(artist_name):
    try:
        return wikipedia.summary(artist_name, sentences=5)
    except:
        return "Artist information not found"

def main():
    st.title("🎵 Song Analysis App")
    st.write("Enter a YouTube URL to analyze the song!")

    url = st.text_input("YouTube URL")
    
    if url:
        video_info = get_video_info(url)
        
        if video_info:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(video_info['thumbnail'], use_container_width=True)
            
            with col2:
                st.subheader("Video Information")
                st.write(f"Title: {video_info['title']}")
                st.write(f"Artist: {video_info['author']}")
                st.write(f"Views: {video_info['views']:,}")
                # Convert ISO 8601 duration to human-readable format
                duration = isodate.parse_duration(video_info['length'])
                minutes = int(duration.total_seconds() // 60)
                seconds = int(duration.total_seconds() % 60)
                st.write(f"Length: {minutes}:{seconds:02d}")

            # Get and display lyrics
            st.subheader("Lyrics")
            lyrics = get_song_lyrics(video_info['title'], video_info['author'])
            st.write(lyrics)

            # Analyze lyrics using Groq
            if lyrics != "Lyrics not found":
                st.subheader("📝 Lyrics Analysis")
                with st.expander("View Complete Analysis", expanded=True):
                    analysis = analyze_lyrics_with_groq(lyrics, video_info['title'], video_info['author'])
                    st.markdown(analysis)  # Display analysis once
            else:
                st.warning("Cannot analyze lyrics as they were not found.")

            # Get and display artist information
            st.subheader("About the Artist")
            artist_info = get_artist_info(video_info['author'])
            st.write(artist_info)

if __name__ == "__main__":
    main()