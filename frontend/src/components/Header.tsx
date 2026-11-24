import React, { useEffect, useState } from 'react';
import { Cpu, HardDrive, Zap, Volume2, ShieldCheck } from 'lucide-react';
import { HardwareStatus } from '../types';

export const Header: React.FC = () => {
  const [hw, setHw] = useState<HardwareStatus | null>(null);

  useEffect(() => {
    const fetchHw = async () => {
      try {
        const res = await fetch('/api/system/hardware');
        if (res.ok) {
          const data = await res.json();
          setHw(data);
        }
      } catch (e) {
        // Fallback gracefully
      }
    };
    fetchHw();
    const interval = setInterval(fetchHw, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 border-b border-charcoal-800 bg-charcoal-900/80 backdrop-blur px-6 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-4">
        <h1 className="text-base font-semibold text-slate-200">
          Elite Knowledge — AI Podcast Studio
        </h1>
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-charcoal-800 border border-charcoal-700 text-xs text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Strict Script Mode: Active</span>
        </div>
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-xs text-purple-300">
          <Volume2 className="w-3.5 h-3.5 text-purple-400" />
          <span>-16.0 LUFS EBU R128</span>
        </div>
      </div>

      {/* Hardware Telemetry HUD */}
      <div className="flex items-center gap-4 text-xs font-mono">
        {hw && (
          <>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-charcoal-800/80 border border-charcoal-700/80 text-slate-300">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              <span>GPU: {hw.gpu.available ? `${hw.gpu.name.slice(0, 16)}` : 'CPU Safe'}</span>
            </div>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-charcoal-800/80 border border-charcoal-700/80 text-slate-300">
              <Cpu className="w-3.5 h-3.5 text-cyan-400" />
              <span>RAM: {hw.ram.percent}% ({hw.ram.free_gb}GB Free)</span>
            </div>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-charcoal-800/80 border border-charcoal-700/80 text-slate-300">
              <HardDrive className="w-3.5 h-3.5 text-emerald-400" />
              <span>Disk: {hw.storage.free_gb}GB Free</span>
            </div>
          </>
        )}
      </div>
    </header>
  );
};
