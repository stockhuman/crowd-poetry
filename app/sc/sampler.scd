(
s.waitForBoot {
    // Create 5 empty buffers
    ~buffers = Array.fill(5, { Buffer.alloc(s, 1, 1) });
    ~bufIndex = 0;

    // SynthDef for playback
    SynthDef(\playbuf, {
        |buf, amp = 0.5|
        var sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf), doneAction: 2);
        Out.ar(0, sig * amp ! 2);
    }).add;

    // Function to load sample
    ~loadSample = { |path|
        var bufnum = ~bufIndex % ~buffers.size;
        ~buffers[bufnum].free; // free old buffer just in case
        ~buffers[bufnum] = Buffer.read(s, path, action: {
            "Loaded % into buffer %".format(path, bufnum).postln;
            Synth(\playbuf, [\buf, ~buffers[bufnum].bufnum]);
        });
        ~bufIndex = ~bufIndex + 1;
    };

    // OSC listener
    ~oscFunc = OSCdef.new(
        \loadsample,
        { |msg|
            var path = msg[1].asString;
            path.postln;
            ~loadSample.(path);
        },
        '/loadsample',
        recvPort: 57120
    );

    "Sampler ready on port 57120".postln;
};
)