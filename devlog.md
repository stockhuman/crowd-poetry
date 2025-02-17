# Dev Log

My strategy in building out the basic architecture is of course first exploring what's out there in terms of APIs for TikTok et al. Unfortunately it seems the [Research API](https://developers.tiktok.com/products/research-api/) is not available in Canada. 
Thankfully, access by unofficial means seems to be available though 3rd party libraries (primarily in Python), chiefly via [PykTok](https://pypi.org/project/pyktok/).

## Hardware Exploration - 2025.01.30

I am going to first test the Olimex A20-OlinuXino. This board offers a linux platform for python scripting which is likely going to be necessary. The plans for more low-level hardware are unlikely to proceed given the API and the A/V complexity. On the other hand, this opens up the possiblity of using a display.

--

UPDATE: The A20-OlinuXino-LIME2 is not powerful enough to run pyktok. I will be switching to a Raspberry Pi 5.

## Software - 2025.01.31

It seems TikTok search is atrocious, by official and unofficial means. A better way of downloading content may be necessary. On the plus side, I can reliably search for and download TikTok video files.

I will go ahead with this PoC implementation to then test the other component parts of this architecture. YouTube, Vimeo or other platforms may be necessary to pivot to in case reliable content surfacing isn't possible on TikTok.

## Software - 2025.02.10

I've found https://filmot.com/, which offers a very compelling search product for almost exactly what I'm looking for, except it's YouTube-based and does not seem to offer an API. 3rd party projects exist to provide one, however. Upon investigation, it seems projects like [this](https://github.com/dusking/filmot) are abandonware and not implementable.

## Software - 2025.02.16

The technical challenge now is to get the audio clips _whittled down_ into morcels that actually represent the words being chosen. For this, OpenAI's whisper (available as FOSS locally and as a paid service at ~$0.006 per minute) as well as Vosk seem to be necessary to get far more accurate soundbytes out of YouTube files, which are downloading successfully.
