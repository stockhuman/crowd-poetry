from filmot_scraper.scraper import fetch_filmot_data
from filmot_scraper.downloader import download
from filmot_scraper.trim import trim, segment

if __name__ == "__main__":
  query = "technical"  # Example search term
  duration = 300  # Example duration in seconds

  try:
    data = fetch_filmot_data(query, duration)
    entries = list(data.items())

    if entries:
      video_key, video_data = entries[4]
      video_id = video_data["vid"]
      hit = video_data["hits"][0]
      start_time = hit["start"]
      duration = hit["dur"]
      token = hit["token"]
      end_time = start_time + duration

      filepath = download(video_id, start_time, end_time, token)
      print(f"Audio file: {filepath}")

      start, end = segment(filepath, query)

      if start is not None:
        trimmed_audio = trim(
          filepath, start, end, f"audio_clips/trim_{query}_{video_id}.mp3"
        )
        print(f"Trimmed file saved as: {trimmed_audio}")
      else:
        print("Phrase not found in audio.")

  except Exception as e:
    print(f"Error: {e}")
