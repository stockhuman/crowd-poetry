(
s.waitForBoot {
    ~maxBuffers = 10;
    ~buffers = Array.fill(~maxBuffers, { Buffer.alloc(s, 1, 1) });
    ~bufIndex = 0;

    // Granular SynthDef
    SynthDef(\grainPlay, {
        |buf, rate = 1, dur = 0.1, density = 20, amp = 0.5, pan = 0.0|
        var trig, pos, sig;

        trig = Impulse.kr(density);
        pos = TRand.kr(0, BufDur.kr(buf), trig);

        sig = TGrains.ar(
            2,
            trig,
            buf,
            rate,
            pos,
            dur,
            pan,
            amp
        );

        Out.ar(0, sig);
    }).add;

    // Sample loader
    ~loadSample = { |path|
        var bufnum = ~bufIndex % ~maxBuffers;
        ~buffers[bufnum].free;
        ~buffers[bufnum] = Buffer.read(s, path, action: {
            "Loaded % into buffer %".format(path, bufnum).postln;
        });
        ~bufIndex = ~bufIndex + 1;
    };

    // Random grain loop spawner
    ~grainLoop = Routine {
        inf.do {
            var valid = ~buffers.select({ |b| b.numFrames > 1 });
            if (valid.notEmpty) {
                var buf = valid.choose;

                Synth(\grainPlay, [
                    \buf, buf.bufnum,
                    \rate, [-1, -0.5, 0.5, 1, 1.5].choose,
                    \dur, 0.03 + 0.1.rand,
                    \density, 10 + 40.rand,
                    \amp, 0.2 + 0.3.rand,
                    \pan, -1.0 + 2.0.rand
                ]);
            };
            (5 + 5.rand).wait; // wait time before next grain cloud
        }
    };

    ~grainLoop.play;

    // OSC sample loader
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

    "Granular loop engine running on port 57120".postln;
};
)
