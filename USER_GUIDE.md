# PodX — User Operating Guide

This guide provides end-to-end instructions for operating **PodX — Elite Knowledge AI Podcast Studio**.

---

## 1. Getting Started

When you launch PodX and open `http://127.0.0.1:8001`, the **Dashboard** displays live system health, available hardware resources (CPU, GPU VRAM, RAM, and disk space), recent episodes, and quick-action shortcuts.

---

## 2. Generating Your First Podcast

1. Navigate to **New Chat Studio** from the left navigation bar.
2. You can click the **Quick Template** pill (*"The Psychology of Elite Decision Making"*) or paste your custom script.
3. **Script Syntax**:
   - Use speaker tags: `M01: Dialogue` or `Alexander [calm, thoughtful]: Dialogue`.
   - Add stage directions in brackets: `[calm, thoughtful]`, `[confident]`, `[curious]`. PodX automatically parses these for emotion and pace, and strips them so they are **never spoken aloud**.
   - Add pauses: `[pause: 1.2 seconds]`. PodX inserts a true acoustic pause of that exact duration.
4. Click **Generate Podcast**.
5. The live progress card will stream real-time telemetry via Server-Sent Events (SSE), showing:
   - Script parsing & direction stripping
   - Voice casting & speaker separation
   - Turn-by-turn speech synthesis
   - Continuity verification
   - Audio mastering (-16 LUFS, true peak limiting)
   - Quality assurance audit
6. Once complete, the embedded player will immediately load the mastered audio.

---

## 3. Using the Multi-Track Studio

1. Navigate to **Podcast Studio**.
2. Select any episode from the archive.
3. The interactive multi-track timeline displays every spoken turn with its speaker badge, emotion tag, and duration.
4. **Selective Sentence Regeneration**: Click the circular refresh icon next to any sentence to re-synthesize that individual turn without re-rendering the rest of the 20–30 minute episode!

---

## 4. Exploring the Voice Library

1. Navigate to **Voice Library**.
2. Filter the 24 personas by gender (Male / Female) or accent (American, British, Indian).
3. Click the Play button on any card to listen to a 15–20 second acoustic sample.

---

## 5. Designing Custom AI Voices

1. Navigate to **AI Voice Designer**.
2. Enter a Persona Name (e.g. *"Sterling"*).
3. Select gender and accent.
4. Provide a natural-language description (e.g. *"A deep, reflective baritone speaking in an authoritative yet calm cadence"*).
5. Adjust the pitch offset and speaking rate sliders.
6. Click **Synthesize Voice Persona**. The custom voice will be saved into your library for future episodes.

---

## 6. Downloading Podcast Artifacts

In the persistent bottom player dock or in **Podcast History**:
- Click **MP3** to download the 320 kbps broadcast master.
- Click **WAV** to download the 24-bit PCM studio master.
- Click **SRT** or **VTT** to download subtitle files with millisecond speaker timestamps.
