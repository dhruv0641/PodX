"""
PodX Database Models
Complete schema for podcasts, voices, chat, episodes, segments, and fine-tuning.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from database.session import Base

def generate_id():
    return str(uuid.uuid4())

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_id)
    title = Column(String(255), default="New Podcast Session")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pinned = Column(Boolean, default=False)
    meta_info = Column(JSON, default=dict)

    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")
    projects = relationship("PodcastProject", back_populates="conversation")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=generate_id)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(32), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    intent = Column(String(64), nullable=True)  # script_submission, command, feedback
    parsed_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id = Column(String(36), primary_key=True)  # M01, F01, etc. or UUID
    name = Column(String(64), nullable=False)
    gender = Column(String(16), nullable=False)  # male, female, neutral
    accent = Column(String(64), default="American")
    language = Column(String(32), default="en-US")
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # ["intellectual", "deep", "authoritative"]
    pitch_offset: float = Column(Float, default=0.0)
    speed_factor: float = Column(Float, default=1.0)
    preferred_provider = Column(String(64), default="kokoro")
    provider_voice_id = Column(String(64), default="am_adam")
    preview_audio_path = Column(String(512), nullable=True)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PodcastProject(Base):
    __tablename__ = "podcast_projects"

    id = Column(String(36), primary_key=True, default=generate_id)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=True)
    raw_script = Column(Text, nullable=False)
    mode = Column(String(32), default="two-host")  # solo, two-host, roundtable
    quality_mode = Column(String(32), default="Studio")  # Preview, Balanced, Studio, Extreme
    strict_script_mode = Column(Boolean, default=True)
    estimated_duration_sec = Column(Float, default=0.0)
    speaker_mapping = Column(JSON, default=dict)  # {"M01": "Alexander", "F01": "Sophia"}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="projects")
    episodes = relationship("PodcastEpisode", back_populates="project", cascade="all, delete-orphan")

class PodcastEpisode(Base):
    __tablename__ = "podcast_episodes"

    id = Column(String(36), primary_key=True, default=generate_id)
    project_id = Column(String(36), ForeignKey("podcast_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(32), default="pending")  # pending, generating, mastering, completed, failed
    progress_percent = Column(Float, default=0.0)
    current_stage = Column(String(64), default="Queued")
    duration_seconds = Column(Float, default=0.0)
    total_segments = Column(Integer, default=0)
    rendered_segments = Column(Integer, default=0)
    
    # Audio output files
    master_wav_path = Column(String(512), nullable=True)
    master_mp3_path = Column(String(512), nullable=True)
    srt_path = Column(String(512), nullable=True)
    vtt_path = Column(String(512), nullable=True)
    transcript_json_path = Column(String(512), nullable=True)
    
    # Metrics
    integrated_lufs = Column(Float, nullable=True)
    true_peak_dbtp = Column(Float, nullable=True)
    qa_status = Column(String(32), default="pending")  # passed, warning, failed
    qa_report = Column(JSON, default=dict)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    project = relationship("PodcastProject", back_populates="episodes")
    segments = relationship("ScriptSegment", back_populates="episode", cascade="all, delete-orphan", order_by="ScriptSegment.sequence_index")

class ScriptSegment(Base):
    __tablename__ = "script_segments"

    id = Column(String(36), primary_key=True, default=generate_id)
    episode_id = Column(String(36), ForeignKey("podcast_episodes.id"), nullable=False)
    sequence_index = Column(Integer, nullable=False)
    speaker_tag = Column(String(64), nullable=False)  # M01, Sophia, etc.
    voice_profile_id = Column(String(36), nullable=False)
    spoken_text = Column(Text, nullable=False)
    raw_directions = Column(String(255), nullable=True)  # [calm, thoughtful]
    emotion = Column(String(64), default="neutral")
    pace = Column(Float, default=1.0)
    pitch = Column(Float, default=0.0)
    pause_after_sec = Column(Float, default=0.4)
    
    # Render status
    status = Column(String(32), default="pending")  # pending, rendered, failed
    audio_path = Column(String(512), nullable=True)
    duration_sec = Column(Float, default=0.0)
    retry_count = Column(Integer, default=0)
    qa_wer = Column(Float, nullable=True)
    
    episode = relationship("PodcastEpisode", back_populates="segments")

class FineTuningDataset(Base):
    __tablename__ = "finetuning_datasets"

    id = Column(String(36), primary_key=True, default=generate_id)
    name = Column(String(128), nullable=False)
    speaker_name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    consent_confirmed = Column(Boolean, default=False)
    provenance_source = Column(String(255), nullable=True)
    total_audio_duration_sec = Column(Float, default=0.0)
    total_samples_count = Column(Integer, default=0)
    dataset_manifest_path = Column(String(512), nullable=True)
    status = Column(String(32), default="ready")
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("FineTuningJob", back_populates="dataset")

class FineTuningJob(Base):
    __tablename__ = "finetuning_jobs"

    id = Column(String(36), primary_key=True, default=generate_id)
    dataset_id = Column(String(36), ForeignKey("finetuning_datasets.id"), nullable=False)
    base_model = Column(String(64), default="qwen3-tts-0.6b")
    status = Column(String(32), default="queued")  # queued, training, completed, failed
    progress_percent = Column(Float, default=0.0)
    current_epoch = Column(Integer, default=0)
    total_epochs = Column(Integer, default=10)
    current_loss = Column(Float, nullable=True)
    loss_history = Column(JSON, default=list)
    output_checkpoint_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    dataset = relationship("FineTuningDataset", back_populates="jobs")
