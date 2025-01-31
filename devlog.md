# Dev Log

My strategy in building out the basic architecture is of course first exploring what's out there in terms of APIs for TikTok et al. Unfortunately it seems the [Research API](https://developers.tiktok.com/products/research-api/) is not available in Canada. 
Thankfully, access by unofficial means seems to be available though 3rd party libraries (primarily in Python), chiefly via [PykTok](https://pypi.org/project/pyktok/).

## Hardware Exploration

I am going to first test the Olimex A20-OlinuXino. This board offers a linux platform for python scripting which is likely going to be necessary. The plans for more low-level hardware are unlikely to proceed given the API and the A/V complexity. On the other hand, this opens up the possiblity of using a display.

--

UPDATE: The A20-OlinuXino-LIME2 is not powerful enough to run pyktok. I will be switching to a Raspberry Pi 5.