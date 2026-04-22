# LinkedIn Organic Content Strategy for B2B SaaS

This repo is a research sprint on how strong B2B SaaS marketers, founders, and creator-operators use LinkedIn organic content to grow reach, build trust, and drive pipeline.

I chose this topic because it is practical. The best people in this space are not just sharing content advice in theory. They are posting consistently, building founder or executive brands in public, testing content-led growth ideas, and sharing lessons across LinkedIn, YouTube, podcasts, and newsletters.

The goal of this repo is to turn that body of work into a useful base for a future playbook.

## Start Here

Use [sources.md](./research/sources.md) as the main gateway into the project. It links out to each expert, their source URLs, and the matching files in this repo.


## What’s in this repo

- 10 experts with real operating experience in B2B SaaS content, founder branding, creator-led growth, or LinkedIn strategy
- Public LinkedIn post notes organized by author
- YouTube and podcast notes organized by video or episode
- YouTube en-orig caption files for all 10 selected videos, stored alongside the transcript notes
- Short source annotations on why each expert was included
- A lightweight transcript collection script and manifest for rerunning the process later

## Why these experts

I wanted a mix of people coming from slightly different perspectives:

- B2B SaaS content operators: Devin Reed, Lashay Lewis, Brendan Hufford
- Founder-brand and category builders: Dave Gerhardt, Udi Ledergor, Tom Hunt
- LinkedIn-native growth practitioners: Tas Bober, Alex Boyd, Richard van der Blom
- Zero-click and distribution thinkers: Amanda Natividad

Each person in this set actively publishes, teaches from real experience, and has enough public material available to support deeper synthesis later.

## Repo structure

- `research/sources.md` — main index of experts, with links, dates, and notes
- `research/linkedin-posts/` — one file per expert with notable recent LinkedIn posts
- `research/youtube-transcripts/` — one file per expert with video or episode notes and transcript references
- `research/other/` — methodology and collection notes
- `research/manifest.json` — rerunnable video manifest for transcript collection
- `scripts/fetch_youtube_transcripts.py` — transcript collection utility using `youtube-transcript-api`
- `scripts/download_youtube_cc.py`- manifest-driven YouTube caption downloader using yt-dlp

## Collection notes

I also set up a reusable YouTube transcript workflow in `scripts/` and `research/manifest.json`.

The transcript folder includes a mix of:

- public transcript pages when available
- public show notes and episode pages when full transcript retrieval was blocked
- links and metadata that make reruns possible from a different IP

That tradeoff keeps the repo honest while still preserving strong primary-source research.

## Outcome

This repo is meant to be a clean research base for a later synthesis into a practical LinkedIn organic content playbook for B2B SaaS.