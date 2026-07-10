---
license: mit
task_categories:
  - video-classification
  - other
tags:
  - physics
  - video-generation
  - benchmark
  - newtonian-mechanics
pretty_name: Morpheus Real-World Physics Videos
size_categories:
  - n<1K
---

# Morpheus — Real-World Physics Videos

Real-world reference footage for **Morpheus**, a benchmark that tests whether
video generative models (Wan, CogVideo, LTX-Video, COSMOS-predict1/2,
Pyramid-Flow, Veo3, Kling-Turbo, ...) obey Newtonian mechanics. Object
trajectories are extracted via SAM2 tracking and tested against physical laws
(energy/momentum conservation, equations of motion) rather than pixel-matched
to a single "correct" video.

This repo contains the **filmed real-world physics experiments** used as the
ground-truth reference split in the paper. Code to download, track, and score
this data lives in [`physics-from-video/Morpheus`](https://github.com/physics-from-video/Morpheus).

## Quickstart

```bash
pip install morpheus-physics   # or: pip install -e . from the Morpheus repo
export HF_TOKEN=hf_...         # optional — this dataset is public, only helps with rate limits
morpheus-download-data --local-dir ./data
morpheus-track-and-score --input-dir ./data --output-dir ./results \
    --methods real-world --calculate-scores
```

## Directory layout

```
real-world-cropped/<experiment>/<video_dir>/
    cropped_video.mp4          # the filmed clip, resized to 1280x1024
    info.json                  # experiment / model / path metadata
    frames_for_tracking/       # per-frame JPGs used for SAM2 tracking
```

## Experiments covered (16)

These are exactly the phenomenon buckets reported in the paper's real-world
results tables (`REAL_WORLD_DEFAULT_EXPERIMENTS` in `morpheus/taxonomy.py`):

| Phenomenon bucket | Experiments |
|---|---|
| Free fall | `falling_ball`, `falling_apple`, `falling_marker`, `falling_tape` |
| Projectile motion | `projectile` |
| Bouncing | `bouncing_ball` |
| Sliding / rolling object | `sliding_book`, `rolling_full_can`, `rolling_empty_can`, `rolling_orange` |
| Pendulum | `holonomic_pendulum` |
| Double pendulum | `double_pendulum` |
| Spring-mass | `spring` |
| Collision | `collision_equal`, `collision_big_hits_small`, `collision_small_hits_big` |

124 videos total. (The pipeline can also score a `non_holonomic_pendulum`
experiment, but it is intentionally excluded here — the paper's results tables
omit it, so it is not part of this release.)

## Citation

```bibtex
@inproceedings{tragoudaras2026evaluating,
  title={Evaluating Newtonian Mechanics in Video Generative Models with Real Physical Systems},
  author={Antonios Tragoudaras and Chenyu Zhang and Daniil Cherniavskii and Antonios Vozikis and Thijmen Nijdam and Derck W. E. Prinzhorn and Mark Bodracska and Nicu Sebe and Andrii Zadaianchuk and Stratis Gavves},
  booktitle={Forty-third International Conference on Machine Learning},
  year={2026},
  url={https://openreview.net/forum?id=f4xAzcMug6}
}
```
