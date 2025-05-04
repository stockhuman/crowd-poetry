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

## Software - 2025.03.01

The way the software stack is going, and the fact that I'm now processing YouTube videos primarily (though still hope to draw from other sources now as a stretch goal) - I've reconsidered the standalone device model. 

Audio clips are being served by a FastAPI service implementation, and I've now turned my attention towards the physical device. Since a server will do the number crunching, I'm free to implement something considerably lighter in compute power. I have experience with the ESP-IDF framework with regard to audio, which could make this a very economical project, but I'm not sure I want to commit to that degree of programming without leaving room for design iteration.

## Hardware - 2025.03.08
I've built a simple web front-end to alter the poem, and now I'm exploring design concepts for the physical device.

## Hardware - 2025.03.20
Hardware selection is now complete. The audio processing is to happen on a Teensy 4.0 and a associated Audio Shield, whilst the file fetching and server interactions are to be managed by an Orange Pi Zero.
The selection of the Teensy is largely due to its DSP strengths and robust audio library support. Whilst I'm not an expert, I've had positive experiences with Paul Stoffregen's work and his online [pseudo-IDE](https://www.pjrc.com/teensy/gui/index.html). The ESP-ADF framework would've been cool, but likely too technically challenging for me to commit to exploratively, and the ESP32 LyraT v4.1 board I had on hand did not have the pinouts I needed to power an external display or extra peripherals. It also was rather forma-facotr limiting given its footprint.

![Orange Pi](./docs/orangepi.png)

## Hardware - 2025.03.24

Thank you, [Giuseppe](http://www.orangepi.org/orangepibbsen/forum.php?mod=viewthread&tid=2441)!  UART2 is `/dev/ttyS2` on the Orange Pi Zero. I'm now trying to get the last non-experiemntal piece of this puzzle working: communication of audio files from the Orange Pi to the Teensy. Explorations beyond paper and pencil in the design of the hardware are underway.

![Draft design, a box](./docs/concept.png)

## Software - 2025.03.27

I've now got the audio file transfer working.

## Software - 2025.03.29

Never mind that, audio transfer is not going to work between the two devices. I am exploring the [Glicol](https://glicol.org/) project, which is a live coding environment for musical expression. It seems promising, but it requires a web interface as it essentially binds Rust to Javascript's web audio API.

[SuperCollider was also considered](https://gist.github.com/madskjeldgaard/8d5b2f0eeeb31fa53a922e6653fc703f).

`node-web-audio-api` was briefly emplored, but the available implementations lacked a number of standard features.

Well, here's the challenge in this project: how to get the audio clips _whittled down_ into morcels that actually represent the words being chosen, and then from there, getting them mixed and playable into something interesting. It is frustrating that I still have not completed the overall architecture of the project end-to-end.

## Hardware - 2025.04.06
I have abandoned the Orange Pi Zero and Teensy in favor of a Raspberry Pi 4. Software support and Realtime Linux are the two most important factors in my decision.

## Software - 2025.04.10

I'm now working on the Raspberry Pi 4 exclusively. Pure Data is running headless with ALSA, and Python is orchestrating dynamic sample playback through OSC. After some trial and error with JACK, .asoundrc, and pd flags, I’ve found a reliable startup configuration that plays a test tone and loads sample files on command. Audio playback is verified, and the system can now load and play individual WAV files with minimal latency.

## Software - 2025.04.12

Sample loading now works! Pure Data can be triggered via OSC from Python to play a sample located at a specific path. Communication is lightweight and effective. The patch is set up to receive /loadsample messages and play the corresponding file once. This proves the system's runtime dynamic audio capability and sets the stage for integration with the rest of the pipeline.

## Hardware - 2025.04.13

The Pi is being run from SSD for faster boot and responsiveness. Patchbox OS was considered but ruled out due to maintenance concerns. I'm manually optimizing for audio with ALSA and avoiding JACK for now. CPU and memory usage are low enough for comfortable runtime operation. Next steps are design integration and tying together sample fetching, parsing, and playback logic.

## Software - 2025.04.14

Attempted to build the ELSE library for Pure Data to support dynamic control structures (count, join). Initial steps:
Eventually abandoned this approach after hitting build issues and system-level clutter. Considered PlugData as an alternative but dropped it due to maintenance overhead on RPi.

## Software - 2025.04.15

Switched to SuperCollider as an audio engine. Installed via apt, then removed and built from source for headless use:
Cloned supercollider repo and built with options to disable IDE and GUI (-DSC_IDE=OFF -DNO_X11=ON)
Wrote a minimal .scd script to play loaded WAV files. Playback worked, but audio was extremely distorted. Verified:
  - 48kHz sample rate
  - 16-bit mono WAVs
  - ALSA output
  - JACK server was active

Suspected RPi's internal DAC was introducing distortion.

## Software - 2025.04.16

Consulted repo notes and found that dithering with JACK (-zs flag) could improve audio quality. After further tweaking, found a .jackdrc config that fixed playback quality: `-P75 -p16 -dalsa -dhw:0 -r44100 -p1024 -n3 -o2 -zs`. This has resolved most audible distortion coming from the built-in output. SuperCollider now plays dynamically assigned samples over OSC without artifacts, as before this tweak it was an unusable mess of screetching.

This concludes a multi-day audio backend configuration process. Next steps are integrating control flow and layering logic, aka the aesthetics. In the meantime, I've also started on an enclosure.

## Hardware - 2025.04.17

I've built a prototype enclosure for the Raspberry Pi 4. It's a rather simple box with port holes and "Crowd Poetry" written on the front. I planned on making a tall cap for the SSD but I may separate that into another housing with a speaker.

## Infrastructure - 2025.04.18

Everything is managed from pm2, a process manager for Node.js. It calls the Loader script, a Tailscale tunnel, the backend API,and the SuperCollider server. Some basic infrastructure is in place so that crowd-poetry.michaelhemingway.com exposes the frontend, tunneling to the Pi itself. This is running on a Digital Ocean droplet, but could (and should) be a static site / A record.
Some issues persist in the loader starting up far before the sclang server is ready to receive OSC messages. With manual rebooting in an installation context, however, this is a non-issue.
