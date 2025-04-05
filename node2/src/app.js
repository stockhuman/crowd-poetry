"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var web_audio_api_1 = require("web-audio-api");
var context = new web_audio_api_1.AudioContext();
context.outStream = process.stdout;
var o = context.createOscillator();
o.type = "sine";
o.connect(context.destination);
o.start();
