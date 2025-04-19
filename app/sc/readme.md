# SuperCollider Send

This foder contains a script that watches a directory for new audio files and sends them to SuperCollider via UDP. It also contains the SuperCollider code that plays the audio files at the heart of this project.

## Setup

```bash
cd sc
poetry env use 3.10
poetry install --no-root
```
## Usage

```bash
poetry run python loader.py
sclang sampler.scd
```

## Notes
`QT_QPA_PLATFORM=offscreen sclang` is required to run on headless Linux.
`jackd -P75 -dalsa -dhw:0 -zs  -p1024 -n3 -s -r44100` is required to be set in .jackdrc, with special attention to `-sz` dithering.