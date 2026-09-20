# Maison Coilliot standard-mode Remotion spike

Status: technical diagnostic only; visual approval and publication remain human gates.

This bounded spike renders one deterministic five-second camera move from the
single supplied 864 x 1536 PNG. It does not use the rejected detail image, add
sound or text, publish media, or implement the future ANAD Reel engine.

## Camera and resolution

- composition: 720 x 1280, 30 fps, 150 frames (5 seconds)
- frames 0-18: full-facade reading hold
- frames 18-132: continuous cubic ease-in/out move
- frames 132-149: stable final framing
- start visual scale: 1.00x
- final visual scale relative to the start: 1.35x
- source-to-output raster scale at start: 720 / 864 = 0.8333x
- source-to-output raster scale at finish: 0.8333 x 1.35 = 1.125x
- native source region represented at finish: 640 x 1137.8 px

The final framing deliberately keeps facade context around the Coilliot sign.
The 12.5% raster enlargement at the finish is acceptable for a 720 x 1280
diagnostic, but it is not evidence that a 1080 x 1920 close-up is publishable.

## Commands

```bash
npm run spike:coilliot:render
npm run spike:coilliot:stills
```

Outputs are written under `video-spikes/maison-coilliot/output/`.
