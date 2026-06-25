---
name: media-content-operations
description: "Umbrella workflow for media tasks: YouTube transcripts, GIF search, Spotify control, audio feature/spectrogram analysis, and AI music generation services."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [media, youtube, gifs, spotify, audio, music-generation, transcripts]
    related_skills: []
---

# Media content operations

Use this umbrella for media retrieval, transformation, analysis, and playback/control workflows. Route by the artifact the user wants rather than by a narrow tool name.

## Routing map

| User need | Section |
|---|---|
| Summarize or transform YouTube videos | YouTube transcripts and content |
| Find/download reaction GIFs | GIF search |
| Generate songs/music from lyrics and tags | AI music generation |
| Inspect spectrograms or audio features | Audio analysis |
| Control playback, search tracks, or manage playlists | Spotify operations |

## Shared workflow

1. Identify the media source, destination, and deliverable: summary, transcript, GIF file/URL, playlist update, generated song, feature plot, etc.
2. Check credentials and local commands (`yt-dlp`, transcript tools, `jq`, Spotify auth, audio libraries, HeartMuLa credentials) before promising execution.
3. Prefer fetching structured metadata first, then the heavy media only if needed.
4. Verify tangible outputs: downloaded file exists, transcript length is non-zero, Spotify command returns a device/track result, or audio analysis/generation produces an artifact path/URL.

## Sections

### YouTube transcripts and content
Fetch transcript/captions first; summarize, turn into blogs/threads, or extract key claims with timestamps. If transcript is unavailable, report that rather than inventing content.

### GIF search
Use a GIF API/CLI workflow for query, selection, and download. Return the chosen GIF URL or local path and cite search terms used.

### AI music generation
For lyrics/music prompts, structure the song with sections, genre/mood/instrumentation/vocal cues, and generation tags. Produce several prompt variants when taste is subjective.

### Audio analysis
Use spectrogram/features workflows when the task is to understand audio characteristics. Preserve sample rate, windowing/features, and output image/data paths.

### Spotify operations
Check active device and auth. For destructive playlist edits, be explicit about target playlist/track IDs before changing them. Verify playback/search/queue results from the CLI/API.

## Preserved source playbooks

Full original skill packages from absorbed narrow skills are preserved under `references/source-packages/<skill-name>/`; former `SKILL.md` files are renamed `source-skill.md` so nested package notes do not register as separate skills.

## Verification checklist

- [ ] Media source and requested output are explicit.
- [ ] Required command/API credentials are available or blocker is reported.
- [ ] Returned URL/path/device/track/transcript/analysis output is verified.
