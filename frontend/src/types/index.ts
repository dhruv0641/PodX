export interface VoiceProfile {
  id: string;
  name: string;
  gender: 'male' | 'female' | 'neutral';
  accent: string;
  language: string;
  description: string;
  tags: string[];
  pitch_offset: number;
  speed_factor: number;
  preferred_provider: string;
  provider_voice_id: string;
  edge_voice_id?: string;
  preview_audio_path?: string;
  is_custom: boolean;
}

export interface ScriptSegment {
  id: string;
  episode_id: string;
  sequence_index: number;
  speaker_tag: string;
  voice_profile_id: string;
  spoken_text: string;
  raw_directions?: string;
  emotion: string;
  pace: number;
  pitch: number;
  pause_after_sec: number;
  status: 'pending' | 'rendered' | 'failed';
  audio_path?: string;
  duration_sec: number;
}

export interface PodcastEpisode {
  id: string;
  project_id: string;
  title: string;
  status: 'pending' | 'generating' | 'completed' | 'failed';
  progress_percent: number;
  current_stage: string;
  duration_seconds: number;
  total_segments: number;
  rendered_segments: number;
  master_wav_path?: string;
  master_mp3_path?: string;
  srt_path?: string;
  vtt_path?: string;
  transcript_json_path?: string;
  integrated_lufs?: number;
  true_peak_dbtp?: number;
  qa_status?: string;
  qa_report?: any;
  created_at: number;
  completed_at?: number;
  segments?: ScriptSegment[];
}

export interface ChatMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  intent?: string;
  parsed_metadata?: any;
  created_at: number;
}

export interface HardwareStatus {
  cpu: { percent: number; cores: number };
  ram: { total_gb: number; free_gb: number; percent: number };
  gpu: {
    available: boolean;
    name: string;
    vram_total_mb: number;
    vram_free_mb: number;
    backend: string;
  };
  storage: { free_gb: number; total_gb: number };
}

export interface FineTuningDataset {
  id: string;
  name: string;
  speaker_name: string;
  description: string;
  consent_confirmed: boolean;
  total_audio_duration_sec: number;
  total_samples_count: number;
  created_at: number;
}

export interface FineTuningJob {
  id: string;
  dataset_id: string;
  base_model: string;
  status: 'queued' | 'training' | 'completed' | 'failed';
  progress_percent: number;
  current_epoch: number;
  total_epochs: number;
  current_loss?: number;
  loss_history: { epoch: number; loss: number; timestamp: number }[];
  output_checkpoint_path?: string;
  created_at: number;
}
