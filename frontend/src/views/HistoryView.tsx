import React, { useState, useEffect } from 'react';
import {
  History,
  Play,
  Download,
  Search,
  Clock,
  Volume2,
  FileText,
  Sliders,
  CheckCircle2,
  Trash2
} from 'lucide-react';
import { PodcastEpisode } from '../types';
import { ViewTab } from '../components/Sidebar';

interface HistoryViewProps {
  onSelectTab: (tab: ViewTab) => void;
  onPlayEpisode: (ep: PodcastEpisode) => void;
}

export const HistoryView: React.FC<HistoryViewProps> = ({ onSelectTab, onPlayEpisode }) => {
  const [episodes, setEpisodes] = useState<PodcastEpisode[]>([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/podcasts')
      .then((r) => r.json())
      .then((d) => setEpisodes(d || []))
      .catch(() => {});
  }, []);

  const filtered = episodes.filter((ep) =>
    ep.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="h-full p-8 max-w-6xl mx-auto space-y-6 overflow-hidden flex flex-col">
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <History className="w-6 h-6 text-purple-400" />
            <span>Podcast Archive & History</span>
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Access past generated podcast masters, download multi-format exports, and review loudness telemetry.
          </p>
        </div>

        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search episodes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-charcoal-900 border border-charcoal-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500 w-64"
          />
        </div>
      </div>

      <div className="flex-1 rounded-2xl bg-charcoal-900 border border-charcoal-800 overflow-y-auto">
        {filtered.length === 0 ? (
          <div className="p-16 text-center text-slate-500 text-sm">
            No podcast episodes match your query.
          </div>
        ) : (
          <div className="divide-y divide-charcoal-800">
            {filtered.map((ep) => (
              <div
                key={ep.id}
                className="p-5 flex items-center justify-between hover:bg-charcoal-850/50 transition gap-4"
              >
                <div className="flex items-center gap-4 min-w-0">
                  <button
                    onClick={() => onPlayEpisode(ep)}
                    className="w-10 h-10 rounded-full bg-purple-600/20 text-purple-400 hover:bg-purple-600 hover:text-white flex items-center justify-center transition shrink-0"
                  >
                    <Play className="w-4 h-4 ml-0.5" />
                  </button>

                  <div className="min-w-0">
                    <h4 className="text-sm font-bold text-white truncate">{ep.title}</h4>
                    <div className="text-xs text-slate-400 flex items-center gap-2 mt-1 font-mono">
                      <span>{Math.round(ep.duration_seconds)}s</span>
                      <span>•</span>
                      <span>{ep.rendered_segments || ep.total_segments} turns</span>
                      <span>•</span>
                      <span className="text-purple-300">
                        {ep.integrated_lufs ? `${ep.integrated_lufs.toFixed(1)} LUFS` : '-16 LUFS'}
                      </span>
                      <span>•</span>
                      <span className="text-cyan-300">
                        {ep.true_peak_dbtp ? `${ep.true_peak_dbtp.toFixed(1)} dBTP` : '-1.0 dBTP'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <button
                    onClick={() => {
                      onPlayEpisode(ep);
                      onSelectTab('studio');
                    }}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-charcoal-800 hover:bg-charcoal-750 text-xs text-slate-300 font-medium transition"
                  >
                    <Sliders className="w-3.5 h-3.5" />
                    <span>Open Studio</span>
                  </button>

                  <a
                    href={`/api/podcasts/${ep.id}/download/mp3`}
                    download
                    className="p-2 rounded-lg bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 text-slate-400 transition"
                    title="Download MP3"
                  >
                    <Download className="w-4 h-4" />
                  </a>

                  <a
                    href={`/api/podcasts/${ep.id}/download/srt`}
                    download
                    className="p-2 rounded-lg bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 text-slate-400 transition"
                    title="Download SRT"
                  >
                    <FileText className="w-4 h-4" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
