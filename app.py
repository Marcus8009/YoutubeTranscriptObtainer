import streamlit as st
import os
import re
from pytube import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def sanitize_filename(url):
    """
    Removes the http/https protocol and sanitizes a string to be safe for a filename.
    Replaces characters that are not alphanumeric, hyphen, underscore, or dot with underscores.
    """
    # Remove protocol (http:// or https://)
    url_no_protocol = re.sub(r'^https?://', '', url)
    # Sanitize the remaining string
    return re.sub(r'[^\w\-_.]', '_', url_no_protocol)

def get_video_transcript(video_url):
    """
    Attempts to retrieve a transcript for a given video URL using its video ID.
    Returns the transcript text if found, otherwise returns None.
    """
    try:
        yt = YouTube(video_url)
        video_id = yt.video_id
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine transcript entries into a single text
        transcript = "\n".join([entry["text"] for entry in transcript_list])
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None
    except Exception as e:
        st.error(f"Unexpected error for {video_url}: {e}")
        return None

st.title("YouTube Transcript Extractor")

st.markdown("""
### Instructions:
1. **Input URLs:**  
   - Enter one YouTube URL per line.  
   - You can input both individual video URLs and playlist URLs.  
   - Example:
     ```
     https://youtube.com/playlist?list=YOUR_PLAYLIST_ID
     https://www.youtube.com/watch?v=VIDEO_ID
     ```
   - You may include quotes or commas; the app will handle them.

2. **Output Folder:**  
   - Specify the folder where you want the transcript text files to be saved.  
   - The folder will be created if it doesn't already exist.

3. **Filename Conventions:**  
   - The app will remove the "http://" or "https://" part of the URL for the filename.  
   - If a transcript is available, the file will be saved as the sanitized URL (e.g., `youtube_com_watch_v_VIDEO_ID.txt`).  
   - If no transcript is found, the filename will start with `notranscript_` (e.g., `notranscript_youtube_com_watch_v_VIDEO_ID.txt`).
""")

# Single input field for multiple YouTube URLs (one per line)
input_urls = st.text_area("Enter YouTube URLs (one per line)", height=200)

# Ask user for an output folder
output_folder = st.text_input("Enter Output Folder", value="output")

if st.button("Start Processing"):
    if not input_urls.strip():
        st.error("Please enter at least one YouTube URL.")
    else:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Split the input into lines, remove extra characters like quotes and commas, and filter out empty lines
        raw_urls = [line.strip().strip('",') for line in input_urls.splitlines() if line.strip()]
        all_video_urls = []

        st.info("Extracting video URLs from playlists (if any)...")
        for url in raw_urls:
            if "playlist" in url.lower():
                try:
                    playlist = Playlist(url)
                    video_urls = playlist.video_urls
                    st.write(f"Found {len(video_urls)} videos in playlist: {url}")
                    all_video_urls.extend(video_urls)
                except Exception as e:
                    st.error(f"Error processing playlist {url}: {e}")
            else:
                all_video_urls.append(url)

        total_videos = len(all_video_urls)
        st.write(f"Total videos to process: {total_videos}")

        progress_bar = st.progress(0)
        processed_count = 0

        for video_url in all_video_urls:
            with st.spinner(f"Processing {video_url}"):
                transcript = get_video_transcript(video_url)
                sanitized_url = sanitize_filename(video_url)
                if transcript:
                    file_name = f"{sanitized_url}.txt"
                else:
                    file_name = f"notranscript_{sanitized_url}.txt"
                    transcript = "Transcript not available."
                file_path = os.path.join(output_folder, file_name)
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(transcript)
                except Exception as e:
                    st.error(f"Error writing file for {video_url}: {e}")
            processed_count += 1
            progress_bar.progress(processed_count / total_videos)

        st.success("Processing complete!")
        st.write(f"Transcripts have been saved to the folder: `{output_folder}`")
