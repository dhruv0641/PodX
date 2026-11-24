---
name: podcast-script-interpretation
description: Autonomous parsing, speaker isolation, and direction stripping for podcast scripts.
---

# Podcast Script Interpretation Skill

## Purpose
Parses unstructured or structured multi-speaker podcast scripts into an intermediate representation (IR) of spoken dialogue, speaker IDs, emotion tags, pacing, and scene transitions.

## Key Rules
1. **Strict Script Mode**: Spoken dialogue must NEVER be altered, added, or deleted without explicit conversational adaptation permissions.
2. **Direction Stripping**: Directives like [calm, thoughtful], [pause: 1.5s], (laughter), *whispering* must NEVER be synthesized as spoken words.
3. **Dialogue Segmentation**: Break scripts into logical turns and sentence-level chunks at natural punctuation marks (. ? ! ;).
4. **Pause Ingestion**: Dedicated pause instructions translate into digital silence buffers inserted into the timeline.

