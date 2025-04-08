# YouTube Transcript Extractor

A Streamlit application to extract transcripts from YouTube videos and playlists. The app fetches captions using the YouTube Transcript API and saves them as text files. If a transcript is unavailable, a corresponding notice is added to the file.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Naming Conventions](#file-naming-conventions)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Transcript Extraction:**  
  Retrieve transcripts from individual YouTube videos and complete playlists.

- **File Output:**  
  Saves each transcript (or a notification when unavailable) into a text file in a user-specified output folder.

- **Filename Sanitization:**  
  Converts YouTube URLs into safe filenames by removing protocols and replacing invalid characters.

- **Progress Indication:**  
  Provides real-time progress feedback using a progress bar and spinner within the Streamlit interface.

## Requirements

- **Python 3.7+**
- **Streamlit:** for the web interface  
- **pytube:** to handle YouTube video and playlist parsing  
- **youtube_transcript_api:** to retrieve transcript data from YouTube  

You may also need additional dependencies like `os` and `re`, which are available in the Python Standard Library.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/youtube-transcript-extractor.git
   cd youtube-transcript-extractor
   ```

2. **Create a Virtual Environment (Optional)**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install streamlit pytube youtube_transcript_api
   ```

## Usage

1. **Run the Application**

   Start the Streamlit app by executing:

   ```bash
   streamlit run your_script_name.py
   ```

   Replace `your_script_name.py` with the name of your Python file containing the code.

2. **Input YouTube URLs**

   In the provided text area:
   - Enter one YouTube URL per line.
   - You can input both individual video URLs and playlist URLs.
   - You can include quotes or commas; the app will process them appropriately.

3. **Specify Output Folder**

   Provide a folder name or path where the transcript text files will be saved. If the folder does not already exist, the app will create it.

4. **Start Processing**

   Click the **Start Processing** button:
   - The application scans the entered URLs, including extracting all video URLs from any playlists.
   - Transcripts are fetched for each video.
   - A progress bar and spinner show the processing status.
   - The transcripts are saved as text files in the specified output folder.

5. **Results**

   Once processing is complete, the app confirms that all transcripts have been saved and displays the output folder path.

## File Naming Conventions

- The application sanitizes the URL by removing `http://` or `https://` and replacing any non-alphanumeric characters (except hyphen, underscore, or dot) with underscores.
  
- **When a transcript is available:**
  - The file is named using the sanitized URL (for example, `youtube_com_watch_v_VIDEO_ID.txt`).

- **When no transcript is available:**
  - The file name is prefixed with `notranscript_` (for example, `notranscript_youtube_com_watch_v_VIDEO_ID.txt`).

## Troubleshooting

- **Transcript Not Found:**  
  If no transcript is found, the application handles the error by saving a file that states "Transcript not available." Ensure that the selected videos have captions enabled or available.

- **Playlist Issues:**  
  In case of an error while processing a playlist, the app will display an error message in the Streamlit UI. Verify that the playlist URL is correct and publicly accessible.

- **Unexpected Errors:**  
  Any unexpected errors will be reported within the Streamlit interface. Check the error message for more details on how to proceed.

## License

This project is licensed under the [MIT License](LICENSE).
