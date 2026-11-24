import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Upload,
  Sparkles,
  Radio,
  Sliders,
  CheckCircle2,
  FileText,
  Volume2,
  Play
} from 'lucide-react';
import { ChatMessage, PodcastEpisode } from '../types';
import { ViewTab } from '../components/Sidebar';

interface NewChatViewProps {
  onSelectTab: (tab: ViewTab) => void;
  onPlayEpisode: (ep: PodcastEpisode) => void;
}

export const NewChatView: React.FC<NewChatViewProps> = ({ onSelectTab, onPlayEpisode }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputScript, setInputScript] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [jobProgress, setJobProgress] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Sample templates for one-click insertion
  const sampleEliteScript = `PODCAST TITLE: The Psychology of Elite Decision Making
MODE: Two-host intellectual discussion
QUALITY: Extreme
LANGUAGE: English
HOST 1: Alexander — M01
HOST 2: Sophia — F01
STYLE: Sophisticated, intellectual, engaging and conversational.

M01 [calm, thoughtful]: The most successful people do not necessarily make more decisions. They make better decisions.

[pause: 1.2 seconds]

F01 [curious, analytical]: That's an interesting distinction. But what actually separates a good decision from a great one?

M01 [confident, measured]: It begins with understanding uncertainty. Elite operators do not seek guarantees; they map probabilities and protect optionality.

[pause: 0.8 seconds]

F01 [analytical, engaged]: Which requires detaching our ego from the outcome. In complex systems, a sound process can still yield a temporary setback.

M01 [authoritative, reflective]: Exactly. When you master your cognitive biases, uncertainty ceases to be a threat—it becomes your competitive edge.`;

  useEffect(() => {
    // Initial greeting
    setMessages([
      {
        id: 'welcome',
        conversation_id: 'default',
        role: 'assistant',
        content: `Welcome to **Elite Knowledge — AI Podcast Studio**.\n\nSubmit your full script below. The studio automatically separates spoken dialogue from bracketed directions like \`[calm, thoughtful]\`, synthesizes distinct multi-speaker voices, and applies broadcast mastering (-16 LUFS).`,
        created_at: Date.now()
      }
    ]);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, jobProgress]);

  // SSE Listener for background job
  useEffect(() => {
    if (!activeJobId) return;

    const eventSource = new EventSource(`/api/podcasts/${activeJobId}/progress`);
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setJobProgress(data);
        if (data.status === 'completed' || data.status === 'failed') {
          setIsLoading(false);
          eventSource.close();
          // Fetch final episode details
          fetch(`/api/podcasts/${activeJobId}`)
            .then((r) => r.json())
            .then((res) => {
              if (res.episode) onPlayEpisode(res.episode);
            });
        }
      } catch (e) {}
    };

    return () => {
      eventSource.close();
    };
  }, [activeJobId]);

  const handleSubmit = async (scriptToSubmit?: string) => {
    const text = scriptToSubmit || inputScript;
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      conversation_id: 'default',
      role: 'user',
      content: text,
      created_at: Date.now()
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputScript('');
    setIsLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();

      const assistantMsg: ChatMessage = {
        id: String(Date.now() + 1),
        conversation_id: data.conversation_id,
        role: 'assistant',
        content: data.reply,
        created_at: Date.now()
      };
      setMessages((prev) => [...prev, assistantMsg]);

      if (data.is_podcast_job && data.episode_id) {
        setActiveJobId(data.episode_id);
      } else {
        setIsLoading(false);
      }
    } catch (e) {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setInputScript(content);
    };
    reader.readAsText(file);
  };

  return (
    <div className="flex flex-col h-full bg-charcoal-950">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex gap-4 max-w-4xl ${m.role === 'user' ? 'ml-auto justify-end' : ''}`}
          >
            {m.role === 'assistant' && (
              <div className="w-9 h-9 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30 flex items-center justify-center shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
            )}
            <div
              className={`p-5 rounded-2xl text-sm leading-relaxed ${
                m.role === 'user'
                  ? 'bg-purple-600 text-white max-w-2xl font-mono text-xs'
                  : 'bg-charcoal-900 border border-charcoal-800 text-slate-200'
              }`}
            >
              <div className="whitespace-pre-wrap">{m.content}</div>
            </div>
          </div>
        ))}

        {/* Live SSE Telemetry Card */}
        {jobProgress && (
          <div className="max-w-2xl bg-charcoal-900 border border-purple-500/30 rounded-2xl p-6 space-y-4 glow-purple">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Radio className="w-4 h-4 text-purple-400 animate-pulse" />
                <span className="font-semibold text-sm text-slate-100">
                  {jobProgress.stage || 'Synthesizing'}
                </span>
              </div>
              <span className="font-mono text-sm font-bold text-purple-300">
                {Math.round(jobProgress.progress)}%
              </span>
            </div>

            {/* Progress bar */}
            <div className="w-full h-2 rounded-full bg-charcoal-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-300"
                style={{ width: `${jobProgress.progress}%` }}
              />
            </div>

            <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>
                Segments: {jobProgress.rendered_segments || 0} / {jobProgress.total_segments || 0}
              </span>
              <span>Status: {jobProgress.status}</span>
            </div>

            {jobProgress.status === 'completed' && (
              <div className="pt-2 flex items-center gap-3">
                <button
                  onClick={() => onSelectTab('studio')}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition"
                >
                  <Sliders className="w-4 h-4" />
                  <span>Open in Multi-Track Studio</span>
                </button>
              </div>
            )}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Script Input Deck */}
      <div className="p-4 bg-charcoal-900/90 border-t border-charcoal-800">
        <div className="max-w-4xl mx-auto space-y-2">
          {/* Quick templates */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Quick Template:</span>
            <button
              onClick={() => handleSubmit(sampleEliteScript)}
              className="text-xs px-2.5 py-1 rounded bg-charcoal-800 text-purple-300 hover:bg-charcoal-750 transition flex items-center gap-1 border border-purple-500/20"
            >
              <Sparkles className="w-3 h-3" />
              <span>Elite Decision Making (M01 & F01)</span>
            </button>
          </div>

          <div className="relative rounded-2xl bg-charcoal-950 border border-charcoal-800 focus-within:border-purple-500/50 transition">
            <textarea
              value={inputScript}
              onChange={(e) => setInputScript(e.target.value)}
              placeholder="Paste your multi-speaker script here (e.g. M01 [calm]: Welcome to our discussion...)"
              rows={4}
              className="w-full bg-transparent px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-none"
            />

            <div className="flex items-center justify-between px-3 py-2 border-t border-charcoal-900">
              <label className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-slate-200 hover:bg-charcoal-800 cursor-pointer transition">
                <Upload className="w-3.5 h-3.5" />
                <span>Upload Script (.txt, .md)</span>
                <input type="file" accept=".txt,.md,.json" onChange={handleFileUpload} className="hidden" />
              </label>

              <button
                onClick={() => handleSubmit()}
                disabled={isLoading || !inputScript.trim()}
                className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-medium text-xs transition shadow-md shadow-purple-600/30"
              >
                <span>Generate Podcast</span>
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
