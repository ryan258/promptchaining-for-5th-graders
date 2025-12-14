import { useEffect, useMemo, useRef, useState } from 'react'
import { BookOpen, Loader2, Send } from 'lucide-react'
import { normalizeArrayInput } from './patterns/utils'

import SocraticFeed from './patterns/SocraticFeed'
import FiveWhysFeed from './patterns/FiveWhysFeed'
import DesignThinkingFeed from './patterns/DesignThinkingFeed'
import ScientificMethodFeed from './patterns/ScientificMethodFeed'
import JudicialReasoningFeed from './patterns/JudicialReasoningFeed'

const FIELD_CONFIG = {
  scientific_method: [
    { key: 'hypothesis', label: 'Hypothesis', placeholder: 'MS fatigue is worsened by dehydration', help: 'The core statement you want to test scientifically.' },
    { key: 'context', label: 'Context', placeholder: 'What makes this hypothesis interesting?', type: 'textarea', help: 'Background info to help the AI understand the domain.' },
    { key: 'evidence_sources', label: 'Evidence sources (one per line)', type: 'textarea', help: 'List any specific papers, data, or observations to consider.' }
  ],
  socratic_dialogue: [
    { key: 'belief', label: 'Belief to test', placeholder: 'AI will replace most doctors', help: 'A strong opinion or claim to be challenged.' },
    { key: 'teacher_persona', label: 'Questioner persona', placeholder: 'Philosopher', help: 'The style of the Socratic questioner (e.g., Skeptic, Child, Professor).' },
    { key: 'depth', label: 'Rounds', type: 'number', placeholder: '5', help: 'How many back-and-forth exchanges to generate (3-5 is usually best).' }
  ],
  design_thinking: [
    { key: 'problem', label: 'Problem to solve', placeholder: 'Medication adherence for MS patients', help: 'The user need or pain point you want to address.' },
    { key: 'target_user', label: 'Target user', placeholder: 'MS patient managing fatigue', help: 'Who are we solving this for? Be specific.' },
    { key: 'constraints', label: 'Constraints (one per line)', type: 'textarea', help: 'Technical, financial, or physical limitations to respect.' }
  ],
  judicial_reasoning: [
    { key: 'case', label: 'Case', placeholder: 'Should insurance cover off-label MS treatments?', help: 'The legal or ethical question to be judged.' },
    { key: 'relevant_principles', label: 'Principles (one per line)', type: 'textarea', help: 'Laws, ethical guidelines, or precedents to apply.' },
    { key: 'precedents', label: 'Precedents (one per line)', type: 'textarea', help: 'Past cases or examples that might influence the ruling.' }
  ],
  five_whys: [
    { key: 'problem', label: 'Problem', placeholder: 'I missed my medication dose', help: 'The surface-level issue that occurred.' },
    { key: 'context', label: 'Context', placeholder: 'What happened around the miss?', type: 'textarea', help: 'Details about the situation when the problem happened.' },
    { key: 'depth', label: 'Whys', type: 'number', placeholder: '5', help: 'How deep to drill down (5 is the standard).' }
  ]
}

const PATTERN_INFO = {
  scientific_method: {
    label: 'Scientific Method',
    description: 'Rigorously test a hypothesis through simulated experimentation and analysis.',
    output: 'Generates a structured experimental design, predictions, and analysis of potential results.'
  },
  socratic_dialogue: {
    label: 'Socratic Dialogue',
    description: 'Explore a belief through a probing question-and-answer session with a persona.',
    output: 'Produces a transcript of the dialogue and a final synthesis of how the belief evolved.'
  },
  design_thinking: {
    label: 'Design Thinking',
    description: 'Solve a user problem using the 5-stage Design Thinking process.',
    output: 'Walks through Empathize, Define, Ideate, Prototype, and Test phases with specific artifacts for each.'
  },
  judicial_reasoning: {
    label: 'Judicial Reasoning',
    description: 'Weigh evidence and principles to reach a fair verdict on a complex case.',
    output: 'Delivers a structured judgment with facts, arguments, and a final ruling.'
  },
  five_whys: {
    label: '5 Whys',
    description: 'Drill down into a problem to find its root cause by asking "Why?" five times.',
    output: 'Visualizes the chain of causality and suggests systemic solutions.'
  }
}

export default function PatternLauncher() {
  const [patterns, setPatterns] = useState([])
  const [patternsLoading, setPatternsLoading] = useState(true)
  const [selectedPattern, setSelectedPattern] = useState('')
  const [formValues, setFormValues] = useState({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
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
                className={`px-3 py-2 text-sm border ${selectedPattern === pattern.name
                  ? 'bg-purple-500/20 border-purple-400/50 text-purple-100'
                  : 'bg-slate-900/40 border-white/10 text-gray-200'
                  }`}
              >
                {PATTERN_INFO[pattern.name]?.label || pattern.name}
              </button>
            ))}
        </div>

        {/* Pattern Description */}
        {selectedPattern && PATTERN_INFO[selectedPattern] && (
          <div className="bg-slate-950/50 p-4 rounded border border-white/5 space-y-2">
            <p className="text-gray-300 text-sm">{PATTERN_INFO[selectedPattern].description}</p>
            <div className="flex items-start gap-2 text-xs text-gray-500">
              <span className="uppercase tracking-wider font-bold text-gray-600 mt-0.5">Output:</span>
              <span>{PATTERN_INFO[selectedPattern].output}</span>
            </div>
          </div>
        )}

        {/* Input Fields */}
        <div className="grid gap-4 pt-2">
          {fields.map((field) => (
            <div key={field.key}>
              <label className="block text-sm font-semibold text-gray-400 mb-1">
                {field.label}
              </label>
              {field.type === 'textarea' ? (
                <textarea
                  value={formValues[field.key] || ''}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  placeholder={field.placeholder}
                  className="w-full h-24 bg-slate-900/50 border border-white/10 rounded p-3 text-sm text-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500 transition-all font-mono"
                />
              ) : field.type === 'number' ? (
                <input
                  type="number"
                  value={formValues[field.key] || ''}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  placeholder={field.placeholder}
                  className="w-full bg-slate-900/50 border border-white/10 rounded p-2 text-sm text-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500 transition-all font-mono"
                />
              ) : (
                <input
                  type="text"
                  value={formValues[field.key] || ''}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  placeholder={field.placeholder}
                  className="w-full bg-slate-900/50 border border-white/10 rounded p-2 text-sm text-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500 transition-all font-mono"
                />
              )}
              {field.help && <p className="text-xs text-gray-500 mt-1">{field.help}</p>}
            </div>
          ))}
        </div>

        <div className="pt-4 flex justify-end">
          <button
            onClick={handleRun}
            disabled={loading || !selectedPattern}
            className="flex items-center gap-2 px-6 py-2 bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
            {loading ? 'Running Pattern...' : 'Run Pattern'}
          </button>
        </div>

        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded text-red-200 text-sm">
            {error}
          </div>
        )}
      </div>

      {result && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          {selectedPattern === 'socratic_dialogue' && <SocraticFeed result={result} />}
          {selectedPattern === 'five_whys' && <FiveWhysFeed result={result} />}
          {selectedPattern === 'design_thinking' && <DesignThinkingFeed result={result} />}
          {selectedPattern === 'scientific_method' && <ScientificMethodFeed result={result} />}
          {selectedPattern === 'judicial_reasoning' && <JudicialReasoningFeed result={result} />}
        </div>
      )}
    </div>
  )
}
