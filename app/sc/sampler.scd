(
s.waitForBoot {
    ~maxBuffers = 10;
    ~buffers = Array.fill(~maxBuffers, { Buffer.alloc(s, 1, 1) });
    ~bufIndex = 0;

    // Granular SynthDef
    SynthDef(\grainPlay, {
        |buf, rate = 1, dur = 0.1, density = 15, amp = 0.5, pan = 0.0|
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

    SynthDef(\bedlayer, {
        |buf, amp = 0.2, rate = 0.05, cutoff = 500|
        var sig;

        sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf) * rate, loop: 1);
        sig = LPF.ar(sig, cutoff);  // Low-pass to unify tone
        sig = sig ! 2; // stereo
        sig = sig * amp;

        Out.ar(0, sig);
    }).add;

    ~startBed = {
        var recentBuf = ~buffers[(~bufIndex - 1) % ~buffers.size];
        if (recentBuf.numFrames > 1) {
            Synth(\bedlayer, [
                \buf, recentBuf.bufnum,
                \rate, 0.02 + 0.03.rand,
                \amp, 0.1,
                \cutoff, 300 + 500.rand
            ]);
            "Bed layer started with buffer %".format(recentBuf.bufnum).postln;
        } {
            "No valid buffer yet for bed layer.".postln;
        }
    };

    // Sample loader
    ~loadSample = { |path|
        var bufnum = ~bufIndex % ~maxBuffers;
        ~buffers[bufnum].free;
        ~buffers[bufnum] = Buffer.read(s, path, action: {
            "Loaded % into buffer %".format(path, bufnum).postln;
            // If this is every 4th sample, start new bed
            if (~bufIndex % 4 == 0) {
                ~startBed.();
            };
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
                    \rate, [-1, -0.5, 0.5, 1].choose,
                    \dur, 0.1 + 0.1.rand,
                    \density, 5 + 10.rand,
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
