import { useEffect, useMemo, useState } from 'react'
import { Swords, Gauge, Loader2, Play } from 'lucide-react'
import MultiColumnViewer from './MultiColumnViewer'

const DEFAULT_CHAINS = [
  { value: 'scientific_method', label: 'Scientific Method' },
  { value: 'design_thinking', label: 'Design Thinking' },
  { value: 'five_whys', label: '5 Whys' }
]

function buildDebateColumns(result, metadata) {
  if (!result) return []
  const rounds = result.rounds || []

  return [
    {
      title: 'Blue Team',
      badge: 'Defense',
      content: {
        opening: result.opening,
        defenses: rounds.map((round) => ({
          round: round.round,
          defense: round.blue_defense
        }))
      }
    },
    {
      title: 'Red Team',
      badge: 'Attack',
      content: rounds.map((round) => ({
        round: round.round,
        attack: round.red_attack
      }))
    },
    {
      title: 'Judge',
      badge: metadata?.winner ? `Winner: ${metadata.winner}` : 'Judgment',
      content: result.judgment
    }
  ]
}

function buildEmergenceColumns(result, metadata) {
  if (!result) return []
  return [
    { title: 'Chain Output', content: result.outputs?.chain },
    { title: 'Baseline Output', content: result.outputs?.baseline },
    {
      title: 'Scores & Winner',
      badge: metadata?.winner || result.winner,
      content: {
        scores: result.scores,
        performance: result.performance,
        analysis: result.analysis
      }
    }
  ]
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

  const columns = useMemo(() => {
    if (mode === 'debate') return buildDebateColumns(result, metadata)
    if (mode === 'emergence') return buildEmergenceColumns(result, metadata)
    return []
  }, [mode, result, metadata])

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
          className={`px-3 py-2 text-sm border ${
            mode === 'debate'
              ? 'bg-amber-500/20 border-amber-400/50 text-amber-100'
              : 'bg-slate-900/40 border-white/10 text-gray-200'
          }`}
        >
          Debate: Red vs Blue
        </button>
        <button
          type="button"
          onClick={() => setMode('emergence')}
          className={`px-3 py-2 text-sm border ${
            mode === 'emergence'
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
          <MultiColumnViewer
            title={mode === 'debate' ? 'Red vs Blue Debate' : 'Emergence Comparison'}
            subtitle={metadata?.topic || form.topic}
            columns={columns}
          />
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
