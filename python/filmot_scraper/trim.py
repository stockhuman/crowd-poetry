from vosk import Model, KaldiRecognizer
import json
import os
from pydub import AudioSegment, effects # Requires ffmpeg to be installed

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../vosk_models/vosk-model-small-en-us-0.15")

# MODEL_PATH = os.path.join(os.path.dirname(__file__), "../vosk_models/vosk-model-en-us-0.22-lgraph")


def segment(filepath: str, phrase: str):
  """Trim audio clip by first transribing it."""
  model = Model(MODEL_PATH)
  recognizer = KaldiRecognizer(model, 16000)
  recognizer.SetWords(True)  # Ensure we get word-level timestamps

  results = []
  
  # Convert to WAV first
  wav_path = convert_to_wav(filepath)

  with open(wav_path, "rb") as f:
    while True:
      data = f.read(4000)
      if len(data) == 0:
        break
      if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print(result)
        if "result" in result:
          results.extend(result["result"])

    # Final result for remaining audio
    final_result = json.loads(recognizer.FinalResult())
    if "result" in final_result:
      results.extend(final_result["result"])
    
    # Clean up
    os.remove(wav_path)

    return find_word_timestamps(results, phrase)


def find_word_timestamps(segments, target_word):
  """Find start and end timestamps for a word or phrase."""
  matches = []

  for i, seg in enumerate(segments):
    if target_word in seg["word"]:
      start = seg["start"]
      end = seg["end"]
      matches.append((start, end))

  if matches:
    # Merge the timestamps if the phrase spans multiple words
    return matches[0][0], matches[-1][1]

  return None, None  # Word not found


def trim(filepath: str, start: int, end: int, output_file: str):
  """Trim audio clip by start and end time."""
  audio = AudioSegment.from_file(filepath)
  trimmed = audio[start * 1000 - 100 : end * 1000 + 100]
  trimmed.export(output_file, format="mp3")
  return output_file

def convert_to_wav(filepath: str) -> str:
  """Convert input audio file to 16kHz mono WAV for Vosk processing."""
  audio = AudioSegment.from_file(filepath)
  audio = audio.set_frame_rate(16000).set_channels(1)  # Vosk requires 16kHz mono
  normalized = effects.normalize(audio)  
  wav_path = os.path.splitext(filepath)[0] + ".wav"
  normalized.export(wav_path, format="wav")
  return wav_path