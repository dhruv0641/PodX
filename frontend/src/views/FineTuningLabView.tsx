import React, { useState, useEffect } from 'react';
import {
  Layers,
  Upload,
  Play,
  CheckCircle2,
  AlertTriangle,
  Activity,
  Cpu,
  ShieldCheck,
  TrendingDown
} from 'lucide-react';
import { FineTuningDataset, FineTuningJob } from '../types';

export const FineTuningLabView: React.FC = () => {
  const [datasets, setDatasets] = useState<FineTuningDataset[]>([]);
  const [jobs, setJobs] = useState<FineTuningJob[]>([]);
  const [datasetName, setDatasetName] = useState('');
  const [speakerName, setSpeakerName] = useState('');
  const [consentConfirmed, setConsentConfirmed] = useState(false);
  const [selectedDatasetId, setSelectedDatasetId] = useState('');
  const [baseModel, setBaseModel] = useState('qwen3-tts-0.6b');
  const [epochs, setEpochs] = useState(5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetch('/api/finetuning/datasets')
      .then((r) => r.json())
      .then((d) => setDatasets(d || []))
      .catch(() => {});

    fetch('/api/finetuning/jobs')
      .then((r) => r.json())
      .then((d) => setJobs(d || []))
      .catch(() => {});
  }, []);

  const handleCreateDataset = async () => {
    if (!datasetName.trim() || !speakerName.trim() || !consentConfirmed) return;
    setIsSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('name', datasetName);
      formData.append('speaker_name', speakerName);
      formData.append('consent_confirmed', 'true');

      const res = await fetch('/api/finetuning/datasets', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        const newDs = await res.json();
        setDatasets((prev) => [newDs, ...prev]);
        setDatasetName('');
        setSpeakerName('');
        setConsentConfirmed(false);
      }
    } catch (e) {
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLaunchJob = async () => {
    if (!selectedDatasetId) return;
    try {
      const res = await fetch('/api/finetuning/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dataset_id: selectedDatasetId,
          base_model: baseModel,
          total_epochs: epochs
        })
      });
      if (res.ok) {
        const newJob = await res.json();
        setJobs((prev) => [newJob, ...prev]);
      }
    } catch (e) {}
  };

  return (
    <div className="h-full p-8 max-w-6xl mx-auto space-y-8 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Layers className="w-6 h-6 text-purple-400" />
          <span>Speech Model Fine-Tuning Lab</span>
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Train custom single-speaker LoRA adapters with VRAM-aware gradient checkpointing.
          Enforces strict consent provenance and audio quality filtering.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Dataset Ingestion */}
        <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-4">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Upload className="w-4 h-4 text-purple-400" />
            <span>Dataset Ingestion & Provenance</span>
          </h3>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Dataset Name</label>
              <input
                type="text"
                value={datasetName}
                onChange={(e) => setDatasetName(e.target.value)}
                placeholder="e.g. Executive Narrator Studio v1"
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Speaker Attribution</label>
              <input
                type="text"
                value={speakerName}
                onChange={(e) => setSpeakerName(e.target.value)}
                placeholder="Speaker Name / Fictional Identity"
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            {/* Mandatory Consent Checkbox */}
            <div className="p-3.5 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-2">
              <label className="flex items-start gap-2.5 cursor-pointer text-xs text-slate-300 leading-relaxed">
                <input
                  type="checkbox"
                  checked={consentConfirmed}
                  onChange={(e) => setConsentConfirmed(e.target.checked)}
                  className="mt-0.5 rounded accent-purple-600 cursor-pointer"
                />
                <span>
                  I confirm that all voice samples have verified consent and rights for synthetic model fine-tuning.
                </span>
              </label>
            </div>

            <button
              onClick={handleCreateDataset}
              disabled={isSubmitting || !datasetName || !speakerName || !consentConfirmed}
              className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-medium text-xs transition"
            >
              Register Training Dataset
            </button>
          </div>
        </div>

        {/* Training Job Launcher */}
        <div className="p-6 rounded-2xl bg-charcoal-900 border border-charcoal-800 space-y-4">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Activity className="w-4 h-4 text-purple-400" />
            <span>Launch LoRA Adaptation Job</span>
          </h3>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Target Dataset</label>
              <select
                value={selectedDatasetId}
                onChange={(e) => setSelectedDatasetId(e.target.value)}
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
              >
                <option value="">Select a dataset...</option>
                {datasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.speaker_name})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Base Audio Model</label>
              <select
                value={baseModel}
                onChange={(e) => setBaseModel(e.target.value)}
                className="w-full bg-charcoal-950 border border-charcoal-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
              >
                <option value="qwen3-tts-0.6b">Qwen3-TTS 0.6B CustomVoice (LoRA)</option>
                <option value="kokoro-adapter">Kokoro-82M Acoustic Adapter</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">
                Epochs: <span className="font-mono text-purple-300">{epochs}</span>
              </label>
              <input
                type="range"
                min="3"
                max="20"
                value={epochs}
                onChange={(e) => setEpochs(parseInt(e.target.value))}
                className="w-full accent-purple-600 cursor-pointer"
              />
            </div>

            <button
              onClick={handleLaunchJob}
              disabled={!selectedDatasetId}
              className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-medium text-xs transition flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4 ml-0.5" />
              <span>Start Training Job</span>
            </button>
          </div>
        </div>
      </div>

      {/* Active & Recent Training Jobs */}
      <div className="rounded-2xl bg-charcoal-900 border border-charcoal-800 overflow-hidden">
        <div className="p-5 border-b border-charcoal-800">
          <h3 className="font-semibold text-slate-100 text-sm">Fine-Tuning Jobs & Checkpoints</h3>
        </div>

        {jobs.length === 0 ? (
          <div className="p-10 text-center text-slate-500 text-xs">
            No active or past fine-tuning jobs recorded.
          </div>
        ) : (
          <div className="divide-y divide-charcoal-800">
            {jobs.map((job) => (
              <div key={job.id} className="p-5 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-sm text-white">{job.base_model}</div>
                  <div className="text-xs text-slate-400 mt-0.5 font-mono">
                    Epoch {job.current_epoch} / {job.total_epochs} • Loss:{' '}
                    {job.current_loss ? job.current_loss.toFixed(4) : 'N/A'}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-purple-500/10 text-purple-300 border border-purple-500/20">
                    {job.status.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
