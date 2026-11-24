import React, { useState, useEffect, useRef } from 'react';
import {
  Sliders,
  RefreshCw,
  Play,
  Pause,
  Volume2,
  Clock,
  Sparkles,
  Download,
  CheckCircle2,
  AlertCircle,
  FileText
} from 'lucide-react';
import { PodcastEpisode, ScriptSegment, VoiceProfile } from '../types';

interface StudioViewProps {
  activeEpisode: PodcastEpisode | null;
  onPlayEpisode: (ep: PodcastEpisode) => void;
}

export const StudioView: React.FC<StudioViewProps> = ({ activeEpisode, onPlayEpisode }) => {
  const [episode, setEpisode] = useState<PodcastEpisode | null>(activeEpisode);
  const [voices, setVoices] = useState<VoiceProfile[]>([]);
  const [selectedSegment, setSelectedSegment] = useState<ScriptSegment | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [playingSegmentId, setPlayingSegmentId] = useState<string | null>(null);
  const segmentAudioRef = useRef<HTMLAudioElement | null>(null);
  const masterAudioRef = useRef<HTMLAudioElement | null>(null);
  const [isMasterPlaying, setIsMasterPlaying] = useState(false);

  // Load voices
  useEffect(() => {
    fetch('/api/voices')
      .then((r) => r.json())
      .then((d) => setVoices(d || []))
      .catch(() => {});
  }, []);

  // Fetch / refresh episode data
  const loadEpisodeDetails = (epId: string) => {
    fetch(`/api/podcasts/${epId}`)
      .then((r) => r.json())
      .then((d) => {
        if (d.episode) {
          setEpisode(d.episode);
          // Also update parent if duration or status changed
          if (activeEpisode && activeEpisode.id === d.episode.id && activeEpisode.duration_seconds !== d.episode.duration_seconds) {
            onPlayEpisode(d.episode);
          }
        }
      })
      .catch(() => {});
  };

  useEffect(() => {
    if (activeEpisode?.id) {
      loadEpisodeDetails(activeEpisode.id);
    } else {
      // If no active episode loaded, automatically load the most recent episode
      fetch('/api/podcasts')
        .then((r) => r.json())
        .then((episodes) => {
          if (episodes && episodes.length > 0) {
            loadEpisodeDetails(episodes[0].id);
          }
        })
        .catch(() => {});
    }
  }, [activeEpisode?.id]);

  // Handle Play individual sentence
  const handlePlaySegment = (segId: string) => {
    if (!episode) return;

    if (playingSegmentId === segId) {
      segmentAudioRef.current?.pause();
      setPlayingSegmentId(null);
      return;
    }

    if (segmentAudioRef.current) {
      segmentAudioRef.current.pause();
    }
    if (masterAudioRef.current) {
      masterAudioRef.current.pause();
      setIsMasterPlaying(false);
    }

    const audioUrl = `/api/podcasts/${episode.id}/segments/${segId}/audio`;
    const audio = new Audio(audioUrl);
    segmentAudioRef.current = audio;
    setPlayingSegmentId(segId);

    audio.play().catch((e) => {
      console.error('Audio playback error:', e);
      setPlayingSegmentId(null);
    });

    audio.onended = () => setPlayingSegmentId(null);
    audio.onerror = () => setPlayingSegmentId(null);
  };

  // Toggle master playback
  const toggleMasterAudio = () => {
    if (!masterAudioRef.current || !episode) return;
    if (isMasterPlaying) {
      masterAudioRef.current.pause();
      setIsMasterPlaying(false);
    } else {
      if (segmentAudioRef.current) {
        segmentAudioRef.current.pause();
        setPlayingSegmentId(null);
      }
      masterAudioRef.current.play().then(() => setIsMasterPlaying(true)).catch(() => {});
    }
  };

  const handleRegenerateSegment = async (segId: string) => {
    if (!episode) return;
    setIsRegenerating(true);
    try {
      const res = await fetch(`/api/podcasts/${episode.id}/segments/${segId}/regenerate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (res.ok) {
        loadEpisodeDetails(episode.id);
      }
    } catch (e) {
    } finally {
      setIsRegenerating(false);
    }
  };

  if (!episode) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center text-slate-400">
        <Sliders className="w-12 h-12 text-slate-600 mb-3" />
        <h3 className="text-lg font-semibold text-slate-200">No Podcast Session Loaded</h3>
        <p className="text-sm text-slate-500 max-w-sm mt-1">
          Generate an episode in New Chat Studio or select one from Podcast History to inspect and edit tracks.
        </p>
      </div>
    );
  }

  const segments = episode.segments || [];
  const durationMins = Math.floor((episode.duration_seconds || 0) / 60);
  const durationSecs = Math.floor((episode.duration_seconds || 0) % 60);

  return (
    <div className="h-full flex flex-col bg-charcoal-950 overflow-hidden">
      {/* Studio Header Bar */}
      <div className="p-6 border-b border-charcoal-800 bg-charcoal-900/80 backdrop-blur flex flex-wrap items-center justify-between gap-4 shrink-0">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white tracking-tight">{episode.title}</h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20 font-medium">
              Multi-Track Timeline
            </span>
          </div>
          <div className="text-xs text-slate-400 flex items-center gap-3 mt-1.5 font-mono">
            <span className="text-slate-200 font-semibold">
              Duration: {durationMins}m {durationSecs}s ({Math.round(episode.duration_seconds || 0)}s)
            </span>
            <span>•</span>
            <span>{segments.length} dialogue turns</span>
            <span>•</span>
            <span className="text-purple-300">LUFS: {episode.integrated_lufs?.toFixed(1) || '-16.0'}</span>
            <span>•</span>
            <span className="text-cyan-300">Peak: {episode.true_peak_dbtp?.toFixed(1) || '-1.0'} dBTP</span>
          </div>
        </div>

        {/* Studio Audio Controls */}
        <div className="flex items-center gap-3">
          {/* Native HTML5 Audio Player for instantaneous streaming playback */}
          <audio
            ref={masterAudioRef}
            src={`/api/podcasts/${episode.id}/audio`}
            onPlay={() => setIsMasterPlaying(true)}
            onPause={() => setIsMasterPlaying(false)}
            onEnded={() => setIsMasterPlaying(false)}
            controls
            className="h-9 w-64 md:w-80 rounded-xl accent-purple-600 bg-charcoal-850"
          />

          <button
            onClick={toggleMasterAudio}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition shadow-md shadow-purple-600/30"
          >
            {isMasterPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
            <span>{isMasterPlaying ? 'Pause Master' : 'Play Full Master'}</span>
          </button>

          <a
            href={`/api/podcasts/${episode.id}/download/mp3`}
            download
            className="flex items-center gap-1 px-3 py-2 rounded-xl bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 text-xs text-slate-300 font-medium transition border border-charcoal-700"
            title="Download Broadcast MP3 (320kbps)"
          >
            <Download className="w-3.5 h-3.5" />
            <span>MP3</span>
          </a>
        </div>
      </div>

      {/* Main Track Workspace */}
      <div className="flex-1 overflow-y-auto p-6 space-y-3">
        <div className="text-xs text-slate-400 font-mono mb-2 flex items-center justify-between">
          <span>Click the play icon on any sentence to listen to that specific dialogue turn:</span>
          <span>{segments.length} Segments Total</span>
        </div>

        {segments.map((seg, idx) => {
          const isFemale = seg.speaker_tag.toUpperCase().includes('F') ||
                           seg.speaker_tag.toUpperCase().includes('SOPHIA') ||
                           seg.speaker_tag.toUpperCase().includes('ALICE');
          const isPlayingThis = playingSegmentId === seg.id;

          return (
            <div
              key={seg.id}
              onClick={() => setSelectedSegment(seg)}
              className={`p-4 rounded-xl border transition cursor-pointer flex items-start gap-4 ${
                isPlayingThis
                  ? 'bg-purple-900/30 border-purple-500 shadow-lg glow-purple'
                  : selectedSegment?.id === seg.id
                  ? 'bg-purple-900/15 border-purple-500/40'
                  : 'bg-charcoal-900 border-charcoal-800 hover:border-charcoal-700'
              }`}
            >
              {/* Play Button for this sentence */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handlePlaySegment(seg.id);
                }}
                className={`w-9 h-9 rounded-full flex items-center justify-center transition shrink-0 mt-0.5 ${
                  isPlayingThis
                    ? 'bg-purple-600 text-white animate-pulse shadow-md shadow-purple-600/50'
                    : 'bg-charcoal-800 hover:bg-purple-600 hover:text-white text-purple-400'
                }`}
                title="Play this sentence"
              >
                {isPlayingThis ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
              </button>

              {/* Dialogue Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                        isFemale
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      }`}
                    >
                      {seg.speaker_tag}
                    </span>
                    {seg.raw_directions && (
                      <span className="text-[11px] text-purple-400 font-mono">
                        [{seg.raw_directions}]
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-400 font-mono">
                    <span className="text-slate-400">{seg.duration_sec ? `${seg.duration_sec.toFixed(2)}s` : ''}</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRegenerateSegment(seg.id);
                      }}
                      disabled={isRegenerating}
                      className="p-1 text-slate-400 hover:text-purple-300 transition"
                      title="Regenerate this specific sentence"
                    >
                      <RefreshCw className={`w-3.5 h-3.5 ${isRegenerating ? 'animate-spin' : ''}`} />
                    </button>
                  </div>
                </div>

                <p className="text-sm text-slate-100 leading-relaxed">
                  {seg.spoken_text}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
