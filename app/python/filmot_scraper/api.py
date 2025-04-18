from os import makedirs, path, unlink
from typing import Optional
from fastapi import FastAPI, Request, staticfiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import choice
from scraper import fetch_filmot_data
from downloader import download
from trim import trim, segment
from db import create_tables, fetch_current_poem, insert_audio, fetch_audio_files, fetch_mp3_by_keyword, insert_poem

app = FastAPI()

if __name__ == "__main__":
  create_tables()
  import uvicorn
  uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)


# Ensure the directory exists
makedirs("audio_clips", exist_ok=True)

# Mount the directory to serve MP3 files
app.mount("/audio", staticfiles.StaticFiles(directory="audio_clips"), name="audio")

# Enable CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class SearchParameters(BaseModel):
  word: str
  duration: Optional[int] = 300

@app.post("/search/")
async def search_filmot(request: Request, params: SearchParameters):
  try:
    base_url = str(request.base_url)
    data = fetch_filmot_data(params.word, params.duration)
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

      start, end = segment(filepath, params.word)

      if start is not None:
        trimmed_audio = trim(
          filepath, start, end, f"audio_clips/trim_{params.word}_{video_id}.wav"
        )
        unlink(filepath)

        insert_audio(trimmed_audio, params.word, video_id)
        return {"status": "success", "data": f"{base_url}audio/{path.basename(trimmed_audio)}"}
      else:
        return {"status": "failed", "data": "trim error"}

    else:
      return {"status": "failed", "data": "no results"}
  except Exception as e:
    print(e)
    return {"status": "error", "message": str(e)}


# Return all audio files presently available
@app.get("/known")
def known(request: Request):
  try:
    base_url = str(request.base_url)
    mp3_entries = fetch_audio_files()
    # Convert relative paths to full URLs
    formatted_entries = [
      {
        "id": entry[0],
        "file_url": f"{base_url}audio/{path.basename(entry[1])}",
        "keyword": entry[2],
        "video_id": entry[3],
        "timestamp": entry[4],
      }
      for entry in mp3_entries
    ]
    return {"status": "success", "data":formatted_entries}
  except Exception as e:
    return {"status": "error", "message": str(e)}


# Return all audio files presently available for a given word
@app.get("/known/{word}")
def known_word(request: Request,word):
  try:
    base_url = str(request.base_url)
    mp3_entries = fetch_mp3_by_keyword(word)
    formatted_entries = [
      {
          "id": entry[0],
          "file_url": f"{base_url}audio/{path.basename(entry[1])}",
          "keyword": entry[2],
          "video_id": entry[3],
          "timestamp": entry[4],
      }
      for entry in mp3_entries
    ]
    return {"status": "success", "data": formatted_entries}
  except Exception as e:
    return {"status": "error", "message": str(e)}

@app.get("/current")
def current(request: Request):
  try:
    poem = fetch_current_poem()
    formatted_poem = {
      "id": poem[0],
      "poem": poem[1],
      "latitude": poem[2],
      "longitude": poem[3],
      "timestamp": poem[4],
    }
    return {"status": "success", "data": formatted_poem}
  except Exception as e:
    print(e)
    return {"status": "error", "message": str(e)}
  
class PoemUpdateParameters(BaseModel):
  poem: str
  latitude: Optional[float] = .0
  longitude: Optional[float] = .0

@app.post("/update-poem")
async def update_poem(params: PoemUpdateParameters):
  try:
    insert_poem(params.poem, params.latitude, params.longitude)
    return {"status": "success", "data": "poem added"}
  except Exception as e:
    print(e)
    return {"status": "error", "message": str(e)}