"""
PodX Script Intelligence & Parser
Parses user-provided scripts, strips production directions, isolates speakers,
extracts emotional tags, and handles pauses.
"""
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ScriptSegmentParsed(BaseModel):
    sequence_index: int
    speaker_tag: str
    voice_profile_id: Optional[str] = None
    spoken_text: str
    raw_directions: Optional[str] = None
    emotion: str = "neutral"
    pace: float = 1.0
    pitch: float = 0.0
    pause_after_sec: float = 0.45

class ParsedPodcastScript(BaseModel):
    title: str = "Elite Knowledge Podcast"
    mode: str = "two-host"
    quality_mode: str = "Studio"
    speakers_detected: List[str] = []
    speaker_mapping: Dict[str, str] = {}
    total_segments: int = 0
    estimated_duration_sec: float = 0.0
    segments: List[ScriptSegmentParsed] = []
    metadata_headers: Dict[str, str] = {}

class ScriptParser:
    """
    Intelligent parser for PodX podcast scripts.
    Distinguishes spoken dialogue from stage directions and control tags.
    """
    # Header regex: e.g., TITLE: The Psychology of Elite Decision Making
    HEADER_REGEX = re.compile(r"^(TITLE|PODCAST TITLE|MODE|DURATION|QUALITY|LANGUAGE|HOST 1|HOST 2|STYLE):\s*(.+)$", re.IGNORECASE)
    
    # Pause regex: e.g., [pause: 1.2 seconds] or [pause: 0.8s]
    PAUSE_REGEX = re.compile(r"\[pause:\s*([\d\.]+)\s*(?:seconds?|s)?\]", re.IGNORECASE)
    
    # Speaker turn regex: e.g. M01 [calm, thoughtful]: Dialogue
    # or Alexander [confident]: Dialogue
    # or Sophia: Dialogue
    SPEAKER_LINE_REGEX = re.compile(r"^([A-Za-z0-9_\-\s]{1,30}?)(?:\s*\[(.*?)\])?\s*:\s*(.+)$")
    
    # Stage direction inline stripping: [whispering], (laughter), *laughs*
    INLINE_DIRECTION_REGEX = re.compile(r"\[(?!pause:)[^\]]+\]|\([^\)]+\)|\*[^\*]+\*")

    @classmethod
    def parse(cls, script_text: str, strict_mode: bool = True) -> ParsedPodcastScript:
        lines = script_text.strip().splitlines()
        headers = {}
        raw_turns = []
        pending_pause = 0.45  # Default conversational pause

        for line_num, raw_line in enumerate(lines):
            line = raw_line.strip()
            if not line:
                continue

            # Check for header metadata
            header_match = cls.HEADER_REGEX.match(line)
            if header_match:
                key = header_match.group(1).upper()
                val = header_match.group(2).strip()
                headers[key] = val
                continue

            # Check for standalone pause directive
            pause_match = cls.PAUSE_REGEX.search(line)
            if pause_match and len(line) < 35:
                try:
                    pending_pause = float(pause_match.group(1))
                    if raw_turns:
                        raw_turns[-1]["pause_after_sec"] = pending_pause
                except ValueError:
                    pass
                continue

            # Check for speaker dialogue line
            speaker_match = cls.SPEAKER_LINE_REGEX.match(line)
            if speaker_match:
                speaker_raw = speaker_match.group(1).strip()
                directions = speaker_match.group(2).strip() if speaker_match.group(2) else ""
                dialogue = speaker_match.group(3).strip()

                # Clean dialogue of any inline brackets
                clean_dialogue = cls.INLINE_DIRECTION_REGEX.sub("", dialogue).strip()
                clean_dialogue = re.sub(r"\s+", " ", clean_dialogue)

                if clean_dialogue:
                    emotion, pace, pitch = cls._interpret_directions(directions)
                    raw_turns.append({
                        "speaker_tag": speaker_raw,
                        "spoken_text": clean_dialogue,
                        "raw_directions": directions,
                        "emotion": emotion,
                        "pace": pace,
                        "pitch": pitch,
                        "pause_after_sec": pending_pause
                    })
                    pending_pause = 0.45  # Reset to default
            else:
                # Continuation of previous speaker dialogue or narrative
                if raw_turns:
                    clean_cont = cls.INLINE_DIRECTION_REGEX.sub("", line).strip()
                    if clean_cont:
                        raw_turns[-1]["spoken_text"] += " " + clean_cont
                else:
                    # Unadorned line without speaker prefix: treat as Narrator / Host
                    clean_line = cls.INLINE_DIRECTION_REGEX.sub("", line).strip()
                    if clean_line:
                        raw_turns.append({
                            "speaker_tag": "Narrator",
                            "spoken_text": clean_line,
                            "raw_directions": "",
                            "emotion": "neutral",
                            "pace": 1.0,
                            "pitch": 0.0,
                            "pause_after_sec": pending_pause
                        })
                        pending_pause = 0.45

        # Split turns into sentence-level segments for long-form stability
        parsed_segments: List[ScriptSegmentParsed] = []
        seq_idx = 0
        total_words = 0
        speakers_set = set()

        for turn in raw_turns:
            speakers_set.add(turn["speaker_tag"])
            sentences = cls._split_into_sentences(turn["spoken_text"])
            
            for s_i, sent in enumerate(sentences):
                is_last_in_turn = (s_i == len(sentences) - 1)
                pause_sec = turn["pause_after_sec"] if is_last_in_turn else 0.25
                total_words += len(sent.split())

                parsed_segments.append(
                    ScriptSegmentParsed(
                        sequence_index=seq_idx,
                        speaker_tag=turn["speaker_tag"],
                        voice_profile_id=cls._resolve_profile_id(turn["speaker_tag"]),
                        spoken_text=sent,
                        raw_directions=turn["raw_directions"],
                        emotion=turn["emotion"],
                        pace=turn["pace"],
                        pitch=turn["pitch"],
                        pause_after_sec=pause_sec
                    )
                )
                seq_idx += 1

        # Calculate estimated duration (approx 150 words per minute = 2.5 words per sec + pauses)
        total_pause = sum(s.pause_after_sec for s in parsed_segments)
        est_duration = (total_words / 2.5) + total_pause

        title = headers.get("TITLE") or headers.get("PODCAST TITLE") or "Elite Knowledge Podcast Episode"
        mode = headers.get("MODE") or ("two-host" if len(speakers_set) >= 2 else "solo")
        quality = headers.get("QUALITY") or "Studio"

        return ParsedPodcastScript(
            title=title,
            mode=mode,
            quality_mode=quality,
            speakers_detected=sorted(list(speakers_set)),
            total_segments=len(parsed_segments),
            estimated_duration_sec=round(est_duration, 2),
            segments=parsed_segments,
            metadata_headers=headers
        )

    @staticmethod
    def _interpret_directions(directions: str):
        if not directions:
            return "neutral", 1.0, 0.0
        
        d_lower = directions.lower()
        emotion = "neutral"
        pace = 1.0
        pitch = 0.0

        if any(w in d_lower for w in ["whisper", "soft", "intimate"]):
            emotion = "whisper"
            pace = 0.88
            pitch = -1.0
        elif any(w in d_lower for w in ["laugh", "chuckle", "humorous", "sarcastic", "playful"]):
            emotion = "playful"
            pace = 1.06
            pitch = 0.8
        elif any(w in d_lower for w in ["urgent", "dramatic", "intense"]):
            emotion = "intense"
            pace = 1.12
            pitch = 1.2
        elif any(w in d_lower for w in ["sad", "somber", "melancholy", "grave"]):
            emotion = "somber"
            pace = 0.88
            pitch = -1.5
        elif any(w in d_lower for w in ["thoughtful", "reflective", "calm", "philosophical", "contemplative"]):
            emotion = "thoughtful"
            pace = 0.93
            pitch = -0.6
        elif any(w in d_lower for w in ["curious", "analytical", "inquisitive"]):
            emotion = "analytical"
            pace = 1.03
            pitch = 0.6
        elif any(w in d_lower for w in ["confident", "authoritative", "measured", "decisive"]):
            emotion = "confident"
            pace = 0.97
            pitch = -1.0
        elif any(w in d_lower for w in ["energetic", "excited", "passionate", "inspirational", "uplifting"]):
            emotion = "excited"
            pace = 1.08
            pitch = 1.0
        elif any(w in d_lower for w in ["serious", "sober", "firm"]):
            emotion = "serious"
            pace = 0.92
            pitch = -1.2
        elif any(w in d_lower for w in ["warm", "friendly", "empathetic", "kind"]):
            emotion = "friendly"
            pace = 0.98
            pitch = 0.2

        return emotion, pace, pitch

    @staticmethod
    def _split_into_sentences(text: str) -> List[str]:
        # Split on sentence boundaries (. ? ! ;) without breaking decimals or abbreviations
        raw_chunks = re.split(r"(?<=[.?!;])\s+(?=[A-Z0-9\"])", text.strip())
        results = []
        for c in raw_chunks:
            c = c.strip()
            if c:
                results.append(c)
        return results if results else [text.strip()]

    @staticmethod
    def _resolve_profile_id(speaker_tag: str) -> str:
        tag_upper = speaker_tag.strip().upper()
        # Direct ID mapping (e.g. M01, F01)
        if re.match(r"^[MF]\d{2}$", tag_upper):
            return tag_upper
        
        # Name to ID matching
        name_map = {
            "ALEXANDER": "M01",
            "JAMES": "M02",
            "ETHAN": "M03",
            "MARCUS": "M04",
            "OLIVER": "M05",
            "DANIEL": "M06",
            "ADRIAN": "M07",
            "VICTOR": "M08",
            "NOAH": "M09",
            "ARJUN": "M10",
            "SEBASTIAN": "M11",
            "GABRIEL": "M12",
            "SOPHIA": "F01",
            "OLIVIA": "F02",
            "EMMA": "F03",
            "ISABELLA": "F04",
            "AVA": "F05",
            "VICTORIA": "F06",
            "AMELIA": "F07",
            "ELENA": "F08",
            "MAYA": "F09",
            "CHARLOTTE": "F10",
            "AURORA": "F11",
            "CLAIRE": "F12",
            "HOST 1": "M01",
            "HOST 2": "F01",
            "NARRATOR": "M06"
        }
        for name, pid in name_map.items():
            if name in tag_upper:
                return pid
        return "M01" if "M" in tag_upper else "F01"
