# YouTube Downloader

![YouTube Downloader](imgs/home.png)

A simple and elegant YouTube video downloader built with **Flask**, **jQuery**, and **Bootstrap**. This application allows users to fetch video information and download YouTube videos in various formats and resolutions.

---

## Features

- 🎥 **Download Videos**: Choose from multiple resolutions and formats.
- 🎵 **Download Audio**: Extract and download audio-only streams.
- 🌙 **Dark/Light Mode**: Toggle between dark and light themes for better user experience.
- ⚡ **Fast and Responsive**: Built with modern web technologies for a seamless experience.
- 🖼️ **Video Previews**: View video thumbnails and details before downloading.

---

## Screenshots

### Video Info
![Video Info](imgs/video_info.png)

### Download Options
![Options](imgs/options.png)

---

## Installation
### Prerequisites
- Python 3.x
- Internet connection (for downloading videos)
- Docker (optional, for running the app in a container)

#### Installing with pip
You can run this application locally by following these steps:

1. Install the required packages:
   ```bash
   pip install -r requirements.txt # It is advised to use a virtual environment
   ```

2. Run the Flask application:
   ```bash
    python app.py
    ```

2. Access the application in your web browser at `http://localhost:5000`.

#### Running with Docker
You can also run this application using Docker. Make sure you have Docker installed on your machine.  
1. Run the docker-compose command to build and start the application:
   ```bash
   docker-compose up --build -d
   ```
2. Access the application in your web browser at `http://localhost:5000`.