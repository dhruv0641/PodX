import React from 'react';
import {
  LayoutDashboard,
  MessageSquarePlus,
  Sliders,
  Mic2,
  Wand2,
  Cpu,
  Layers,
  History,
  Activity,
  Settings,
  Sparkles
} from 'lucide-react';

export type ViewTab =
  | 'dashboard'
  | 'chat'
  | 'studio'
  | 'voices'
  | 'designer'
  | 'finetune'
  | 'models'
  | 'history'
  | 'agents'
  | 'settings';

interface SidebarProps {
  currentTab: ViewTab;
  onSelectTab: (tab: ViewTab) => void;
  activeEpisodeTitle?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onSelectTab, activeEpisodeTitle }) => {
  const navItems: { id: ViewTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
    { id: 'chat', label: 'New Chat Studio', icon: <MessageSquarePlus className="w-5 h-5" />, badge: 'AI' },
    { id: 'studio', label: 'Podcast Studio', icon: <Sliders className="w-5 h-5" /> },
    { id: 'voices', label: 'Voice Library', icon: <Mic2 className="w-5 h-5" />, badge: '24' },
    { id: 'designer', label: 'AI Voice Designer', icon: <Wand2 className="w-5 h-5" /> },
    { id: 'finetune', label: 'Fine-Tuning Lab', icon: <Layers className="w-5 h-5" /> },
    { id: 'models', label: 'Model Manager', icon: <Cpu className="w-5 h-5" /> },
    { id: 'history', label: 'Podcast History', icon: <History className="w-5 h-5" /> },
    { id: 'agents', label: 'Agent Monitor', icon: <Activity className="w-5 h-5" /> },
    { id: 'settings', label: 'System Settings', icon: <Settings className="w-5 h-5" /> },
  ];

  return (
    <aside className="w-64 bg-charcoal-900 border-r border-charcoal-800 flex flex-col h-screen select-none shrink-0">
      {/* Brand Header */}
      <div className="p-5 border-b border-charcoal-800 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
          <Sparkles className="w-5 h-5 text-white animate-pulse" />
        </div>
        <div>
          <div className="font-bold text-base tracking-wide text-white flex items-center gap-1.5">
            PodX
            <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">
              Studio
            </span>
          </div>
          <div className="text-xs text-slate-400">Elite Knowledge AI</div>
        </div>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                isActive
                  ? 'bg-purple-600/15 text-purple-300 border border-purple-500/30 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-charcoal-800/60'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={isActive ? 'text-purple-400' : 'text-slate-400'}>
                  {item.icon}
                </span>
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[11px] font-semibold px-1.5 py-0.5 rounded-md bg-charcoal-800 text-purple-300 border border-purple-500/20">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Active Studio Quick Widget */}
      {activeEpisodeTitle && (
        <div className="p-3 mx-3 mb-3 bg-charcoal-850 border border-purple-500/30 rounded-xl">
          <div className="text-[11px] uppercase tracking-wider text-purple-400 font-semibold mb-1 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block" />
            Active Session
          </div>
          <div className="text-xs font-medium text-slate-200 truncate">{activeEpisodeTitle}</div>
        </div>
      )}

      {/* Hardware Safety Status Tag */}
      <div className="p-3.5 border-t border-charcoal-800 bg-charcoal-950/40 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-400" />
          <span>Local Offline Mode</span>
        </div>
        <span className="text-[11px] font-mono text-slate-500">v1.0.0</span>
      </div>
    </aside>
  );
};
