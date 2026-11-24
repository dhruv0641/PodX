import React, { useState, useEffect } from 'react';
import {
  Mic2,
  Play,
  Pause,
  Filter,
  Search,
  Volume2,
  Sparkles,
  Tag,
  Globe
} from 'lucide-react';
import { VoiceProfile } from '../types';

export const VoiceLibraryView: React.FC = () => {
  const [voices, setVoices] = useState<VoiceProfile[]>([]);
  const [filterGender, setFilterGender] = useState<string>('all');
  const [filterAccent, setFilterAccent] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [playingVoiceId, setPlayingVoiceId] = useState<string | null>(null);
  const audioRef = React.useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    fetch('/api/voices')
      .then((r) => r.json())
      .then((d) => setVoices(d || []))
      .catch(() => {});
  }, []);

  const handlePlayPreview = (voiceId: string) => {
    if (playingVoiceId === voiceId) {
      audioRef.current?.pause();
      setPlayingVoiceId(null);
      return;
    }

    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audio = new Audio(`/api/voices/${voiceId}/preview`);
    audioRef.current = audio;
    setPlayingVoiceId(voiceId);

    audio.play();
    audio.onended = () => setPlayingVoiceId(null);
    audio.onerror = () => setPlayingVoiceId(null);
  };

  const filteredVoices = voices.filter((v) => {
    if (filterGender !== 'all' && v.gender !== filterGender) return false;
    if (filterAccent !== 'all' && !v.accent.toLowerCase().includes(filterAccent.toLowerCase()))
      return false;
    if (
      searchQuery &&
      !v.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !v.description.toLowerCase().includes(searchQuery.toLowerCase())
    )
      return false;
    return true;
  });

  return (
    <div className="h-full flex flex-col p-8 space-y-6 overflow-hidden">
      {/* Header & Stats */}
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <span>Voice Library</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">
              24 Distinct Profiles
            </span>
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Original fictional personas calibrated for deep intellectual discussions, narrative
            clarity, and emotional expressiveness.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-charcoal-900 border border-charcoal-800 shrink-0">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by name, timbre, style..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-charcoal-950 border border-charcoal-800 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500 w-64"
            />
          </div>

          {/* Gender Filter */}
          <div className="flex items-center gap-1 bg-charcoal-950 p-1 rounded-lg border border-charcoal-800 text-xs">
            {['all', 'male', 'female'].map((g) => (
              <button
                key={g}
                onClick={() => setFilterGender(g)}
                className={`px-3 py-1 rounded-md font-medium capitalize transition ${
                  filterGender === g
                    ? 'bg-purple-600 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {g}
              </button>
            ))}
          </div>

          {/* Accent Filter */}
          <div className="flex items-center gap-1 bg-charcoal-950 p-1 rounded-lg border border-charcoal-800 text-xs">
            {['all', 'american', 'british', 'indian'].map((acc) => (
              <button
                key={acc}
                onClick={() => setFilterAccent(acc)}
                className={`px-3 py-1 rounded-md font-medium capitalize transition ${
                  filterAccent === acc
                    ? 'bg-purple-600 text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {acc}
              </button>
            ))}
          </div>
        </div>

        <div className="text-xs text-slate-400 font-mono">
          Showing {filteredVoices.length} of {voices.length} voices
        </div>
      </div>

      {/* Grid of Voices */}
      <div className="flex-1 overflow-y-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 pr-1">
        {filteredVoices.map((v) => {
          const isPlaying = playingVoiceId === v.id;
          const isFemale = v.gender === 'female';

          return (
            <div
              key={v.id}
              className={`p-5 rounded-2xl border transition flex flex-col justify-between ${
                isPlaying
                  ? 'bg-purple-900/20 border-purple-500/60 shadow-lg glow-purple'
                  : 'bg-charcoal-900 border-charcoal-800 hover:border-charcoal-700'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div
                      className={`w-9 h-9 rounded-xl flex items-center justify-center text-xs font-bold ${
                        isFemale
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      }`}
                    >
                      {v.id}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-white flex items-center gap-1.5">
                        <span>{v.name}</span>
                        {v.is_custom && (
                          <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                            Custom
                          </span>
                        )}
                      </h4>
                      <div className="text-[11px] text-slate-400 flex items-center gap-1">
                        <Globe className="w-3 h-3 text-slate-500" />
                        <span>{v.accent}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePlayPreview(v.id)}
                    className={`w-9 h-9 rounded-full flex items-center justify-center transition shadow-md ${
                      isPlaying
                        ? 'bg-purple-600 text-white animate-pulse'
                        : 'bg-charcoal-800 hover:bg-purple-600 hover:text-white text-purple-400'
                    }`}
                    title="Play 15-second acoustic preview"
                  >
                    {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
                  </button>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed line-clamp-3">
                  {v.description}
                </p>
              </div>

              {/* Tags and Pace/Pitch HUD */}
              <div className="pt-4 border-t border-charcoal-800/80 space-y-2">
                <div className="flex flex-wrap gap-1">
                  {(v.tags || []).slice(0, 3).map((tag, idx) => (
                    <span
                      key={idx}
                      className="text-[10px] px-2 py-0.5 rounded-md bg-charcoal-800 text-slate-400 font-medium capitalize"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1">
                  <span>Speed: {v.speed_factor}x</span>
                  <span>Pitch: {v.pitch_offset >= 0 ? `+${v.pitch_offset}` : v.pitch_offset}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
