# Crowd Poetry API
This collection of loose scripts scrapes Filmot, downloads the retrieved audio files and serves them.

## Setup
```bash
sudo apt install ffmpeg -y
cd python
poetry env use 3.9.0
poetry install --no-root
```

## Usage
```bash
poetry run python api.py
```