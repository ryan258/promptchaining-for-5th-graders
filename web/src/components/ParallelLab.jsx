import { useEffect, useMemo, useState } from 'react'
import { Swords, Gauge, Loader2, Play, Shield, Gavel } from 'lucide-react'


const DEFAULT_CHAINS = [
  { value: 'scientific_method', label: 'Scientific Method' },
  { value: 'design_thinking', label: 'Design Thinking' },
  { value: 'five_whys', label: '5 Whys' }
]


function safeRender(value) {
  if (value === null || value === undefined) return ''
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value, null, 2)
    } catch (e) {
      return String(value)
    }
  }
  return String(value)
}

function DebateFeed({ result, metadata }) {
  if (!result) return null
  const { opening, rounds, judgment } = result

  // Parse judgment if it's a string, or use it directly if it's an object
  const judgeData = useMemo(() => {
    if (!judgment) return {}
    if (typeof judgment === 'object') return judgment
    try {
      return JSON.parse(judgment)
    } catch (e) {
      console.warn('Failed to parse judgment:', e)
      // Fallback: try to preserve as much as possible, or just wrap the string
      return { reasoning: judgment, winner: 'Undecided (Parse Error)' }
    }
  }, [judgment])

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold text-white">Red vs Blue Debate</h3>
        <p className="text-gray-400">{safeRender(metadata?.topic)}</p>
      </div>

      {/* Opening Statement */}
      {opening && (
        <div className="glass-card border-l-4 border-blue-500">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-semibold text-blue-100">Blue Team: Opening Statement</h4>
            <span className="px-2 py-1 text-xs rounded bg-blue-500/20 text-blue-200 border border-blue-500/30">Defense</span>
          </div>
          <div className="space-y-4 text-gray-300">
            <div>
              <strong className="text-blue-200 block mb-1">Thesis</strong>
              <p className="whitespace-pre-wrap">{safeRender(opening.thesis)}</p>
            </div>
            <div className="grid gap-2">
              {Array.isArray(opening.arguments) && opening.arguments.map((arg, i) => (
                <div key={i} className="bg-slate-900/30 p-3 rounded">
                  <strong className="text-blue-200">{safeRender(arg.point)}:</strong> {safeRender(arg.reasoning)}
                </div>
              ))}
            </div>
            <div>
              <strong className="text-blue-200 block mb-1">Conclusion</strong>
              <p className="whitespace-pre-wrap">{safeRender(opening.conclusion)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Rounds Feed */}
      <div className="space-y-6 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
        {(!rounds || rounds.length === 0) && (
          <div className="text-center p-8 glass-card text-gray-400 italic">
            No debate rounds generated yet.
          </div>
        )}
        {Array.isArray(rounds) && rounds.map((round, idx) => (
          <div key={idx} className="relative">
            <div className="sticky top-4 z-10 flex justify-center mb-4">
              <span className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-mono text-gray-400 shadow-xl">
                Round {safeRender(round.round)}
              </span>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              {/* Red Attack */}
              <div className="glass-card border-l-4 border-red-500 md:text-right">
                <div className="flex items-center justify-between md:flex-row-reverse mb-3">
                  <h5 className="font-semibold text-red-200">Red Attack</h5>
                  <Swords size={16} className="text-red-400" />
                </div>
                <div className="space-y-3 text-sm text-gray-300">
                  {Array.isArray(round.red_attack?.attacks) && round.red_attack.attacks.map((atk, i) => (
                    <div key={i} className="bg-red-900/10 p-2 rounded border border-red-500/10">
                      <strong className="text-red-200 block">{safeRender(atk.target)}</strong>
                      {safeRender(atk.attack)}
                    </div>
                  ))}
                  <div className="mt-2 text-xs text-gray-400">
                    <strong>Strongest Objection:</strong> {safeRender(round.red_attack?.strongest_objection)}
                  </div>
                </div>
              </div>

              {/* Blue Defense */}
              <div className="glass-card border-l-4 border-blue-500">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-semibold text-blue-200">Blue Defense</h5>
                  <Shield size={16} className="text-blue-400" />
                </div>
                <div className="space-y-3 text-sm text-gray-300">
                  {Array.isArray(round.blue_defense?.counters) && round.blue_defense.counters.map((counter, i) => (
                    <div key={i} className="bg-blue-900/10 p-2 rounded border border-blue-500/10">
                      <strong className="text-blue-200 block">Re: {safeRender(counter.to_attack)}</strong>
                      {safeRender(counter.counter)}
                    </div>
                  ))}
                  <div className="mt-2 text-xs text-gray-400">
                    <strong>Concessions:</strong> {safeRender(round.blue_defense?.concessions)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Judge's Dashboard */}
      <div className="glass-card border-t-4 border-amber-500 bg-gradient-to-b from-slate-900 to-amber-900/10">
        <div className="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
          <div className="p-2 bg-amber-500/20 rounded-lg">
            <Gavel className="text-amber-400" size={24} />
          </div>
          <div>
            <h3 className="text-xl font-bold text-amber-100">Final Verdict</h3>
            <p className="text-amber-200/60 text-sm">The debate has concluded.</p>
          </div>
          <div className="ml-auto text-right">
            <div className="text-xs text-gray-400 uppercase tracking-wider">Winner</div>
            <div className="text-2xl font-black text-amber-400 tracking-tight">{safeRender(judgeData.winner || metadata?.winner || 'Undecided')}</div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Scores */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-950/50 p-4 rounded-lg border border-blue-500/20">
              <div className="text-xs text-blue-300 uppercase mb-1">Blue Team Strength</div>
              <div className="text-3xl font-mono font-bold text-blue-100">{safeRender(judgeData.blue_team_strength || metadata?.blue_score || 0)}<span className="text-sm text-gray-500">/10</span></div>
            </div>
            <div className="bg-slate-950/50 p-4 rounded-lg border border-red-500/20">
              <div className="text-xs text-red-300 uppercase mb-1">Red Team Strength</div>
              <div className="text-3xl font-mono font-bold text-red-100">{safeRender(judgeData.red_team_strength || metadata?.red_score || 0)}<span className="text-sm text-gray-500">/10</span></div>
            </div>
          </div>

          {/* Highlights */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <div className="text-xs text-blue-300 uppercase flex items-center gap-2">
                <Shield size={12} /> Blue's Strongest Point
              </div>
              <div className="bg-blue-900/10 p-3 rounded border border-blue-500/10 text-sm text-gray-300">
                {safeRender(judgeData.blue_strongest || 'N/A')}
              </div>
            </div>
            <div className="space-y-2">
              <div className="text-xs text-red-300 uppercase flex items-center gap-2">
                <Swords size={12} /> Red's Best Attack
              </div>
              <div className="bg-red-900/10 p-3 rounded border border-red-500/10 text-sm text-gray-300">
                {safeRender(judgeData.red_strongest || 'N/A')}
              </div>
            </div>
          </div>

          {/* Weaknesses */}
          {judgeData.remaining_weaknesses && (
            <div className="bg-slate-950/30 p-4 rounded border border-white/5">
              <div className="text-xs text-gray-400 uppercase mb-2">Remaining Weaknesses</div>
              <ul className="list-disc list-inside text-sm text-gray-400 space-y-1">
                {Array.isArray(judgeData.remaining_weaknesses)
                  ? judgeData.remaining_weaknesses.map((w, i) => <li key={i}>{safeRender(w)}</li>)
                  : <li>{safeRender(judgeData.remaining_weaknesses)}</li>
                }
              </ul>
            </div>
          )}

          {/* Reasoning */}
          <div>
            <div className="text-xs text-gray-400 uppercase mb-2">Judge's Reasoning</div>
            <p className="text-gray-300 leading-relaxed bg-slate-950/30 p-4 rounded border border-white/5">
              {safeRender(judgeData.reasoning || judgment || metadata?.reasoning)}
            </p>
          </div>

          {/* Nuanced Conclusion */}
          {(judgeData.nuanced_conclusion || metadata?.nuanced_conclusion) && (
            <div className="bg-amber-500/10 p-4 rounded border border-amber-500/20">
              <strong className="text-amber-200 text-sm block mb-1">Nuanced Conclusion</strong>
              <p className="text-sm text-amber-100/80 italic">
                {safeRender(judgeData.nuanced_conclusion || metadata?.nuanced_conclusion)}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}



function EmergenceFeed({ result, metadata }) {
  if (!result) return null
  const { outputs, scores, analysis, winner } = result
  const qualitative = scores?.qualitative || {}
  const scoreData = scores?.scores || {}

  const formatOutput = (content) => {
    if (!content) return ''
    if (typeof content === 'object') {
      return JSON.stringify(content, null, 2)
    }
    try {
      const json = JSON.parse(content)
      return JSON.stringify(json, null, 2)
    } catch (e) {
      return content
    }
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold text-white">Emergence Comparison</h3>
        <p className="text-gray-400">{safeRender(metadata?.topic)}</p>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/20 border border-amber-500/30 text-amber-200 text-sm font-medium">
          <Gavel size={14} />
          Winner: {safeRender(winner || metadata?.winner || 'Undecided')}
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Baseline Output */}
        <div className="glass-card border-l-4 border-slate-500 flex flex-col h-[600px]">
          <div className="flex items-center justify-between mb-4 flex-shrink-0">
            <h4 className="text-lg font-semibold text-slate-200">Baseline Prompt</h4>
            <span className="px-2 py-1 text-xs rounded bg-slate-500/20 text-slate-300 border border-slate-500/30">Standard</span>
          </div>
          <div className="flex-grow overflow-auto bg-slate-950/30 p-4 rounded border border-white/5 font-mono text-xs text-gray-300">
            <pre className="whitespace-pre-wrap">{formatOutput(outputs?.baseline)}</pre>
          </div>
        </div>

        {/* Chain Output */}
        <div className="glass-card border-l-4 border-amber-500 flex flex-col h-[600px]">
          <div className="flex items-center justify-between mb-4 flex-shrink-0">
            <h4 className="text-lg font-semibold text-amber-200">Chain Output</h4>
            <span className="px-2 py-1 text-xs rounded bg-amber-500/20 text-amber-200 border border-amber-500/30">Emergent</span>
          </div>
          <div className="flex-grow overflow-auto bg-slate-950/30 p-4 rounded border border-white/5 font-mono text-xs text-gray-300">
            <pre className="whitespace-pre-wrap">{formatOutput(outputs?.chain)}</pre>
          </div>
        </div>
      </div>

      {/* Analysis & Metrics */}
      <div className="glass-card border-t-4 border-amber-500 bg-gradient-to-b from-slate-900 to-amber-900/10">
        <h3 className="text-xl font-bold text-amber-100 mb-6">Analysis & Metrics</h3>

        <div className="space-y-8">
          {/* Summary */}
          <div className="bg-amber-500/10 p-4 rounded border border-amber-500/20">
            <strong className="text-amber-200 block text-sm uppercase tracking-wider mb-2">Executive Summary</strong>
            <p className="text-amber-100/90 leading-relaxed">
              {safeRender(qualitative.summary || analysis)}
            </p>
          </div>

          {/* Detailed Scores */}
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <strong className="text-slate-400 block text-xs uppercase tracking-wider mb-3">Baseline Performance</strong>
              <div className="space-y-3">
                {Object.entries(scoreData.approach_b || {}).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 capitalize">{key}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-slate-500" style={{ width: `${value * 10}%` }} />
                      </div>
                      <span className="font-mono text-slate-300 w-6 text-right">{value}</span>
                    </div>
                  </div>
                ))}
              </div>
              {Array.isArray(qualitative.approach_b_strengths) && qualitative.approach_b_strengths.length > 0 && (
                <div className="mt-4">
                  <strong className="text-slate-500 block text-xs uppercase tracking-wider mb-1">Strengths</strong>
                  <div className="flex flex-wrap gap-1">
                    {qualitative.approach_b_strengths.map((s, i) => (
                      <span key={i} className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-xs border border-slate-700">{s}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div>
              <strong className="text-amber-400 block text-xs uppercase tracking-wider mb-3">Chain Performance</strong>
              <div className="space-y-3">
                {Object.entries(scoreData.approach_a || {}).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 capitalize">{key}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-amber-500" style={{ width: `${value * 10}%` }} />
                      </div>
                      <span className="font-mono text-amber-300 w-6 text-right">{value}</span>
                    </div>
                  </div>
                ))}
              </div>
              {Array.isArray(qualitative.approach_a_strengths) && qualitative.approach_a_strengths.length > 0 && (
                <div className="mt-4">
                  <strong className="text-amber-500/70 block text-xs uppercase tracking-wider mb-1">Strengths</strong>
                  <div className="flex flex-wrap gap-1">
                    {qualitative.approach_a_strengths.map((s, i) => (
                      <span key={i} className="px-2 py-0.5 rounded bg-amber-900/30 text-amber-300 text-xs border border-amber-500/30">{s}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Novel Insights */}
          <div className="grid md:grid-cols-2 gap-6 pt-4 border-t border-white/5">
            <div>
              <strong className="text-slate-400 block text-xs uppercase tracking-wider mb-2">Baseline's Best Insight</strong>
              <p className="text-sm text-gray-400 italic bg-slate-950/30 p-3 rounded border border-white/5">
                "{safeRender(qualitative.most_novel_insight_b || 'N/A')}"
              </p>
            </div>
            <div>
              <strong className="text-amber-400 block text-xs uppercase tracking-wider mb-2">Chain's Best Insight</strong>
              <p className="text-sm text-gray-300 italic bg-amber-900/10 p-3 rounded border border-amber-500/10">
                "{safeRender(qualitative.most_novel_insight_a || 'N/A')}"
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ParallelLab() {
  const [mode, setMode] = useState('debate')
  const [form, setForm] = useState({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [metadata, setMetadata] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    setForm({})
    setResult(null)
    setMetadata(null)
    setError(null)
  }, [mode])



  const handleChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const handleRun = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    setMetadata(null)

    try {
      if (mode === 'debate') {
        const payload = {
          topic: form.topic,
          position_to_defend: form.position_to_defend,
          rounds: parseInt(form.rounds, 10) || 3
        }
        const response = await fetch('/api/adversarial/red_vs_blue', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        const data = await response.json()
        if (!response.ok) {
          throw new Error(data.detail || 'Debate run failed')
        }
        setResult(data.result)
        setMetadata(data.metadata)
      } else {
        const payload = {
          topic: form.topic,
          chain_name: form.chain_name || DEFAULT_CHAINS[0].value,
          chain_kwargs: form.context ? { context: form.context } : undefined,
          baseline_prompt: form.baseline_prompt || undefined
        }
        const response = await fetch('/api/emergence/compare', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        const data = await response.json()
        if (!response.ok) {
          throw new Error(data.detail || 'Emergence comparison failed')
        }
        setResult(data.comparison)
        setMetadata(data.metadata)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-xl bg-amber-500/20 border border-amber-400/40">
          <Swords className="text-amber-200" />
        </div>
        <div>
          <h2 className="text-xl font-bold">Parallel Reasoning Lab</h2>
          <p className="text-sm text-gray-400">
            Run debates or compare chain vs baseline to see emergence effects.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => setMode('debate')}
          className={`px-3 py-2 text-sm border ${mode === 'debate'
            ? 'bg-amber-500/20 border-amber-400/50 text-amber-100'
            : 'bg-slate-900/40 border-white/10 text-gray-200'
            }`}
        >
          Debate: Red vs Blue
        </button>
        <button
          type="button"
          onClick={() => setMode('emergence')}
          className={`px-3 py-2 text-sm border ${mode === 'emergence'
            ? 'bg-amber-500/20 border-amber-400/50 text-amber-100'
            : 'bg-slate-900/40 border-white/10 text-gray-200'
            }`}
        >
          Emergence Compare
        </button>
      </div>

      <div className="glass-card space-y-3">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
              Topic
            </label>
            <input
              type="text"
              value={form.topic || ''}
              onChange={(e) => handleChange('topic', e.target.value)}
              placeholder="E.g., The future of AI in healthcare"
            />
          </div>
          {mode === 'debate' ? (
            <div>
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                Position to defend
              </label>
              <input
                type="text"
                value={form.position_to_defend || ''}
                onChange={(e) => handleChange('position_to_defend', e.target.value)}
                placeholder="Aggressive DMTs should be prioritized"
              />
            </div>
          ) : (
            <div>
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                Chain to test
              </label>
              <select
                value={form.chain_name || DEFAULT_CHAINS[0].value}
                onChange={(e) => handleChange('chain_name', e.target.value)}
              >
                {DEFAULT_CHAINS.map((chain) => (
                  <option key={chain.value} value={chain.value}>
                    {chain.label}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {mode === 'debate' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                Rounds
              </label>
              <input
                type="number"
                value={form.rounds || 3}
                onChange={(e) => handleChange('rounds', e.target.value)}
                min={1}
                max={5}
              />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                Context (optional)
              </label>
              <textarea
                rows={3}
                value={form.context || ''}
                onChange={(e) => handleChange('context', e.target.value)}
                placeholder="Constraints or extra details for the chain"
              />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                Baseline prompt (optional)
              </label>
              <textarea
                rows={3}
                value={form.baseline_prompt || ''}
                onChange={(e) => handleChange('baseline_prompt', e.target.value)}
                placeholder="Custom mega-prompt to compare against"
              />
            </div>
          </div>
        )}

        <div className="flex items-center gap-2">
          <button onClick={handleRun} disabled={loading || !form.topic} className="flex items-center gap-2">
            {loading ? <Loader2 className="animate-spin" size={18} /> : <Play size={18} />}
            {loading ? 'Running...' : 'Run'}
          </button>
          {error && <span className="text-sm text-red-300">{error}</span>}
        </div>
      </div>

      {result && (
        <div className="space-y-4">
          {mode === 'debate' ? (
            <DebateFeed result={result} metadata={metadata} />
          ) : (
            <EmergenceFeed result={result} metadata={metadata} />
          )}
          <div className="glass-card">
            <div className="flex items-center gap-2 mb-2">
              <Gauge className="text-amber-300" size={16} />
              <p className="text-xs uppercase tracking-wide text-gray-400">Metadata</p>
            </div>
            <div className="flex flex-wrap gap-2 text-xs text-gray-200">
              {Object.entries(metadata || {}).map(([key, value]) => (
                <span
                  key={key}
                  className="px-3 py-1 rounded-full bg-slate-900/40 border border-white/10"
                >
                  <strong className="mr-1 capitalize">{key.replace(/_/g, ' ')}:</strong>
                  {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
