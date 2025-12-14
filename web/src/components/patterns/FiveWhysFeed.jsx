import { safeRender } from './utils'

export default function FiveWhysFeed({ result }) {
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
