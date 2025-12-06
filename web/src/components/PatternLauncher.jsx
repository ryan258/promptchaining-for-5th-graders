import { useEffect, useMemo, useRef, useState } from 'react'
import { BookOpen, Loader2, Send } from 'lucide-react'
import MultiColumnViewer from './MultiColumnViewer'

const FIELD_CONFIG = {
  scientific_method: [
    { key: 'hypothesis', label: 'Hypothesis', placeholder: 'MS fatigue is worsened by dehydration' },
    { key: 'context', label: 'Context', placeholder: 'What makes this hypothesis interesting?', type: 'textarea' },
    { key: 'evidence_sources', label: 'Evidence sources (one per line)', type: 'textarea' }
  ],
  socratic_dialogue: [
    { key: 'belief', label: 'Belief to test', placeholder: 'AI will replace most doctors' },
    { key: 'teacher_persona', label: 'Questioner persona', placeholder: 'Philosopher' },
    { key: 'depth', label: 'Rounds', type: 'number', placeholder: '5' }
  ],
  design_thinking: [
    { key: 'problem', label: 'Problem to solve', placeholder: 'Medication adherence for MS patients' },
    { key: 'target_user', label: 'Target user', placeholder: 'MS patient managing fatigue' },
    { key: 'constraints', label: 'Constraints (one per line)', type: 'textarea' }
  ],
  judicial_reasoning: [
    { key: 'case', label: 'Case', placeholder: 'Should insurance cover off-label MS treatments?' },
    { key: 'relevant_principles', label: 'Principles (one per line)', type: 'textarea' },
    { key: 'precedents', label: 'Precedents (one per line)', type: 'textarea' }
  ],
  five_whys: [
    { key: 'problem', label: 'Problem', placeholder: 'I missed my medication dose' },
    { key: 'context', label: 'Context', placeholder: 'What happened around the miss?', type: 'textarea' },
    { key: 'depth', label: 'Whys', type: 'number', placeholder: '5' }
  ]
}

const PATTERN_LABELS = {
  scientific_method: 'Scientific Method',
  socratic_dialogue: 'Socratic Dialogue',
  design_thinking: 'Design Thinking',
  judicial_reasoning: 'Judicial Reasoning',
  five_whys: '5 Whys'
}

function normalizeArrayInput(value) {
  if (!value) return undefined
  return value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function buildColumns(pattern, result) {
  if (!result) return []

  if (pattern === 'design_thinking') {
    return [
      { title: 'Empathize', content: result.empathize },
      { title: 'Define', content: result.define },
      { title: 'Ideate', content: result.ideate },
      { title: 'Prototype', content: result.prototype },
      { title: 'Test', content: result.test }
    ]
  }

  if (pattern === 'scientific_method') {
    return [
      { title: 'Observations', content: result.observations },
      { title: 'Predictions', content: result.predictions },
      { title: 'Experimental Design', content: result.experimental_design },
      { title: 'Analysis', content: result.analysis },
      { title: 'Conclusion', content: result.conclusion }
    ]
  }

  if (pattern === 'five_whys') {
    return [
      { title: 'Problem', content: result.problem },
      { title: 'Why Chain', content: result.whys },
      { title: 'Synthesis', content: result.synthesis }
    ]
  }

  if (pattern === 'judicial_reasoning') {
    return [
      { title: 'Facts', content: result.facts },
      { title: 'Principles', content: result.principles },
      { title: 'Arguments', content: result.arguments },
      { title: 'Ruling', content: result.ruling }
    ]
  }

  if (pattern === 'socratic_dialogue') {
    return [
      { title: 'Belief', content: result.initial_belief },
      { title: 'Dialogue', content: result.dialogue },
      { title: 'Synthesis', content: result.synthesis }
    ]
  }

  return []
}

export default function PatternLauncher() {
  const [patterns, setPatterns] = useState([])
  const [patternsLoading, setPatternsLoading] = useState(true)
  const [selectedPattern, setSelectedPattern] = useState('')
  const [formValues, setFormValues] = useState({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [metadata, setMetadata] = useState(null)
  const [error, setError] = useState(null)
  const requestIdRef = useRef(0)

  useEffect(() => {
    const controller = new AbortController()
    fetch('/api/patterns', { signal: controller.signal })
      .then((res) => res.json())
      .then((data) => {
        setPatterns(data)
        if (data.length > 0) {
          setSelectedPattern(data[0].name)
        }
        setPatternsLoading(false)
      })
      .catch((err) => {
        if (err.name !== 'AbortError') setError(err.message)
        setPatternsLoading(false)
      })
    return () => controller.abort()
  }, [])

  const fields = useMemo(() => FIELD_CONFIG[selectedPattern] || [], [selectedPattern])

  useEffect(() => {
    setFormValues({})
    setResult(null)
    setMetadata(null)
    setError(null)
    requestIdRef.current += 1
  }, [selectedPattern])

  const handleChange = (key, value) => {
    setFormValues((prev) => ({ ...prev, [key]: value }))
  }

  const handleRun = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    setMetadata(null)
    const currentRequest = ++requestIdRef.current

    const payload = {
      ...formValues,
      evidence_sources: formValues.evidence_sources
        ? normalizeArrayInput(formValues.evidence_sources)
        : undefined,
      constraints: formValues.constraints ? normalizeArrayInput(formValues.constraints) : undefined,
      relevant_principles: formValues.relevant_principles
        ? normalizeArrayInput(formValues.relevant_principles)
        : undefined,
      precedents: formValues.precedents ? normalizeArrayInput(formValues.precedents) : undefined
    }

    try {
      const response = await fetch(`/api/patterns/${selectedPattern}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Pattern execution failed')
      }
      if (currentRequest === requestIdRef.current) {
        setResult(data.result)
        setMetadata(data.metadata)
      }
    } catch (err) {
      if (err.name !== 'AbortError') setError(err.message)
    } finally {
      if (currentRequest === requestIdRef.current) {
        setLoading(false)
      }
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-xl bg-purple-500/20 border border-purple-400/30">
          <BookOpen className="text-purple-200" />
        </div>
        <div>
          <h2 className="text-xl font-bold">Reasoning Pattern Launcher</h2>
          <p className="text-sm text-gray-400">Run expert reasoning flows without the CLI.</p>
        </div>
      </div>

      <div className="glass-card space-y-4">
        <div className="flex flex-wrap gap-2">
          {patternsLoading && <span className="text-xs text-gray-400">Loading patterns…</span>}
          {!patternsLoading &&
            patterns.map((pattern) => (
              <button
                key={pattern.name}
                type="button"
                onClick={() => setSelectedPattern(pattern.name)}
                className={`px-3 py-2 text-sm border ${
                  selectedPattern === pattern.name
                    ? 'bg-purple-500/20 border-purple-400/50 text-purple-100'
                    : 'bg-slate-900/40 border-white/10 text-gray-200'
                }`}
              >
                {PATTERN_LABELS[pattern.name] || pattern.name}
              </button>
            ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {fields.map((field) => (
            <div key={field.key} className="md:col-span-1">
              <label className="text-xs uppercase tracking-wide text-gray-400 block mb-1">
                {field.label}
              </label>
              {field.type === 'textarea' ? (
                <textarea
                  rows={field.rows || 3}
                  value={formValues[field.key] || ''}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  placeholder={field.placeholder}
                />
              ) : (
                <input
                  type={field.type || 'text'}
                  value={formValues[field.key] || ''}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  placeholder={field.placeholder}
                />
              )}
            </div>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <button onClick={handleRun} disabled={loading} className="flex items-center gap-2">
            {loading ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
            {loading ? 'Running pattern...' : 'Run pattern'}
          </button>
          {error && <span className="text-sm text-red-300">{error}</span>}
        </div>
      </div>

      {result && (
        <div className="space-y-4">
          <MultiColumnViewer
            title={PATTERN_LABELS[selectedPattern] || selectedPattern}
            subtitle={metadata?.hypothesis || metadata?.problem || metadata?.case}
            columns={buildColumns(selectedPattern, result)}
          />

          <div className="glass-card">
            <p className="text-xs uppercase tracking-wide text-gray-400 mb-2">Metadata</p>
            <div className="flex flex-wrap gap-2 text-sm text-gray-300">
              {Object.entries(metadata || {}).map(([key, value]) => (
                <span
                  key={key}
                  className="px-3 py-1 rounded-full bg-slate-900/40 border border-white/10 text-xs"
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
