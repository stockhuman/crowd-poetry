import yt_dlp

OUTPUT_DIR = 'audio_clips'

def download(video_id: str, start: int, end: int, token: str):
  """Download audio clip from YouTube video."""
  url = f"https://www.youtube.com/watch?v={video_id}"
  output_file = f"{OUTPUT_DIR}/{token}_{video_id}"

  def download_ranges_cb(info_dict, ydl):
    return [{"start_time": start, "end_time": end}]
    
  ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_file,
    "download_ranges": download_ranges_cb,
    "quiet": True,
    "postprocessors": [
      {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
      }
    ],
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
    
  return F"{output_file}.mp3"
