import { useEffect, useState } from 'react'
import { Brain, Loader2, Play, Save, Sparkles } from 'lucide-react'
import ChainViewer from './ChainViewer'

const cognitiveMoves = [
  'decompose',
  'analogize',
  'synthesize',
  'connect',
  'critique',
  'exemplify',
  'historicize',
  'problematize',
  'apply',
  'compare'
]

function loadTemplates() {
  try {
    const saved = localStorage.getItem('metaChainTemplates')
    return { templates: saved ? JSON.parse(saved) : [], error: null }
  } catch (e) {
    return { templates: [], error: e }
  }
}

function persistTemplates(templates) {
  try {
    localStorage.setItem('metaChainTemplates', JSON.stringify(templates))
    return { success: true }
  } catch (e) {
    return { success: false, error: e }
  }
}

export default function MetaChainStudio() {
  const [goal, setGoal] = useState('')
  const [context, setContext] = useState('')
  const [selectedMoves, setSelectedMoves] = useState([])
  const [design, setDesign] = useState(null)
  const [promptEdits, setPromptEdits] = useState([])
  const [templateName, setTemplateName] = useState('')
  const [templates, setTemplates] = useState([])
  const [designing, setDesigning] = useState(false)
  const [executing, setExecuting] = useState(false)
  const [executionTrace, setExecutionTrace] = useState(null)
  const [error, setError] = useState(null)
  const [storageWarning, setStorageWarning] = useState('')
  const MAX_PROMPT_LENGTH = 10000

  useEffect(() => {
    const { templates: stored, error } = loadTemplates()
    setTemplates(stored)
    if (error) {
      setStorageWarning('Templates unavailable (storage blocked).')
    }
  }, [])

  const toggleMove = (move) => {
    setSelectedMoves((prev) =>
      prev.includes(move) ? prev.filter((m) => m !== move) : [...prev, move]
    )
  }

  const handleDesign = async () => {
    if (!goal) return
    setDesigning(true)
    setError(null)
    setExecutionTrace(null)

    try {
      const response = await fetch('/api/meta-chain/design', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          goal,
          context: {
            topic: goal,
            notes: context
          },
          constraints: selectedMoves
        })
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to design chain')
      }

      const prompts = Array.isArray(data.design.prompts) ? data.design.prompts : []
      setDesign(data.design)
      setPromptEdits(prompts)
      setTemplateName((data.design.goal || '').slice(0, 50))
    } catch (err) {
      setError(err.message)
    } finally {
      setDesigning(false)
    }
  }

  const handleExecute = async () => {
    if (!design) return
    if (!promptEdits.length || promptEdits.some((p) => !p || !p.trim())) {
      setError('Please ensure all prompts have content before executing.')
      return
    }
    setExecuting(true)
    setError(null)

    try {
      const response = await fetch('/api/meta-chain/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          design: {
            ...design,
            prompts: promptEdits
          }
        })
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to execute chain')
      }

      setExecutionTrace(data.execution_trace)
    } catch (err) {
      setError(err.message)
    } finally {
      setExecuting(false)
    }
  }

  const saveTemplate = () => {
    if (!design) return
    const name = templateName || design.goal || 'Meta chain template'
    const existing = templates.find((t) => t.name === name)
    if (existing && typeof window !== 'undefined') {
      const ok = window.confirm(`Template "${name}" exists. Overwrite it?`)
      if (!ok) return
    }

    const payload = {
      name,
      savedAt: new Date().toISOString(),
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      design: { ...design, prompts: promptEdits }
    }
    try {
      const next = [payload, ...templates.filter((t) => t.id !== payload.id)]
      setTemplates(next)
      const res = persistTemplates(next)
      if (!res.success) {
        setStorageWarning('Saving templates failed (storage blocked).')
      } else {
        setStorageWarning('')
      }
    } catch (err) {
      setStorageWarning('Saving templates failed (storage blocked).')
    }
  }

  const loadTemplate = (template) => {
    setDesign(template.design)
    setPromptEdits(template.design.prompts || [])
    setGoal(template.design.goal || '')
    setContext(template.design.context?.notes || '')
    setSelectedMoves(template.design.cognitive_moves || [])
    setExecutionTrace(null)
    setTemplateName(template.name)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-xl bg-blue-500/20 border border-blue-400/30">
          <Brain className="text-blue-300" />
        </div>
        <div>
          <h2 className="text-xl font-bold">Meta-Chain Studio</h2>
          <p className="text-sm text-gray-400">
            Design chains that design themselves. Two-phase flow: design then execute.
          </p>
        </div>
      </div>

      {/* Tool Description */}
      <div className="bg-slate-900/50 p-4 rounded-lg border border-white/5">
        <p className="text-gray-300 text-sm mb-2">
          The Meta-Chain Studio uses a "Designer AI" to build a custom reasoning chain for your specific goal.
          It selects the best cognitive moves (like "analogize" or "critique") and writes the prompts for you.
        </p>
        <div className="flex items-start gap-2 text-xs text-gray-400">
          <span className="uppercase tracking-wider font-bold text-blue-400/80 shrink-0">Output:</span>
          A fully executed custom chain, complete with intermediate steps and final result.
        </div>
      </div>

      <div className="glass-card space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-semibold text-blue-300">Goal</label>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Teach quantum physics through historical analogies"
            />
            <p className="text-[10px] text-gray-500 mt-1">What do you want the chain to achieve? Be specific.</p>
          </div>
          <div>
            <label className="text-sm font-semibold text-blue-300">Context (optional)</label>
            <textarea
              rows={2}
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Audience, constraints, or special instructions"
            />
            <p className="text-[10px] text-gray-500 mt-1">Optional details to guide the Designer AI.</p>
          </div>
        </div>

        <div>
          <p className="text-sm font-semibold text-blue-300 mb-1">Desired cognitive moves</p>
          <p className="text-[10px] text-gray-500 mb-2">Select specific reasoning steps you want the chain to include (optional).</p>
          <div className="flex flex-wrap gap-2">
            {cognitiveMoves.map((move) => {
              const isActive = selectedMoves.includes(move)
              return (
                <button
                  key={move}
                  type="button"
                  onClick={() => toggleMove(move)}
                  className={`px-3 py-2 text-sm border ${isActive
                      ? 'bg-blue-500/20 border-blue-400/50 text-blue-100'
                      : 'bg-slate-900/40 border-white/10 text-gray-200'
                    }`}
                >
                  {move.replace(/_/g, ' ')}
                </button>
              )
            })}
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={handleDesign}
            disabled={!goal || designing}
            className="flex items-center gap-2"
          >
            {designing ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
            {designing ? 'Designing chain...' : 'Design chain'}
          </button>

          <button
            onClick={handleExecute}
            disabled={!design || executing}
            className="flex items-center gap-2 bg-green-500 hover:bg-green-600 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {executing ? <Loader2 className="animate-spin" size={18} /> : <Play size={18} />}
            {executing ? 'Executing...' : 'Execute designed chain'}
          </button>

          <button
            type="button"
            onClick={saveTemplate}
            disabled={!design}
            className="flex items-center gap-2 bg-purple-500 hover:bg-purple-600"
          >
            <Save size={18} />
            Save template
          </button>
        </div>

        {error && (
          <div className="p-3 bg-red-900/40 border border-red-500/50 rounded text-sm text-red-100">
            {error}
          </div>
        )}

        {design && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-wide text-gray-400">Design reasoning</p>
                <h3 className="text-lg font-semibold">{design.goal}</h3>
              </div>
              <span className="text-xs px-3 py-1 rounded-full bg-blue-500/20 text-blue-100 border border-blue-500/40">
                {design.cognitive_moves?.length || 0} moves
              </span>
            </div>

            <div className="border border-white/10 rounded-lg p-3 bg-black/10 text-sm text-gray-200">
              {design.reasoning}
            </div>

            <div className="space-y-2">
              <p className="text-xs uppercase tracking-wide text-gray-400">Prompts</p>
              <div className="space-y-3">
                {promptEdits.map((prompt, idx) => (
                  <div key={idx} className="border border-white/10 rounded-lg p-3 bg-slate-900/40">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-gray-400">Step {idx + 1}</span>
                      <span className="text-[11px] px-2 py-1 rounded bg-blue-500/10 text-blue-100 border border-blue-500/20">
                        {design.cognitive_moves?.[idx] || 'Prompt'}
                      </span>
                    </div>
                    <textarea
                      rows={4}
                      value={prompt}
                      onChange={(e) => {
                        const value = e.target.value
                        if (value.length > MAX_PROMPT_LENGTH) return
                        const next = [...promptEdits]
                        next[idx] = value
                        setPromptEdits(next)
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
              <div className="md:col-span-2">
                <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                  Template name
                </label>
                <input
                  type="text"
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                  placeholder="Meta-chain template name"
                />
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">Saved templates</p>
                <div className="flex flex-wrap gap-2">
                  {templates.length === 0 && (
                    <span className="text-xs text-gray-500">No saved templates yet</span>
                  )}
                  {templates.map((tpl) => (
                    <button
                      key={tpl.id || tpl.name}
                      type="button"
                      onClick={() => loadTemplate(tpl)}
                      className="px-3 py-2 text-xs bg-slate-900/40 border border-white/10 hover:border-blue-400/40"
                    >
                      {tpl.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {storageWarning && (
          <div className="p-3 border border-amber-500/40 bg-amber-500/10 rounded text-xs text-amber-100">
            {storageWarning}
          </div>
        )}
      </div>

      {executionTrace && (
        <div className="glass-card">
          <ChainViewer executionTrace={executionTrace} />
        </div>
      )}
    </div>
  )
}
