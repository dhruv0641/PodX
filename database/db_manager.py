"""
PodX Native SQLite WAL Database Engine
Zero-dependency, high-reliability persistence engine using Python's built-in sqlite3.
Enforces Write-Ahead Logging (WAL) mode, foreign keys, and safe multi-threaded transactions.
"""
import os
import sys
import json
import sqlite3
import uuid
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class DatabaseManager:
    """
    Thread-safe SQLite database manager operating in WAL mode.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            db_path = str(base_dir / "storage" / "podx.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode and performance pragmas
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def _init_schema(self):
        with self.get_connection() as conn:
            # 1. Conversations
            conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                pinned INTEGER DEFAULT 0,
                meta_info TEXT DEFAULT '{}'
            );
            """)

            # 2. Chat Messages
            conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                intent TEXT,
                parsed_metadata TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
            """)

            # 3. Voice Profiles
            conn.execute("""
            CREATE TABLE IF NOT EXISTS voice_profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                accent TEXT NOT NULL,
                language TEXT DEFAULT 'en-US',
                description TEXT,
                tags TEXT DEFAULT '[]',
                pitch_offset REAL DEFAULT 0.0,
                speed_factor REAL DEFAULT 1.0,
                preferred_provider TEXT DEFAULT 'kokoro',
                provider_voice_id TEXT DEFAULT 'am_adam',
                edge_voice_id TEXT DEFAULT 'en-US-GuyNeural',
                preview_audio_path TEXT,
                is_custom INTEGER DEFAULT 0,
                created_at REAL NOT NULL
            );
            """)

            # 4. Podcast Projects
            conn.execute("""
            CREATE TABLE IF NOT EXISTS podcast_projects (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                title TEXT NOT NULL,
                topic TEXT,
                raw_script TEXT NOT NULL,
                mode TEXT DEFAULT 'two-host',
                quality_mode TEXT DEFAULT 'Studio',
                strict_script_mode INTEGER DEFAULT 1,
                estimated_duration_sec REAL DEFAULT 0.0,
                speaker_mapping TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
            );
            """)

            # 5. Podcast Episodes
            conn.execute("""
            CREATE TABLE IF NOT EXISTS podcast_episodes (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                progress_percent REAL DEFAULT 0.0,
                current_stage TEXT DEFAULT 'Queued',
                duration_seconds REAL DEFAULT 0.0,
                total_segments INTEGER DEFAULT 0,
                rendered_segments INTEGER DEFAULT 0,
                master_wav_path TEXT,
                master_mp3_path TEXT,
                srt_path TEXT,
                vtt_path TEXT,
                transcript_json_path TEXT,
                integrated_lufs REAL,
                true_peak_dbtp REAL,
                qa_status TEXT DEFAULT 'pending',
                qa_report TEXT DEFAULT '{}',
                error_message TEXT,
                created_at REAL NOT NULL,
                completed_at REAL,
                FOREIGN KEY (project_id) REFERENCES podcast_projects(id) ON DELETE CASCADE
            );
            """)

            # 6. Script Segments
            conn.execute("""
            CREATE TABLE IF NOT EXISTS script_segments (
                id TEXT PRIMARY KEY,
                episode_id TEXT NOT NULL,
                sequence_index INTEGER NOT NULL,
                speaker_tag TEXT NOT NULL,
                voice_profile_id TEXT NOT NULL,
                spoken_text TEXT NOT NULL,
                raw_directions TEXT,
                emotion TEXT DEFAULT 'neutral',
                pace REAL DEFAULT 1.0,
                pitch REAL DEFAULT 0.0,
                pause_after_sec REAL DEFAULT 0.45,
                status TEXT DEFAULT 'pending',
                audio_path TEXT,
                duration_sec REAL DEFAULT 0.0,
                retry_count INTEGER DEFAULT 0,
                qa_wer REAL,
                FOREIGN KEY (episode_id) REFERENCES podcast_episodes(id) ON DELETE CASCADE
            );
            """)

            # 7. Fine-Tuning Datasets
            conn.execute("""
            CREATE TABLE IF NOT EXISTS finetuning_datasets (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                speaker_name TEXT NOT NULL,
                description TEXT,
                consent_confirmed INTEGER DEFAULT 0,
                provenance_source TEXT,
                total_audio_duration_sec REAL DEFAULT 0.0,
                total_samples_count INTEGER DEFAULT 0,
                dataset_manifest_path TEXT,
                status TEXT DEFAULT 'ready',
                created_at REAL NOT NULL
            );
            """)

            # 8. Fine-Tuning Jobs
            conn.execute("""
            CREATE TABLE IF NOT EXISTS finetuning_jobs (
                id TEXT PRIMARY KEY,
                dataset_id TEXT NOT NULL,
                base_model TEXT DEFAULT 'qwen3-tts-0.6b',
                status TEXT DEFAULT 'queued',
                progress_percent REAL DEFAULT 0.0,
                current_epoch INTEGER DEFAULT 0,
                total_epochs INTEGER DEFAULT 10,
                current_loss REAL,
                loss_history TEXT DEFAULT '[]',
                output_checkpoint_path TEXT,
                error_message TEXT,
                created_at REAL NOT NULL,
                completed_at REAL,
                FOREIGN KEY (dataset_id) REFERENCES finetuning_datasets(id) ON DELETE CASCADE
            );
            """)

            # 9. System Logs
            conn.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                level TEXT NOT NULL,
                source TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT DEFAULT '{}'
            );
            """)
            conn.commit()

    # --- Seeding Helpers ---
    def seed_default_voices(self, voices_json_path: str):
        if not os.path.exists(voices_json_path):
            return
        with open(voices_json_path, "r", encoding="utf-8") as f:
            voices = json.load(f)

        now = time.time()
        with self.get_connection() as conn:
            for v in voices:
                existing = conn.execute("SELECT id FROM voice_profiles WHERE id = ?", (v["id"],)).fetchone()
                if not existing:
                    conn.execute("""
                    INSERT INTO voice_profiles (
                        id, name, gender, accent, language, description, tags,
                        pitch_offset, speed_factor, preferred_provider, provider_voice_id,
                        edge_voice_id, is_custom, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        v["id"], v["name"], v["gender"], v["accent"], v.get("language", "en-US"),
                        v.get("description", ""), json.dumps(v.get("tags", [])),
                        v.get("pitch_offset", 0.0), v.get("speed_factor", 1.0),
                        v.get("preferred_provider", "kokoro"),
                        v.get("provider_voice_id", "am_adam"),
                        v.get("edge_voice_id", "en-US-GuyNeural"),
                        0, now
                    ))
            conn.commit()

    # --- Voice Profile CRUD ---
    def get_all_voices(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM voice_profiles ORDER BY id ASC").fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
                item["is_custom"] = bool(item.get("is_custom"))
                results.append(item)
            return results

    def get_voice(self, voice_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM voice_profiles WHERE id = ?", (voice_id,)).fetchone()
            if not r:
                return None
            item = dict(r)
            item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
            item["is_custom"] = bool(item.get("is_custom"))
            return item

    # --- Conversation CRUD ---
    def create_conversation(self, title: str = "New Podcast Session") -> Dict[str, Any]:
        cid = str(uuid.uuid4())
        now = time.time()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO conversations (id, title, created_at, updated_at, pinned, meta_info)
            VALUES (?, ?, ?, ?, 0, '{}')
            """, (cid, title, now, now))
            conn.commit()
        return self.get_conversation(cid)

    def get_all_conversations(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
            return [dict(r) for r in rows]

    def get_conversation(self, cid: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM conversations WHERE id = ?", (cid,)).fetchone()
            if not r:
                return None
            res = dict(r)
            res["meta_info"] = json.loads(res["meta_info"]) if res.get("meta_info") else {}
            # Fetch messages
            msgs = conn.execute(
                "SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at ASC", (cid,)
            ).fetchall()
            res["messages"] = [dict(m) for m in msgs]
            return res

    def add_message(self, cid: str, role: str, content: str, intent: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        mid = str(uuid.uuid4())
        now = time.time()
        meta_str = json.dumps(metadata or {})
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO chat_messages (id, conversation_id, role, content, intent, parsed_metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (mid, cid, role, content, intent, meta_str, now))
            conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, cid))
            conn.commit()
        return {"id": mid, "conversation_id": cid, "role": role, "content": content, "intent": intent, "created_at": now}

    # --- Project & Episode CRUD ---
    def create_project(self, title: str, raw_script: str, conversation_id: Optional[str] = None, mode: str = "two-host", quality_mode: str = "Studio", speaker_mapping: Optional[Dict] = None) -> Dict[str, Any]:
        pid = str(uuid.uuid4())
        now = time.time()
        map_str = json.dumps(speaker_mapping or {})
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO podcast_projects (id, conversation_id, title, raw_script, mode, quality_mode, speaker_mapping, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (pid, conversation_id, title, raw_script, mode, quality_mode, map_str, now, now))
            conn.commit()
        return self.get_project(pid)

    def get_project(self, pid: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM podcast_projects WHERE id = ?", (pid,)).fetchone()
            if not r:
                return None
            res = dict(r)
            res["speaker_mapping"] = json.loads(res["speaker_mapping"]) if res.get("speaker_mapping") else {}
            episodes = conn.execute("SELECT * FROM podcast_episodes WHERE project_id = ? ORDER BY created_at DESC", (pid,)).fetchall()
            res["episodes"] = [dict(e) for e in episodes]
            return res

    def create_episode(self, project_id: str, title: str) -> Dict[str, Any]:
        eid = str(uuid.uuid4())
        now = time.time()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO podcast_episodes (id, project_id, title, status, progress_percent, current_stage, created_at)
            VALUES (?, ?, ?, 'pending', 0.0, 'Queued', ?)
            """, (eid, project_id, title, now))
            conn.commit()
        return self.get_episode(eid)

    def get_episode(self, eid: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM podcast_episodes WHERE id = ?", (eid,)).fetchone()
            if not r:
                return None
            res = dict(r)
            res["qa_report"] = json.loads(res["qa_report"]) if res.get("qa_report") else {}
            segs = conn.execute("SELECT * FROM script_segments WHERE episode_id = ? ORDER BY sequence_index ASC", (eid,)).fetchall()
            res["segments"] = [dict(s) for s in segs]
            return res

    def update_episode_status(self, eid: str, status: str, progress: float, stage: str, error_message: Optional[str] = None):
        with self.get_connection() as conn:
            conn.execute("""
            UPDATE podcast_episodes 
            SET status = ?, progress_percent = ?, current_stage = ?, error_message = ?
            WHERE id = ?
            """, (status, progress, stage, error_message, eid))
            conn.commit()

    def update_episode_completion(self, eid: str, duration_sec: float, master_wav: str, master_mp3: str, srt: str, vtt: str, json_path: str, lufs: float, peak: float, qa_report: Dict):
        now = time.time()
        qa_str = json.dumps(qa_report or {})
        with self.get_connection() as conn:
            conn.execute("""
            UPDATE podcast_episodes 
            SET status = 'completed', progress_percent = 100.0, current_stage = 'Master Completed',
                duration_seconds = ?, master_wav_path = ?, master_mp3_path = ?, srt_path = ?,
                vtt_path = ?, transcript_json_path = ?, integrated_lufs = ?, true_peak_dbtp = ?,
                qa_status = ?, qa_report = ?, completed_at = ?
            WHERE id = ?
            """, (duration_sec, master_wav, master_mp3, srt, vtt, json_path, lufs, peak, qa_report.get("status", "passed"), qa_str, now, eid))
            conn.commit()

    # --- Segments ---
    def set_episode_segments(self, eid: str, segments: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM script_segments WHERE episode_id = ?", (eid,))
            for s in segments:
                sid = s.get("id") or str(uuid.uuid4())
                conn.execute("""
                INSERT INTO script_segments (
                    id, episode_id, sequence_index, speaker_tag, voice_profile_id,
                    spoken_text, raw_directions, emotion, pace, pitch, pause_after_sec, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                """, (
                    sid, eid, s["sequence_index"], s["speaker_tag"], s["voice_profile_id"],
                    s["spoken_text"], s.get("raw_directions", ""), s.get("emotion", "neutral"),
                    s.get("pace", 1.0), s.get("pitch", 0.0), s.get("pause_after_sec", 0.45)
                ))
            conn.execute("UPDATE podcast_episodes SET total_segments = ?, rendered_segments = 0 WHERE id = ?", (len(segments), eid))
            conn.commit()

    def update_segment_rendered(self, seg_id: str, audio_path: str, duration_sec: float):
        with self.get_connection() as conn:
            conn.execute("""
            UPDATE script_segments 
            SET status = 'rendered', audio_path = ?, duration_sec = ?
            WHERE id = ?
            """, (audio_path, duration_sec, seg_id))
            conn.execute("""
            UPDATE podcast_episodes 
            SET rendered_segments = rendered_segments + 1 
            WHERE id = (SELECT episode_id FROM script_segments WHERE id = ?)
            """, (seg_id,))
            conn.commit()

    def get_all_episodes(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM podcast_episodes ORDER BY created_at DESC").fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["qa_report"] = json.loads(item["qa_report"]) if item.get("qa_report") else {}
                results.append(item)
            return results

    # --- Fine-Tuning Datasets & Jobs ---
    def create_dataset(self, name: str, speaker_name: str, description: str = "", consent_confirmed: bool = True) -> Dict[str, Any]:
        did = str(uuid.uuid4())
        now = time.time()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO finetuning_datasets (id, name, speaker_name, description, consent_confirmed, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (did, name, speaker_name, description, 1 if consent_confirmed else 0, now))
            conn.commit()
        return self.get_dataset(did)

    def get_all_datasets(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM finetuning_datasets ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    def get_dataset(self, did: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM finetuning_datasets WHERE id = ?", (did,)).fetchone()
            return dict(r) if r else None

    def create_finetuning_job(self, dataset_id: str, base_model: str = "qwen3-tts-0.6b", total_epochs: int = 10) -> Dict[str, Any]:
        jid = str(uuid.uuid4())
        now = time.time()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO finetuning_jobs (id, dataset_id, base_model, status, total_epochs, created_at)
            VALUES (?, ?, ?, 'queued', ?, ?)
            """, (jid, dataset_id, base_model, total_epochs, now))
            conn.commit()
        return self.get_finetuning_job(jid)

    def get_all_finetuning_jobs(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM finetuning_jobs ORDER BY created_at DESC").fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["loss_history"] = json.loads(item["loss_history"]) if item.get("loss_history") else []
                results.append(item)
            return results

    def get_finetuning_job(self, jid: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            r = conn.execute("SELECT * FROM finetuning_jobs WHERE id = ?", (jid,)).fetchone()
            if not r:
                return None
            res = dict(r)
            res["loss_history"] = json.loads(res["loss_history"]) if res.get("loss_history") else []
            return res

    def update_finetuning_progress(self, jid: str, epoch: int, loss: float, progress: float):
        with self.get_connection() as conn:
            r = conn.execute("SELECT loss_history FROM finetuning_jobs WHERE id = ?", (jid,)).fetchone()
            history = json.loads(r["loss_history"]) if r and r["loss_history"] else []
            history.append({"epoch": epoch, "loss": round(loss, 4), "timestamp": time.time()})
            conn.execute("""
            UPDATE finetuning_jobs 
            SET current_epoch = ?, current_loss = ?, progress_percent = ?, loss_history = ?, status = 'training'
            WHERE id = ?
            """, (epoch, loss, progress, json.dumps(history), jid))
            conn.commit()

    def complete_finetuning_job(self, jid: str, checkpoint_path: str):
        now = time.time()
        with self.get_connection() as conn:
            conn.execute("""
            UPDATE finetuning_jobs 
            SET status = 'completed', progress_percent = 100.0, output_checkpoint_path = ?, completed_at = ?
            WHERE id = ?
            """, (checkpoint_path, now, jid))
            conn.commit()

# Global database manager instance
db_manager = DatabaseManager()
