---
name: long-form-speech-generation
description: Reliable generation of 20-30+ minute podcast episodes through checkpointing and caching.
---

# Long-Form Speech Generation Skill

## Purpose
Orchestrates generation of full-length episodes (20-30 minutes, 3,000 to 6,000+ words) without memory degradation, audio drift, or loss of state.

## Core Directives
1. **Chunking**: Chunk by natural sentence and speaker boundaries, never arbitrary token counts.
2. **Segment Caching**: Store each rendered audio segment as a standalone .wav keyed by hash of (text, voice_id, speed, pitch, emotion).
3. **Resumability**: Store segment progress in SQLite. If interrupted, generation resumes from the exact unrendered segment.
4. **Selective Regeneration**: Re-render individual sentences or turns without regenerating the entire podcast.

