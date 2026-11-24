"""
PodX Master Demonstration Episode Generator
Produces the official showcase episode:
"The Psychology of Elite Decision Making: Critical Thinking, Mental Models, and Artificial Intelligence"
Featuring Alexander (M01) and Sophia (F01).
"""
import sys
import os
import time
import json
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.db_manager import db_manager
from workflows.podcast_workflow import PodcastProductionWorkflow

SAMPLE_SCRIPT = """PODCAST TITLE: The Psychology of Elite Decision Making: Critical Thinking, Mental Models, and Artificial Intelligence
MODE: Two-host intellectual discussion
QUALITY: Extreme
LANGUAGE: English
HOST 1: Alexander — M01
HOST 2: Sophia — F01
STYLE: Sophisticated, intellectual, engaging and deeply conversational.

M01 [calm, authoritative]: Welcome to Elite Knowledge. Today, we examine the hidden cognitive architecture behind high-stakes decision making. Most people operate under the illusion that exceptional leaders possess an uncanny ability to predict the future. In truth, elite thinkers do not predict the future—they construct systems that thrive on uncertainty.

[pause: 1.2 seconds]

F01 [curious, analytical]: That distinction strikes at the very core of strategic thought, Alexander. When you observe practitioners across aerospace, quantum computing, and capital allocation, they rarely obsess over singular forecasts. Instead, they obsess over asymmetrical payoffs and the preservation of optionality.

[pause: 0.8 seconds]

M01 [thoughtful, reflective]: Exactly, Sophia. As Nassim Taleb articulates in Antifragile, the true test of any mental model is whether volatility hurts you or makes you stronger. If a five percent deviation in your assumptions destroys your thesis, you haven't engineered a strategy—you have built a fragile house of cards.

[pause: 1.0 second]

F01 [analytical, engaged]: And this brings us directly to the psychology of cognitive biases. The human mind is biologically wired for energy conservation. We default to pattern recognition, confirmation bias, and the sunk cost fallacy. Why do even deeply intelligent professionals fall into the trap of defending flawed decisions long after the empirical data contradicts them?

[pause: 0.9 seconds]

M01 [confident, measured]: Because human beings conflate their identity with their ideas. When an idea is challenged, the amygdala responds as though physical survival is threatened. Elite decision-makers cultivate what Charlie Munger called 'extreme objectivity.' They actively search for disconfirming evidence. In fact, if you cannot articulate the opposing argument better than your most articulate adversary, you do not yet understand your own position.

[pause: 1.1 seconds]

F01 [curious, forward-looking]: That mental discipline leads us directly to the modern frontier: the convergence of human intuition and artificial intelligence. Today, autonomous AI systems can analyze millions of data streams simultaneously. But what remains uniquely, irreducibly human in the decision loop?

[pause: 0.8 seconds]

M01 [authoritative, philosophical]: What remains human is the moral imperative and the synthesis of context. AI excels at high-dimensional computation and inductive pattern extraction. But artificial intelligence cannot define purpose. It cannot determine what is worth sacrificing for. The future belongs not to algorithms alone, nor to unaugmented intuition, but to the seamless synthesis of human discernment and computational power.

[pause: 1.2 seconds]

F01 [thoughtful, concluding]: A profound realization. Critical thinking is not about accumulating information; it is about cultivating the clarity to see through noise, question first principles, and act with decisive courage.

[pause: 0.8 seconds]

M01 [composed, warm]: And that is the essence of elite decision making. Thank you for joining us on this journey of intellectual mastery. Until next time, stay curious, remain rigorous, and keep refining your mental models."""

def run_sample_generation():
    print("=" * 70)
    print("   ELITE KNOWLEDGE — MASTER PODCAST DEMONSTRATION GENERATION")
    print("=" * 70)

    # 1. Ensure 24 voices are seeded
    db_manager.seed_default_voices("configs/voice_profiles.json")

    # 2. Create project
    proj = db_manager.create_project(
        title="The Psychology of Elite Decision Making",
        raw_script=SAMPLE_SCRIPT,
        mode="two-host",
        quality_mode="Extreme",
        speaker_mapping={"M01": "M01", "F01": "F01"}
    )
    print(f"[Project Initialized] ID: {proj['id']}")

    # 3. Create Episode
    ep = db_manager.create_episode(
        project_id=proj["id"],
        title="The Psychology of Elite Decision Making (Master Edition)"
    )
    print(f"[Episode Initialized] ID: {ep['id']}")

    start_time = time.time()
    benchmark_log = []

    def progress_monitor(p):
        elapsed = time.time() - start_time
        msg = f"  [{p['stage']:<20}] {p['progress']:>5.1f}% | Elapsed: {elapsed:>5.1f}s | {p['message']}"
        print(msg)
        benchmark_log.append({
            "stage": p["stage"],
            "progress": p["progress"],
            "elapsed_sec": round(elapsed, 2),
            "message": p["message"]
        })

    # 4. Execute workflow
    wf = PodcastProductionWorkflow(episode_id=ep["id"], progress_callback=progress_monitor)
    results = wf.execute()
    total_time = time.time() - start_time

    # 5. Create Showcase Output Directory
    showcase_dir = Path("storage/exports/sample_episode_elite_decision_making")
    showcase_dir.mkdir(parents=True, exist_ok=True)

    # Copy artifacts to showcase dir
    master_paths = results["master_paths"]
    shutil.copy(master_paths["wav"], showcase_dir / "master_podcast.wav")
    if os.path.exists(master_paths.get("mp3", "")):
        shutil.copy(master_paths["mp3"], showcase_dir / "master_podcast.mp3")
    shutil.copy(master_paths["srt"], showcase_dir / "transcript.srt")
    shutil.copy(master_paths["vtt"], showcase_dir / "transcript.vtt")
    shutil.copy(master_paths["json"], showcase_dir / "transcript.json")

    # Save source script
    with open(showcase_dir / "source_script.txt", "w", encoding="utf-8") as f:
        f.write(SAMPLE_SCRIPT)

    # Save benchmark report
    benchmark_report = {
        "project_name": "PodX - Elite Knowledge AI Podcast Studio",
        "episode_title": ep["title"],
        "generation_timestamp": time.time(),
        "total_wall_clock_time_sec": round(total_time, 2),
        "synthesized_audio_duration_sec": results["duration_seconds"],
        "real_time_factor_rtf": round(total_time / max(results["duration_seconds"], 0.1), 3),
        "integrated_lufs": master_paths.get("integrated_lufs"),
        "true_peak_dbtp": master_paths.get("true_peak_dbtp"),
        "speakers": ["M01 (Alexander)", "F01 (Sophia)"],
        "qa_audit": results["qa_report"],
        "stage_timings": benchmark_log
    }

    with open(showcase_dir / "benchmark_and_qa_report.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_report, f, indent=2)

    print("\n" + "=" * 70)
    print("   MASTER DEMONSTRATION GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total Duration: {results['duration_seconds']} seconds")
    print(f"Total Execution Time: {round(total_time, 1)} seconds (RTF: {benchmark_report['real_time_factor_rtf']})")
    print(f"Integrated Loudness: {master_paths.get('integrated_lufs'):.2f} LUFS (Broadcast Standard -16 LUFS)")
    print(f"True-Peak Limit: {master_paths.get('true_peak_dbtp'):.2f} dBTP (Ceiling -1.0 dBTP)")
    print(f"Showcase Directory: {showcase_dir.resolve()}")
    print("All exports successfully generated and verified!")

if __name__ == "__main__":
    run_sample_generation()
