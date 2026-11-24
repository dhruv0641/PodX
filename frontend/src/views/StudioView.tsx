import React, { useState, useEffect } from 'react';
import {
  Sliders,
  RefreshCw,
  Play,
  Volume2,
  Clock,
  Sparkles,
  Download,
  CheckCircle2,
  AlertCircle
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

  useEffect(() => {
    fetch('/api/voices')
      .then((r) => r.json())
      .then((d) => setVoices(d || []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (activeEpisode?.id) {
      fetch(`/api/podcasts/${activeEpisode.id}`)
        .then((r) => r.json())
        .then((d) => {
          if (d.episode) setEpisode(d.episode);
        });
    }
  }, [activeEpisode]);

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
        // Refresh episode
        const epRes = await fetch(`/api/podcasts/${episode.id}`);
        const epData = await epRes.json();
        if (epData.episode) setEpisode(epData.episode);
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

  return (
    <div className="h-full flex flex-col bg-charcoal-950 overflow-hidden">
      {/* Studio Header Bar */}
      <div className="p-6 border-b border-charcoal-800 bg-charcoal-900/60 flex items-center justify-between shrink-0">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white tracking-tight">{episode.title}</h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20 font-medium">
              Multi-Track Timeline
            </span>
          </div>
          <div className="text-xs text-slate-400 flex items-center gap-3 mt-1 font-mono">
            <span>Duration: {Math.round(episode.duration_seconds)}s</span>
            <span>•</span>
            <span>Segments: {segments.length}</span>
            <span>•</span>
            <span className="text-purple-300">LUFS: {episode.integrated_lufs?.toFixed(1) || '-16.0'}</span>
            <span>•</span>
            <span className="text-cyan-300">Peak: {episode.true_peak_dbtp?.toFixed(1) || '-1.0'} dBTP</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => onPlayEpisode(episode)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition shadow-md shadow-purple-600/30"
          >
            <Play className="w-4 h-4 ml-0.5" />
            <span>Play Full Master</span>
          </button>
        </div>
      </div>

      {/* Main Track Workspace */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {segments.map((seg, idx) => {
          const isFemale = seg.speaker_tag.toUpperCase().includes('F') || seg.speaker_tag.toUpperCase().includes('SOPHIA');
          return (
            <div
              key={seg.id}
              onClick={() => setSelectedSegment(seg)}
              className={`p-4 rounded-xl border transition cursor-pointer ${
                selectedSegment?.id === seg.id
                  ? 'bg-purple-900/15 border-purple-500/50 shadow-sm'
                  : 'bg-charcoal-900 border-charcoal-800 hover:border-charcoal-700'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                      isFemale
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    }`}
                  >
                    {seg.speaker_tag.slice(0, 3)}
                  </div>
                  <div>
                    <span className="text-xs font-semibold text-slate-200">
                      {seg.speaker_tag}
                    </span>
                    {seg.raw_directions && (
                      <span className="text-[11px] text-purple-400 ml-2 font-mono">
                        [{seg.raw_directions}]
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-3 text-xs text-slate-400 font-mono">
                  <span>{seg.duration_sec ? `${seg.duration_sec}s` : ''}</span>
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

              {/* Dialogue text */}
              <p className="text-sm text-slate-100 mt-2 leading-relaxed">
                {seg.spoken_text}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
