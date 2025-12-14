import { safeRender } from './utils'

export default function DesignThinkingFeed({ result }) {
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
