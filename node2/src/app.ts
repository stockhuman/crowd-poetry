import { AudioContext } from 'web-audio-api'
const context = new AudioContext()

context.outStream = process.stdout


var o = context.createOscillator()
o.type = "sine"
o.connect(context.destination)
o.start()