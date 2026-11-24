import React, { useState } from 'react';
import { Sidebar, ViewTab } from './components/Sidebar';
import { Header } from './components/Header';
import { AudioPlayer } from './components/AudioPlayer';

import { DashboardView } from './views/DashboardView';
import { NewChatView } from './views/NewChatView';
import { StudioView } from './views/StudioView';
import { VoiceLibraryView } from './views/VoiceLibraryView';
import { VoiceDesignerLab } from './views/VoiceDesignerLab';
import { FineTuningLabView } from './views/FineTuningLabView';
import { ModelManagerView } from './views/ModelManagerView';
import { HistoryView } from './views/HistoryView';
import { AgentMonitorView } from './views/AgentMonitorView';
import { SettingsView } from './views/SettingsView';

import { PodcastEpisode } from './types';

export default function App() {
  const [currentTab, setCurrentTab] = useState<ViewTab>('dashboard');
  const [activeEpisode, setActiveEpisode] = useState<PodcastEpisode | null>(null);

  const handlePlayEpisode = (ep: PodcastEpisode) => {
    setActiveEpisode(ep);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-charcoal-950 text-slate-100 antialiased select-none">
      {/* Fixed Left Navigation Sidebar */}
      <Sidebar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        activeEpisodeTitle={activeEpisode?.title}
      />

      {/* Main Workspace Frame */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
        {/* Top Telemetry & Controls Header */}
        <Header />

        {/* Dynamic Viewport Container */}
        <main className="flex-1 min-h-0 overflow-hidden relative">
          {currentTab === 'dashboard' && (
            <DashboardView onSelectTab={setCurrentTab} onPlayEpisode={handlePlayEpisode} />
          )}
          {currentTab === 'chat' && (
            <NewChatView onSelectTab={setCurrentTab} onPlayEpisode={handlePlayEpisode} />
          )}
          {currentTab === 'studio' && (
            <StudioView activeEpisode={activeEpisode} onPlayEpisode={handlePlayEpisode} />
          )}
          {currentTab === 'voices' && <VoiceLibraryView />}
          {currentTab === 'designer' && <VoiceDesignerLab />}
          {currentTab === 'finetune' && <FineTuningLabView />}
          {currentTab === 'models' && <ModelManagerView />}
          {currentTab === 'history' && (
            <HistoryView onSelectTab={setCurrentTab} onPlayEpisode={handlePlayEpisode} />
          )}
          {currentTab === 'agents' && <AgentMonitorView />}
          {currentTab === 'settings' && <SettingsView />}
        </main>

        {/* Persistent Bottom Audio Player Dock */}
        <AudioPlayer episode={activeEpisode} />
      </div>
    </div>
  );
}
