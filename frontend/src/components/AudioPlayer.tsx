import React, { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';
import {
  Play,
  Pause,
  RotateCcw,
  Volume2,
  VolumeX,
  Download,
  Gauge,
  Sparkles,
  FileText
} from 'lucide-react';
import { PodcastEpisode } from '../types';

interface AudioPlayerProps {
  episode: PodcastEpisode | null;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ episode }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<WaveSurfer | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.85);
  const [isMuted, setIsMuted] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1.0);

  const audioUrl = episode ? `/api/podcasts/${episode.id}/audio` : null;

  useEffect(() => {
    if (!containerRef.current || !audioUrl) return;

    if (wavesurferRef.current) {
      wavesurferRef.current.destroy();
    }

    const ws = WaveSurfer.create({
      container: containerRef.current,
      waveColor: '#3d4757',
      progressColor: '#8b5cf6',
      cursorColor: '#c084fc',
      barWidth: 2,
      barGap: 1.5,
      barRadius: 2,
      height: 44,
      normalize: true
    });

    wavesurferRef.current = ws;
    ws.load(audioUrl);

    ws.on('ready', () => {
      setDuration(ws.getDuration());
      ws.setVolume(isMuted ? 0 : volume);
    });

    ws.on('audioprocess', () => {
      setCurrentTime(ws.getCurrentTime());
    });

    ws.on('play', () => setIsPlaying(true));
    ws.on('pause', () => setIsPlaying(false));
    ws.on('finish', () => setIsPlaying(false));

    return () => {
      ws.destroy();
    };
  }, [audioUrl]);

  const togglePlay = () => {
    if (wavesurferRef.current) {
      wavesurferRef.current.playPause();
    }
  };

  const handleSeekBack = () => {
    if (wavesurferRef.current) {
      wavesurferRef.current.seekTo(Math.max(0, (currentTime - 10) / (duration || 1)));
    }
  };

  const toggleMute = () => {
    if (!wavesurferRef.current) return;
    const nextMuted = !isMuted;
    setIsMuted(nextMuted);
    wavesurferRef.current.setVolume(nextMuted ? 0 : volume);
  };

  const cycleSpeed = () => {
    const speeds = [1.0, 1.25, 1.5, 0.85];
    const next = speeds[(speeds.indexOf(playbackRate) + 1) % speeds.length];
    setPlaybackRate(next);
    if (wavesurferRef.current) {
      wavesurferRef.current.setPlaybackRate(next);
    }
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  if (!episode || episode.status !== 'completed') {
    return null;
  }

  return (
    <div className="h-24 bg-charcoal-900 border-t border-charcoal-800 px-6 flex items-center justify-between gap-6 shrink-0 z-30 shadow-2xl">
      {/* Episode Meta */}
      <div className="w-64 min-w-0">
        <div className="text-sm font-semibold text-slate-100 truncate flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-purple-400 shrink-0" />
          <span>{episode.title}</span>
        </div>
        <div className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
          <span>{episode.rendered_segments || episode.total_segments} turns</span>
          <span>•</span>
          <span className="font-mono text-purple-300">
            {episode.integrated_lufs ? `${episode.integrated_lufs.toFixed(1)} LUFS` : '-16 LUFS'}
          </span>
          <span>•</span>
          <span className="font-mono text-cyan-300">
            {episode.true_peak_dbtp ? `${episode.true_peak_dbtp.toFixed(1)} dBTP` : '-1.0 dBTP'}
          </span>
        </div>
      </div>

      {/* Main Playback & Waveform */}
      <div className="flex-1 max-w-3xl flex flex-col items-center gap-1.5">
        <div className="w-full flex items-center gap-3">
          <button
            onClick={handleSeekBack}
            className="p-1.5 text-slate-400 hover:text-slate-200 transition"
            title="Seek back 10s"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          <button
            onClick={togglePlay}
            className="w-10 h-10 rounded-full bg-purple-600 hover:bg-purple-500 text-white flex items-center justify-center transition shadow-lg shadow-purple-600/30 shrink-0"
          >
            {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
          </button>

          <span className="text-xs font-mono text-slate-400 w-10 text-right">
            {formatTime(currentTime)}
          </span>

          {/* Waveform Container */}
          <div ref={containerRef} className="flex-1 cursor-pointer" />

          <span className="text-xs font-mono text-slate-400 w-10">
            {formatTime(duration)}
          </span>
        </div>
      </div>

      {/* Controls & Multi-Format Downloads */}
      <div className="flex items-center gap-3">
        {/* Speed toggle */}
        <button
          onClick={cycleSpeed}
          className="px-2 py-1 rounded bg-charcoal-800 text-xs font-mono text-slate-300 hover:bg-charcoal-750 transition"
        >
          {playbackRate}x
        </button>

        {/* Volume */}
        <button onClick={toggleMute} className="p-1.5 text-slate-400 hover:text-slate-200">
          {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
        </button>

        <div className="h-4 w-px bg-charcoal-700 mx-1" />

        {/* Export dropdown / buttons */}
        <div className="flex items-center gap-1.5">
          <a
            href={`/api/podcasts/${episode.id}/download/mp3`}
            download
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 border border-charcoal-700 text-xs font-medium text-slate-300 transition"
            title="Download Broadcast MP3 (320 kbps)"
          >
            <Download className="w-3.5 h-3.5" />
            <span>MP3</span>
          </a>

          <a
            href={`/api/podcasts/${episode.id}/download/wav`}
            download
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 border border-charcoal-700 text-xs font-medium text-slate-300 transition"
            title="Download Master WAV (24-bit PCM)"
          >
            <Download className="w-3.5 h-3.5" />
            <span>WAV</span>
          </a>

          <a
            href={`/api/podcasts/${episode.id}/download/srt`}
            download
            className="flex items-center gap-1 px-2 py-1.5 rounded-lg bg-charcoal-800 hover:bg-purple-600/20 hover:text-purple-300 border border-charcoal-700 text-xs font-medium text-slate-300 transition"
            title="Download Subtitles (SRT)"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>SRT</span>
          </a>
        </div>
      </div>
    </div>
  );
};
