---
name: multi-speaker-synthesis
description: Multi-speaker coordination, turn-taking, and voice assignment.
---

# Multi-Speaker Synthesis Skill

## Purpose
Manages conversational turn-taking, distinct speaker identities, and acoustic separation across dialogue turns.

## Execution Procedure
1. Verify speaker identity consistency across episodes. Never swap voice models midway through a speaker dialogue turn.
2. Apply speaker-specific acoustic styling (pitch offset, speaking rate, EQ curve).
3. Ensure smooth acoustic cross-fading and natural conversational pauses (typically 300ms to 900ms between alternating speakers).

