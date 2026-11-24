"""
Unit tests for PodX Script Intelligence & Direction Parser.
"""
import pytest
from audio_engine.script_parser import ScriptParser

def test_script_header_parsing():
    script = """PODCAST TITLE: Autonomous Systems of Tomorrow
MODE: Two-host intellectual discussion
QUALITY: Extreme

M01 [calm]: Autonomous agents represent a fundamental shift in computing.
F01 [analytical]: Indeed, from procedural code to goal-driven execution."""

    parsed = ScriptParser.parse(script)
    assert parsed.title == "Autonomous Systems of Tomorrow"
    assert parsed.mode == "Two-host intellectual discussion"
    assert parsed.quality_mode == "Extreme"
    assert len(parsed.speakers_detected) == 2
    assert "M01" in parsed.speakers_detected
    assert "F01" in parsed.speakers_detected

def test_direction_stripping_and_pause_extraction():
    script = """M01 [calm, thoughtful]: The human mind defaults to confirmation bias.
[pause: 1.5 seconds]
F01 [curious, analytical]: Why is that the case? (laughs) *whispering*"""

    parsed = ScriptParser.parse(script)
    assert len(parsed.segments) >= 2
    
    # First segment: directions stripped from spoken text
    seg0 = parsed.segments[0]
    assert "calm" not in seg0.spoken_text
    assert "thoughtful" not in seg0.spoken_text
    assert seg0.spoken_text == "The human mind defaults to confirmation bias."
    assert seg0.emotion == "thoughtful"
    assert seg0.pause_after_sec == 1.5

    # Second segment: inline laughter and asterisks stripped
    seg1 = parsed.segments[1]
    assert "laughs" not in seg1.spoken_text
    assert "whispering" not in seg1.spoken_text
    assert "Why is that the case?" in seg1.spoken_text

def test_strict_script_preservation():
    text = "M01: Precision is non-negotiable in safety-critical systems."
    parsed = ScriptParser.parse(text)
    assert parsed.segments[0].spoken_text == "Precision is non-negotiable in safety-critical systems."
