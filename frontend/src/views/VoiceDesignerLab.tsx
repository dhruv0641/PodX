import React, { useState } from 'react';
import {
  Wand2,
  Sparkles,
  Sliders,
  Play,
  CheckCircle2,
  Mic2,
  Save,
  Volume2
} from 'lucide-react';
import { VoiceProfile } from '../types';

export const VoiceDesignerLab: React.FC = () => {
  const [name, setName] = useState('');
  const [gender, setGender] = useState<'male' | 'female' | 'neutral'>('male');
  const [accent, setAccent] = useState('American');
  const [prompt, setPrompt] = useState('');
  const [speed, setSpeed] = useState(1.0);
  const [pitch, setPitch] = useState(0.0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [createdVoice, setCreatedVoice] = useState<VoiceProfile | null>(null);

  const handleDesignVoice = async () => {
    if (!name.trim() || !prompt.trim()) return;
    setIsGenerating(true);
    try {
      const res = await fetch('/api/voices/design', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          gender,
          accent,
          persona_prompt: prompt,
          speed,
          pitch
        })
      });
      if (res.ok) {
        const data = await res.json();
        setCreatedVoice(data);
      }
    } catch (e) {
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-full p-8 max-w-4xl mx-auto space-y-8 overflow-y-auto">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Wand2 className="w-6 h-6 text-purple-400" />
          <span>AI Voice Designer</span>
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Synthesize original, fictional voice personalities using natural language descriptions.
          Configure acoustic timbre, pitch balance, and cadence.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Configuration Panel */}
        <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-5">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-purple-400" />
            <span>Persona Specifications</span>
          </h3>

          <div className="space-y-4">
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">
                Voice Persona Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Cassandra, Sterling, Julian"
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value as any)}
                  className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="neutral">Neutral</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Accent</label>
                <select
                  value={accent}
                  onChange={(e) => setAccent(e.target.value)}
                  className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
                >
                  <option value="American">American</option>
                  <option value="British">British</option>
                  <option value="Indian">Indian English</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">
                Natural-Language Persona Prompt
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe tone, timbre, and character (e.g. A deep, intellectual philosopher with gravitas, speaking in a calm, analytical cadence with nuanced pauses...)"
                rows={4}
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl p-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 resize-none"
              />
            </div>

            {/* Sliders */}
            <div className="space-y-3 pt-2">
              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Pitch Offset</span>
                  <span className="font-mono text-purple-300">{pitch > 0 ? `+${pitch}` : pitch}</span>
                </div>
                <input
                  type="range"
                  min="-4"
                  max="4"
                  step="0.5"
                  value={pitch}
                  onChange={(e) => setPitch(parseFloat(e.target.value))}
                  className="w-full accent-purple-600 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Speaking Rate</span>
                  <span className="font-mono text-purple-300">{speed}x</span>
                </div>
                <input
                  type="range"
                  min="0.8"
                  max="1.3"
                  step="0.05"
                  value={speed}
                  onChange={(e) => setSpeed(parseFloat(e.target.value))}
                  className="w-full accent-purple-600 cursor-pointer"
                />
              </div>
            </div>

            <button
              onClick={handleDesignVoice}
              disabled={isGenerating || !name.trim() || !prompt.trim()}
              className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-medium text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-purple-600/30"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isGenerating ? 'Designing Persona...' : 'Synthesize Voice Persona'}</span>
            </button>
          </div>
        </div>

        {/* Live Preview Panel */}
        <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Mic2 className="w-4 h-4 text-purple-400" />
              <span>Persona Preview & Result</span>
            </h3>

            {createdVoice ? (
              <div className="p-5 rounded-xl bg-charcoal-950 border border-purple-500/30 space-y-3 glow-purple">
                <div className="flex items-center justify-between">
                  <h4 className="text-base font-bold text-white">{createdVoice.name}</h4>
                  <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium">
                    Created
                  </span>
                </div>

                <div className="text-xs text-slate-400">
                  {createdVoice.accent} • {createdVoice.gender}
                </div>

                <p className="text-xs text-slate-300 leading-relaxed italic">
                  "{createdVoice.description}"
                </p>

                <div className="pt-2">
                  <audio
                    controls
                    src={`/api/voices/${createdVoice.id}/preview`}
                    className="w-full h-10 accent-purple-600 rounded-lg"
                  />
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-slate-500 text-xs">
                Fill out the specifications on the left and click "Synthesize Voice Persona" to preview your custom acoustic profile.
              </div>
            )}
          </div>

          <div className="p-4 rounded-xl bg-charcoal-950 border border-charcoal-800/80 text-xs text-slate-400 space-y-1">
            <div className="font-semibold text-slate-300 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Voice Safety & Provenance</span>
            </div>
            <p>
              Custom personas are synthesized purely as fictional character voices. All outputs
              comply with AI ethics safeguards and privacy boundaries.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
