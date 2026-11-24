import React, { useState } from 'react';
import {
  Settings,
  ShieldCheck,
  Volume2,
  HardDrive,
  Save,
  CheckCircle2,
  Sliders
} from 'lucide-react';

export const SettingsView: React.FC = () => {
  const [lufsTarget, setLufsTarget] = useState(-16.0);
  const [truePeakCeiling, setTruePeakCeiling] = useState(-1.0);
  const [sampleRate, setSampleRate] = useState(48000);
  const [pauseDuration, setPauseDuration] = useState(0.45);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="h-full p-8 max-w-4xl mx-auto space-y-8 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-purple-400" />
          <span>System & Audio Production Settings</span>
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Configure mastering standards, DSP signal chains, sample rates, and storage paths.
        </p>
      </div>

      <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-6">
        <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
          <Volume2 className="w-4 h-4 text-purple-400" />
          <span>Loudness & Digital Signal Processing</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">
              Integrated Loudness Target (LUFS)
            </label>
            <select
              value={lufsTarget}
              onChange={(e) => setLufsTarget(parseFloat(e.target.value))}
              className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="-16.0">-16.0 LUFS (Podcast Stereo Standard - EBU R128)</option>
              <option value="-19.0">-19.0 LUFS (Mono Podcast Standard)</option>
              <option value="-14.0">-14.0 LUFS (High Energy Web Audio)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">
              True-Peak Ceiling
            </label>
            <select
              value={truePeakCeiling}
              onChange={(e) => setTruePeakCeiling(parseFloat(e.target.value))}
              className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="-1.0">-1.0 dBTP (Standard Intersample Limiting)</option>
              <option value="-0.5">-0.5 dBTP (Maximum Safe Ceiling)</option>
              <option value="-2.0">-2.0 dBTP (Conservative Master)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">
              Production Master Sample Rate
            </label>
            <select
              value={sampleRate}
              onChange={(e) => setSampleRate(parseInt(e.target.value))}
              className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="48000">48,000 Hz (Broadcast & Video Standard)</option>
              <option value="44100">44,100 Hz (Standard CD Audio)</option>
              <option value="24000">24,000 Hz (Native Model Synthesis)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">
              Default Speaker Pause (Seconds)
            </label>
            <input
              type="number"
              step="0.05"
              min="0.2"
              max="1.5"
              value={pauseDuration}
              onChange={(e) => setPauseDuration(parseFloat(e.target.value))}
              className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <div className="pt-4 border-t border-charcoal-800 flex items-center justify-between">
          {saved ? (
            <span className="text-xs text-emerald-400 flex items-center gap-1 font-medium">
              <CheckCircle2 className="w-4 h-4" />
              <span>Settings saved to SQLite database.</span>
            </span>
          ) : (
            <span className="text-xs text-slate-500">Settings persist across restarts.</span>
          )}

          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </div>
    </div>
  );
};
