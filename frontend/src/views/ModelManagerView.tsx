import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Zap,
  HardDrive,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Layers,
  Sparkles
} from 'lucide-react';
import { HardwareStatus } from '../types';

export const ModelManagerView: React.FC = () => {
  const [models, setModels] = useState<any[]>([]);
  const [hw, setHw] = useState<HardwareStatus | null>(null);

  useEffect(() => {
    fetch('/api/system/models')
      .then((r) => r.json())
      .then((d) => setModels(d || []))
      .catch(() => {});

    fetch('/api/system/hardware')
      .then((r) => r.json())
      .then((d) => setHw(d))
      .catch(() => {});
  }, []);

  return (
    <div className="h-full p-8 max-w-5xl mx-auto space-y-8 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Cpu className="w-6 h-6 text-purple-400" />
          <span>Model Manager & Hardware Allocation</span>
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Inspect installed neural audio engines, memory footprints, and execution safety guards.
        </p>
      </div>

      {/* Hardware Telemetry Card */}
      {hw && (
        <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-1">
            <div className="text-xs text-slate-400 flex items-center gap-1.5">
              <Zap className="w-4 h-4 text-amber-400" />
              <span>NVIDIA GPU Acceleration</span>
            </div>
            <div className="text-lg font-bold text-white">{hw.gpu.name}</div>
            <div className="text-xs text-slate-400 font-mono">
              VRAM: {hw.gpu.vram_free_mb}MB free / {hw.gpu.vram_total_mb}MB total
            </div>
          </div>

          <div className="space-y-1">
            <div className="text-xs text-slate-400 flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-cyan-400" />
              <span>Host CPU & System Memory</span>
            </div>
            <div className="text-lg font-bold text-white">{hw.ram.total_gb} GB RAM</div>
            <div className="text-xs text-slate-400 font-mono">
              Available: {hw.ram.free_gb} GB • Cores: {hw.cpu.cores}
            </div>
          </div>

          <div className="space-y-1">
            <div className="text-xs text-slate-400 flex items-center gap-1.5">
              <HardDrive className="w-4 h-4 text-emerald-400" />
              <span>Model & Cache Storage</span>
            </div>
            <div className="text-lg font-bold text-white">{hw.storage.free_gb} GB Free</div>
            <div className="text-xs text-slate-400 font-mono">Disk Space Available</div>
          </div>
        </div>
      )}

      {/* Model Cards */}
      <div className="space-y-4">
        <h3 className="text-base font-semibold text-slate-100">Integrated Speech Models</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {models.map((m) => (
            <div
              key={m.id}
              className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">
                    {m.family}
                  </span>
                  <span className="text-xs text-emerald-400 font-medium flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Active</span>
                  </span>
                </div>

                <h4 className="text-base font-bold text-white">{m.name}</h4>
                <div className="text-xs text-slate-400 font-mono space-y-1">
                  <div>VRAM Footprint: ~{m.vram_requirement_mb} MB</div>
                  <div>Cache Size: {m.size_mb > 0 ? `${m.size_mb} MB` : 'Dynamic'}</div>
                </div>
              </div>

              <div className="pt-3 border-t border-charcoal-800/80">
                <div className="text-[11px] text-slate-400 font-medium">Recommended for:</div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {m.recommended_modes.map((mode: string, idx: number) => (
                    <span
                      key={idx}
                      className="text-[10px] px-2 py-0.5 rounded bg-charcoal-800 text-slate-300"
                    >
                      {mode}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
