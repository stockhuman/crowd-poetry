from fastapi import FastAPI
from pydantic import BaseModel
from random import choice
from scraper import fetch_filmot_data
from downloader import download
from trim import trim, segment
from db import insert_mp3, fetch_mp3_files, fetch_mp3_by_keyword

app = FastAPI()


class SearchParameters(BaseModel):
  word: str
  duration: int | None = 300


@app.post("/search/")
async def search_filmot(params: SearchParameters):
  try:
    data = fetch_filmot_data(params.query, params.duration)
    entries = list(data.items())

    # TODO: try again if failed to download, download another
    if entries:
      video_key, video_data = choice(entries)
      video_id = video_data["vid"]
      hit = video_data["hits"][0]
      start_time = hit["start"]
      duration = hit["dur"]
      token = hit["token"]
      end_time = start_time + duration

      filepath = download(video_id, start_time, end_time, token)
      print(f"Audio file: {filepath}")

      start, end = segment(filepath, params.query)

      if start is not None:
        trimmed_audio = trim(
          filepath, start, end, f"audio_clips/trim_{params.query}_{video_id}.mp3"
        )
        insert_mp3(trimmed_audio, params.query, video_id)
        return {"status": "success", "data": trimmed_audio}
      else:
        return {"status": "failed", "data": "trim error"}

    else:
      return {"status": "failed", "data": "no results"}
  except Exception as e:
    return {"status": "error", "message": str(e)}


# Return all audio files presently available
@app.get("/known")
def known():
  try:
    return {"status": "success", "data": fetch_mp3_files()}
  except Exception as e:
    return {"status": "error", "message": str(e)}


# Return all audio files presently available for a given word
@app.get("/known/{word}")
def known_word(word):
  try:
    return {"status": "success", "data": fetch_mp3_by_keyword(word)}
  except Exception as e:
    return {"status": "error", "message": str(e)}
