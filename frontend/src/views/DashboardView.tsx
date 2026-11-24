import React, { useEffect, useState } from 'react';
import {
  Mic2,
  Clock,
  Sparkles,
  Play,
  ArrowRight,
  TrendingUp,
  Cpu,
  ShieldCheck,
  Headphones
} from 'lucide-react';
import { PodcastEpisode } from '../types';
import { ViewTab } from '../components/Sidebar';

interface DashboardViewProps {
  onSelectTab: (tab: ViewTab) => void;
  onPlayEpisode: (ep: PodcastEpisode) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onSelectTab, onPlayEpisode }) => {
  const [episodes, setEpisodes] = useState<PodcastEpisode[]>([]);

  useEffect(() => {
    fetch('/api/podcasts')
      .then((res) => res.json())
      .then((data) => setEpisodes(data || []))
      .catch(() => {});
  }, []);

  const totalDuration = episodes.reduce((acc, ep) => acc + (ep.duration_seconds || 0), 0);
  const completedEpisodes = episodes.filter((ep) => ep.status === 'completed');

  return (
    <div className="p-8 space-y-8 overflow-y-auto h-full">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-purple-900/40 via-indigo-900/20 to-charcoal-900 border border-purple-500/20 p-8 glow-purple">
        <div className="max-w-2xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-xs font-semibold text-purple-300">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Autonomous Local Audio Production</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Elite Knowledge Studio
          </h2>
          <p className="text-slate-300 text-sm leading-relaxed">
            Transform user-provided scripts into broadcast-grade 20–30 minute podcasts. Powered by
            modular multi-speaker synthesis, intelligent direction stripping, and EBU R128 mastering.
          </p>
          <div className="flex items-center gap-3 pt-2">
            <button
              onClick={() => onSelectTab('chat')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-sm transition shadow-lg shadow-purple-600/30"
            >
              <span>Create New Podcast</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onSelectTab('voices')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-charcoal-800 hover:bg-charcoal-750 text-slate-200 font-medium text-sm transition border border-charcoal-700"
            >
              <Mic2 className="w-4 h-4 text-purple-400" />
              <span>Explore 24 Voices</span>
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="p-5 rounded-xl bg-charcoal-900 border border-charcoal-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Total Episodes</span>
            <Headphones className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-white">{episodes.length}</div>
          <div className="text-xs text-emerald-400 font-medium flex items-center gap-1">
            <span>{completedEpisodes.length} broadcast ready</span>
          </div>
        </div>

        <div className="p-5 rounded-xl bg-charcoal-900 border border-charcoal-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Generated Audio</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {Math.floor(totalDuration / 60)}m {Math.floor(totalDuration % 60)}s
          </div>
          <div className="text-xs text-slate-400">Total mastered speech</div>
        </div>

        <div className="p-5 rounded-xl bg-charcoal-900 border border-charcoal-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Voice Library</span>
            <Mic2 className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">24 Profiles</div>
          <div className="text-xs text-slate-400">12 Male • 12 Female</div>
        </div>

        <div className="p-5 rounded-xl bg-charcoal-900 border border-charcoal-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Mastering Standard</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white">-16.0 LUFS</div>
          <div className="text-xs text-slate-400">-1.0 dBTP True-Peak Ceiling</div>
        </div>
      </div>

      {/* Recent Episodes Table */}
      <div className="rounded-xl bg-charcoal-900 border border-charcoal-800 overflow-hidden">
        <div className="p-5 border-b border-charcoal-800 flex items-center justify-between">
          <h3 className="font-semibold text-slate-100 text-sm">Recent Podcast Episodes</h3>
          <button
            onClick={() => onSelectTab('history')}
            className="text-xs text-purple-400 hover:text-purple-300 font-medium"
          >
            View All Episodes →
          </button>
        </div>

        {episodes.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No podcasts generated yet. Submit your script in the New Chat Studio to create your first episode!
          </div>
        ) : (
          <div className="divide-y divide-charcoal-800">
            {episodes.slice(0, 5).map((ep) => (
              <div
                key={ep.id}
                className="p-4 flex items-center justify-between hover:bg-charcoal-850/50 transition"
              >
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => onPlayEpisode(ep)}
                    className="w-9 h-9 rounded-full bg-purple-600/20 text-purple-400 hover:bg-purple-600 hover:text-white flex items-center justify-center transition shrink-0"
                  >
                    <Play className="w-4 h-4 ml-0.5" />
                  </button>
                  <div>
                    <div className="font-medium text-sm text-slate-200">{ep.title}</div>
                    <div className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                      <span>{Math.round(ep.duration_seconds)}s</span>
                      <span>•</span>
                      <span>{ep.rendered_segments || ep.total_segments} turns</span>
                      <span>•</span>
                      <span className="font-mono text-purple-300">
                        {ep.integrated_lufs ? `${ep.integrated_lufs.toFixed(1)} LUFS` : '-16 LUFS'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                      ep.status === 'completed'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : ep.status === 'generating'
                        ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20 animate-pulse'
                        : 'bg-charcoal-800 text-slate-400'
                    }`}
                  >
                    {ep.status === 'completed' ? 'Broadcast Ready' : ep.current_stage || ep.status}
                  </span>
                  <button
                    onClick={() => {
                      onPlayEpisode(ep);
                      onSelectTab('studio');
                    }}
                    className="text-xs text-slate-400 hover:text-slate-200 px-2 py-1 rounded bg-charcoal-800"
                  >
                    Open Studio
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
