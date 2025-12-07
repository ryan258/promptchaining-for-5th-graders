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

function normalizeArrayInput(value) {
  if (!value) return undefined
  return value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function SocraticFeed({ result }) {
  if (!result) return null
  const { initial_belief, rounds, synthesis } = result

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Initial Belief */}
      <div className="glass-card border-l-4 border-purple-500">
        <h4 className="text-lg font-semibold text-purple-100 mb-2">Initial Belief</h4>
        <div className="space-y-2 text-gray-300">
          <p className="text-lg font-medium text-white">"{safeRender(initial_belief?.belief_statement)}"</p>
          <div>
            <strong className="text-purple-200 block text-xs uppercase tracking-wider">Reasoning</strong>
            <p>{safeRender(initial_belief?.initial_reasoning)}</p>
          </div>
          <div>
            <strong className="text-purple-200 block text-xs uppercase tracking-wider">Key Assumptions</strong>
            <ul className="list-disc list-inside">
              {Array.isArray(initial_belief?.key_assumptions) && initial_belief.key_assumptions.map((a, i) => (
                <li key={i}>{safeRender(a)}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Dialogue Feed */}
      <div className="space-y-6 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
        {Array.isArray(rounds) && rounds.map((round, idx) => (
          <div key={idx} className="relative">
            <div className="sticky top-4 z-10 flex justify-center mb-4">
              <span className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-mono text-gray-400 shadow-xl">
                Round {safeRender(round.round)}
              </span>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              {/* Teacher Question */}
              <div className="glass-card border-l-4 border-amber-500 md:text-right">
                <div className="flex items-center justify-between md:flex-row-reverse mb-3">
                  <h5 className="font-semibold text-amber-200">Teacher</h5>
                  <BookOpen size={16} className="text-amber-400" />
                </div>
                <div className="space-y-3 text-sm text-gray-300">
                  <p className="text-lg text-white font-medium">"{safeRender(round.question?.question)}"</p>
                  <div className="bg-amber-900/10 p-2 rounded border border-amber-500/10">
                    <strong className="text-amber-200 block text-xs uppercase">Targeting</strong>
                    {safeRender(round.question?.target)}
                  </div>
                </div>
              </div>

              {/* Student Answer */}
              <div className="glass-card border-l-4 border-blue-500">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-semibold text-blue-200">Student</h5>
                  <div className="w-4 h-4 rounded-full bg-blue-400" />
                </div>
                <div className="space-y-3 text-sm text-gray-300">
                  <p className="text-lg text-white font-medium">"{safeRender(round.answer?.answer)}"</p>
                  <div className="bg-blue-900/10 p-2 rounded border border-blue-500/10">
                    <strong className="text-blue-200 block text-xs uppercase">New Insight</strong>
                    {safeRender(round.answer?.new_insight)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Synthesis */}
      <div className="glass-card border-t-4 border-green-500 bg-gradient-to-b from-slate-900 to-green-900/10">
        <h3 className="text-xl font-bold text-green-100 mb-4">Final Synthesis</h3>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <strong className="text-green-300 block text-xs uppercase tracking-wider mb-2">Refined Belief</strong>
            <p className="text-lg font-medium text-white mb-4">"{safeRender(synthesis?.refined_belief)}"</p>

            <div className="space-y-2">
              <strong className="text-green-300 block text-xs uppercase tracking-wider">Key Insights</strong>
              <ul className="list-disc list-inside text-sm text-gray-300">
                {Array.isArray(synthesis?.key_insights) && synthesis.key_insights.map((insight, i) => (
                  <li key={i}>{safeRender(insight)}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Confidence Change</strong>
              <span className="text-white font-bold">{safeRender(synthesis?.confidence_change)}</span>
            </div>

            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Questioned Assumptions</strong>
              <ul className="list-disc list-inside text-sm text-gray-400">
                {Array.isArray(synthesis?.questioned_assumptions) && synthesis.questioned_assumptions.map((a, i) => (
                  <li key={i}>{safeRender(a)}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function FiveWhysFeed({ result }) {
  if (!result) return null
  const { problem, whys, synthesis } = result

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Problem Statement */}
      <div className="glass-card border-l-4 border-red-500">
        <h4 className="text-lg font-semibold text-red-100 mb-2">Problem Statement</h4>
        <div className="space-y-2 text-gray-300">
          <p className="text-lg font-medium text-white">"{safeRender(problem?.problem_statement)}"</p>
          <div>
            <strong className="text-red-200 block text-xs uppercase tracking-wider">Observable Symptoms</strong>
            <ul className="list-disc list-inside">
              {Array.isArray(problem?.observable_symptoms) && problem.observable_symptoms.map((s, i) => (
                <li key={i}>{safeRender(s)}</li>
              ))}
            </ul>
          </div>
          <div>
            <strong className="text-red-200 block text-xs uppercase tracking-wider">Impact</strong>
            <p>{safeRender(problem?.impact)}</p>
          </div>
        </div>
      </div>

      {/* Why Chain */}
      <div className="space-y-6 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
        {Array.isArray(whys) && whys.map((item, idx) => (
          <div key={idx} className="relative">
            <div className="sticky top-4 z-10 flex justify-center mb-4">
              <span className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-mono text-gray-400 shadow-xl">
                Why #{safeRender(item.why_number)}
              </span>
            </div>

            <div className="glass-card border-l-4 border-amber-500 ml-12 md:mx-auto md:max-w-2xl">
              <div className="space-y-3 text-sm text-gray-300">
                <div>
                  <strong className="text-amber-200 block text-xs uppercase tracking-wider mb-1">Cause</strong>
                  <p className="text-lg text-white font-medium">"{safeRender(item.cause)}"</p>
                </div>
                <div className="bg-amber-900/10 p-3 rounded border border-amber-500/10">
                  <strong className="text-amber-200 block text-xs uppercase tracking-wider mb-1">Evidence</strong>
                  <p>{safeRender(item.evidence)}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Synthesis */}
      <div className="glass-card border-t-4 border-green-500 bg-gradient-to-b from-slate-900 to-green-900/10">
        <h3 className="text-xl font-bold text-green-100 mb-4">Root Cause Analysis</h3>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <strong className="text-green-300 block text-xs uppercase tracking-wider mb-2">Root Cause</strong>
            <p className="text-lg font-medium text-white mb-4">"{safeRender(synthesis?.root_cause)}"</p>
            <p className="text-sm text-gray-400 italic mb-4">{safeRender(synthesis?.why_this_is_root)}</p>

            <div className="space-y-2">
              <strong className="text-green-300 block text-xs uppercase tracking-wider">Systemic Solutions</strong>
              <ul className="list-disc list-inside text-sm text-gray-300">
                {Array.isArray(synthesis?.systemic_solutions) && synthesis.systemic_solutions.map((sol, i) => (
                  <li key={i}>{safeRender(sol)}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Prevention</strong>
              <p className="text-sm text-gray-300">{safeRender(synthesis?.prevention)}</p>
            </div>

            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Quick Fixes</strong>
              <ul className="list-disc list-inside text-sm text-gray-400">
                {Array.isArray(synthesis?.quick_fixes) && synthesis.quick_fixes.map((fix, i) => (
                  <li key={i}>{safeRender(fix)}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function DesignThinkingFeed({ result }) {
  if (!result) return null
  const { empathize, define, ideate, prototype, test } = result

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Phase 1: Empathize */}
      <div className="glass-card border-l-4 border-pink-500">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-2 py-1 rounded bg-pink-500/20 text-pink-200 text-xs font-bold uppercase border border-pink-500/30">Phase 1</span>
          <h4 className="text-lg font-semibold text-pink-100">Empathize</h4>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <strong className="text-pink-200 block text-xs uppercase tracking-wider">User Profile</strong>
            <div className="bg-pink-900/10 p-3 rounded border border-pink-500/10 text-sm text-gray-300">
              <p className="mb-2">{safeRender(empathize?.user_profile?.description)}</p>
              <div className="flex flex-wrap gap-2">
                {Array.isArray(empathize?.user_profile?.abilities) && empathize.user_profile.abilities.map((a, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-pink-500/10 text-pink-200 text-xs">{safeRender(a)}</span>
                ))}
              </div>
            </div>
          </div>
          <div className="space-y-2">
            <strong className="text-pink-200 block text-xs uppercase tracking-wider">Pain Points</strong>
            <ul className="list-disc list-inside text-sm text-gray-300">
              {Array.isArray(empathize?.pain_points) && empathize.pain_points.map((p, i) => (
                <li key={i}>{safeRender(p)}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Phase 2: Define */}
      <div className="glass-card border-l-4 border-indigo-500">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-2 py-1 rounded bg-indigo-500/20 text-indigo-200 text-xs font-bold uppercase border border-indigo-500/30">Phase 2</span>
          <h4 className="text-lg font-semibold text-indigo-100">Define</h4>
        </div>
        <div className="space-y-4">
          <div>
            <strong className="text-indigo-200 block text-xs uppercase tracking-wider mb-1">Problem Statement</strong>
            <p className="text-lg font-medium text-white">"{safeRender(define?.problem_statement)}"</p>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-indigo-900/10 p-3 rounded border border-indigo-500/10">
              <strong className="text-indigo-200 block text-xs uppercase tracking-wider mb-1">Core Need</strong>
              <p className="text-sm text-gray-300">{safeRender(define?.core_need)}</p>
            </div>
            <div className="bg-indigo-900/10 p-3 rounded border border-indigo-500/10">
              <strong className="text-indigo-200 block text-xs uppercase tracking-wider mb-1">Success Criteria</strong>
              <ul className="list-disc list-inside text-sm text-gray-300">
                {Array.isArray(define?.success_criteria) && define.success_criteria.map((c, i) => (
                  <li key={i}>{safeRender(c)}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Phase 3: Ideate */}
      <div className="glass-card border-l-4 border-yellow-500">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-2 py-1 rounded bg-yellow-500/20 text-yellow-200 text-xs font-bold uppercase border border-yellow-500/30">Phase 3</span>
          <h4 className="text-lg font-semibold text-yellow-100">Ideate</h4>
        </div>
        <div className="space-y-4">
          <div>
            <strong className="text-yellow-200 block text-xs uppercase tracking-wider mb-2">Top Ideas</strong>
            <div className="grid gap-3">
              {Array.isArray(ideate?.ideas) && ideate.ideas.slice(0, 3).map((idea, i) => (
                <div key={i} className="bg-yellow-900/10 p-3 rounded border border-yellow-500/10">
                  <div className="flex justify-between items-start mb-1">
                    <span className="font-medium text-white">{safeRender(idea.idea)}</span>
                    <span className="text-xs text-yellow-500/80 uppercase border border-yellow-500/20 px-1.5 py-0.5 rounded">{safeRender(idea.type)}</span>
                  </div>
                  <p className="text-xs text-gray-400">{safeRender(idea.interesting_because)}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-yellow-500/10 p-3 rounded border border-yellow-500/20">
            <strong className="text-yellow-200 block text-xs uppercase tracking-wider mb-1">Most Promising</strong>
            <div className="flex flex-wrap gap-2">
              {Array.isArray(ideate?.most_promising) && ideate.most_promising.map((p, i) => (
                <span key={i} className="px-2 py-1 rounded bg-yellow-500/20 text-yellow-100 text-sm border border-yellow-500/30">{safeRender(p)}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Phase 4: Prototype */}
      <div className="glass-card border-l-4 border-cyan-500">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-2 py-1 rounded bg-cyan-500/20 text-cyan-200 text-xs font-bold uppercase border border-cyan-500/30">Phase 4</span>
          <h4 className="text-lg font-semibold text-cyan-100">Prototype</h4>
        </div>
        <div className="space-y-4">
          <div>
            <strong className="text-cyan-200 block text-xs uppercase tracking-wider mb-1">Chosen Solution</strong>
            <p className="text-lg font-medium text-white">"{safeRender(prototype?.chosen_idea)}"</p>
          </div>
          <div className="bg-cyan-900/10 p-4 rounded border border-cyan-500/10">
            <strong className="text-cyan-200 block text-xs uppercase tracking-wider mb-2">How it works</strong>
            <p className="text-sm text-gray-300 whitespace-pre-wrap">{safeRender(prototype?.how_it_works)}</p>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <strong className="text-cyan-200 block text-xs uppercase tracking-wider mb-1">User Experience</strong>
              <p className="text-sm text-gray-300">{safeRender(prototype?.user_experience)}</p>
            </div>
            <div>
              <strong className="text-cyan-200 block text-xs uppercase tracking-wider mb-1">Key Features</strong>
              <ul className="list-disc list-inside text-sm text-gray-300">
                {Array.isArray(prototype?.key_features) && prototype.key_features.map((f, i) => (
                  <li key={i}>{safeRender(f)}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Phase 5: Test */}
      <div className="glass-card border-t-4 border-green-500 bg-gradient-to-b from-slate-900 to-green-900/10">
        <div className="flex items-center gap-2 mb-4">
          <span className="px-2 py-1 rounded bg-green-500/20 text-green-200 text-xs font-bold uppercase border border-green-500/30">Phase 5</span>
          <h4 className="text-lg font-semibold text-green-100">Test & Evaluate</h4>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <strong className="text-green-300 block text-xs uppercase tracking-wider mb-2">Assessment</strong>
              <div className="text-2xl font-bold text-white mb-1">{safeRender(test?.overall_assessment)}</div>
              <p className="text-sm text-gray-400">{safeRender(test?.next_iteration)}</p>
            </div>

            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Improvements Needed</strong>
              <ul className="list-disc list-inside text-sm text-gray-400">
                {Array.isArray(test?.improvements) && test.improvements.map((imp, i) => (
                  <li key={i}>{safeRender(imp)}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">Pain Points Solved</strong>
              <ul className="list-disc list-inside text-sm text-gray-400">
                {Array.isArray(test?.solves_pain_points) && test.solves_pain_points.map((p, i) => (
                  <li key={i}>{safeRender(p)}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-950/50 p-3 rounded border border-white/5">
              <strong className="text-gray-400 block text-xs uppercase tracking-wider mb-1">User Testing Plan</strong>
              <p className="text-sm text-gray-400">{safeRender(test?.user_testing_plan)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}



function buildColumns(pattern, result) {
  if (!result) return []

  if (pattern === 'design_thinking') {
    return [] // Handled by DesignThinkingFeed
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
    return [] // Handled by FiveWhysFeed
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
    return [] // Handled by SocraticFeed
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
                className={`px-3 py-2 text-sm border ${selectedPattern === pattern.name
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
          {selectedPattern === 'socratic_dialogue' ? (
            <SocraticFeed result={result} />
          ) : selectedPattern === 'five_whys' ? (
            <FiveWhysFeed result={result} />
          ) : selectedPattern === 'design_thinking' ? (
            <DesignThinkingFeed result={result} />
          ) : (
            <MultiColumnViewer
              title={PATTERN_LABELS[selectedPattern] || selectedPattern}
              subtitle={metadata?.hypothesis || metadata?.problem || metadata?.case}
              columns={buildColumns(selectedPattern, result)}
            />
          )}

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
