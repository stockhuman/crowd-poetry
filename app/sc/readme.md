# SuperCollider Send

This foder contains a script that watches a directory for new audio files and sends them to SuperCollider via UDP. It also contains the SuperCollider code that plays the audio files at the heart of this project.

## Setup

```bash
cd sc
poetry env use 3.10
poetry install
```
## Usage

```bash
poetry run python loader.py
sclang sampler.scd
```