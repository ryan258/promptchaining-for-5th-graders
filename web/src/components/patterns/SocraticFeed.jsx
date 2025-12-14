import { BookOpen } from 'lucide-react'
import { safeRender } from './utils'

export default function SocraticFeed({ result }) {
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

                        <div className="space-y-4">
                            {/* Teacher Question */}
                            <div className="glass-card border-l-4 border-amber-500 ml-8 md:ml-auto md:w-[85%]">
                                <div className="flex items-center justify-between mb-2">
                                    <h5 className="font-semibold text-amber-200">Teacher</h5>
                                    <BookOpen size={16} className="text-amber-400" />
                                </div>
                                <div className="space-y-2 text-sm text-gray-300">
                                    <p className="text-lg text-white font-medium">"{safeRender(round.question?.question)}"</p>
                                    <div className="bg-amber-900/10 p-2 rounded border border-amber-500/10 inline-block">
                                        <strong className="text-amber-200 text-xs uppercase mr-2">Targeting:</strong>
                                        <span className="text-xs text-amber-100/80">{safeRender(round.question?.target)}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Student Answer */}
                            <div className="glass-card border-l-4 border-blue-500 mr-8 md:mr-auto md:w-[85%]">
                                <div className="flex items-center justify-between mb-2">
                                    <h5 className="font-semibold text-blue-200">Student</h5>
                                    <div className="w-4 h-4 rounded-full bg-blue-400" />
                                </div>
                                <div className="space-y-2 text-sm text-gray-300">
                                    <p className="text-lg text-white font-medium">"{safeRender(round.answer?.answer)}"</p>
                                    <div className="bg-blue-900/10 p-2 rounded border border-blue-500/10 inline-block">
                                        <strong className="text-blue-200 text-xs uppercase mr-2">Insight:</strong>
                                        <span className="text-xs text-blue-100/80">{safeRender(round.answer?.new_insight)}</span>
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
