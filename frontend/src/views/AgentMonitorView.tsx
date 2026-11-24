import React from 'react';
import {
  Activity,
  CheckCircle2,
  Layers,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  RotateCw,
  Cpu,
  Volume2
} from 'lucide-react';

export const AgentMonitorView: React.FC = () => {
  const agents = [
    { id: 1, name: 'Master Orchestration Agent', role: 'Coordinates generation lifecycle & recovery loops', status: 'Online' },
    { id: 2, name: 'Script Intelligence Agent', role: 'Parses script, strips bracketed directions & pauses', status: 'Online' },
    { id: 3, name: 'Podcast Director Agent', role: 'Plans conversational pacing, transitions & scene flow', status: 'Online' },
    { id: 4, name: 'Voice Casting Agent', role: 'Assigns 24 distinct personas & validates acoustic harmony', status: 'Online' },
    { id: 5, name: 'Emotion & Prosody Agent', role: 'Maps script emotions to pitch, rate & timbre offsets', status: 'Online' },
    { id: 6, name: 'Pronunciation Agent', role: 'Enforces technical vocabulary and acronym phonetics', status: 'Online' },
    { id: 7, name: 'Speech Generation Agent', role: 'Synthesizes dialogue turns via Kokoro & Qwen models', status: 'Online' },
    { id: 8, name: 'Continuity Agent', role: 'Prevents acoustic drift and speaker identity swaps', status: 'Online' },
    { id: 9, name: 'Audio Engineering Agent', role: 'Applies -16 LUFS mastering, compression & ducking', status: 'Online' },
    { id: 10, name: 'Audio QA Agent', role: 'Verifies script completeness, clipping & loudness limits', status: 'Online' },
    { id: 11, name: 'Recovery Agent', role: 'Manages bounded retries and provider fallback', status: 'Online' },
    { id: 12, name: 'Memory Agent', role: 'Commits checkpoints, audio assets & metrics to SQLite WAL', status: 'Online' }
  ];

  return (
    <div className="h-full p-8 max-w-5xl mx-auto space-y-8 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Activity className="w-6 h-6 text-purple-400" />
          <span>Agent Orchestration Monitor</span>
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Stateful multi-agent DAG executing asynchronous podcast generation with durable SQLite checkpoints.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((ag) => (
          <div
            key={ag.id}
            className="p-5 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-3 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-purple-400">Agent {String(ag.id).padStart(2, '0')}</span>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                  {ag.status}
                </span>
              </div>
              <h4 className="text-sm font-bold text-white">{ag.name}</h4>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">{ag.role}</p>
            </div>

            <div className="pt-3 border-t border-charcoal-800 text-[11px] text-slate-500 font-mono flex items-center justify-between">
              <span>Failure Recovery: Bounded</span>
              <span>State: Resumable</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
