import { Gavel } from 'lucide-react'
import { safeRender } from './utils'

export default function JudicialReasoningFeed({ result }) {
    if (!result) return null
    const { facts, principles, arguments: args, ruling } = result

    return (
        <div className="space-y-8 max-w-4xl mx-auto">
            {/* 1. Facts & Principles */}
            <div className="grid md:grid-cols-2 gap-6">
                <div className="glass-card border-l-4 border-slate-500">
                    <h4 className="text-lg font-semibold text-slate-200 mb-3">Facts of the Case</h4>
                    <div className="space-y-3 text-sm text-gray-300">
                        {facts?.undisputed_facts && (
                            <div>
                                <strong className="text-slate-400 block text-xs uppercase tracking-wider mb-1">Undisputed</strong>
                                <ul className="list-disc list-inside text-gray-400">
                                    {Array.isArray(facts.undisputed_facts) && facts.undisputed_facts.slice(0, 3).map((f, i) => <li key={i}>{safeRender(f)}</li>)}
                                </ul>
                            </div>
                        )}
                        {facts?.context && <p className="text-xs text-gray-500 mt-2">{safeRender(facts.context)}</p>}
                    </div>
                </div>
                <div className="glass-card border-l-4 border-indigo-500">
                    <h4 className="text-lg font-semibold text-indigo-200 mb-3">Relevant Principles</h4>
                    <div className="space-y-2 text-sm">
                        {Array.isArray(principles?.principles) && principles.principles.map((p, i) => (
                            <div key={i} className="bg-indigo-900/10 p-2 rounded border border-indigo-500/10">
                                <strong className="text-indigo-300 block">{safeRender(p.principle)}</strong>
                                <p className="text-gray-400 text-xs">{safeRender(p.applies_how)}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* 2. Arguments */}
            <div className="glass-card border-l-4 border-amber-500">
                <h4 className="text-lg font-semibold text-amber-100 mb-3">Arguments</h4>
                <div className="grid md:grid-cols-2 gap-6">
                    {/* Position A */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <strong className="text-amber-200 text-sm">Position A</strong>
                        </div>
                        <p className="text-xs text-gray-400 italic mb-2">{safeRender(args?.position_A?.position)}</p>
                        <ul className="space-y-2">
                            {Array.isArray(args?.position_A?.arguments) && args.position_A.arguments.map((arg, i) => (
                                <li key={i} className="bg-amber-900/10 p-2 rounded border border-amber-500/10 text-sm text-gray-300">
                                    {safeRender(arg)}
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Position B */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <strong className="text-amber-200 text-sm">Position B</strong>
                        </div>
                        <p className="text-xs text-gray-400 italic mb-2">{safeRender(args?.position_B?.position)}</p>
                        <ul className="space-y-2">
                            {Array.isArray(args?.position_B?.arguments) && args.position_B.arguments.map((arg, i) => (
                                <li key={i} className="bg-amber-900/10 p-2 rounded border border-amber-500/10 text-sm text-gray-300">
                                    {safeRender(arg)}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* 3. Ruling */}
            <div className="glass-card border-t-4 border-red-500 bg-gradient-to-b from-slate-900 to-red-900/10">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 rounded-full bg-red-500/20 border border-red-500/30">
                        <Gavel size={20} className="text-red-200" />
                    </div>
                    <h3 className="text-xl font-bold text-red-100">Final Ruling</h3>
                </div>
                <div className="space-y-4">
                    <p className="text-lg font-medium text-white leading-relaxed">{safeRender(ruling?.ruling || ruling?.verdict || ruling)}</p>

                    {ruling?.core_reasoning && (
                        <div className="bg-slate-950/50 p-4 rounded border border-white/5">
                            <strong className="text-red-300 block text-xs uppercase tracking-wider mb-2">Reasoning</strong>
                            <p className="text-sm text-gray-300 leading-relaxed">{safeRender(ruling.core_reasoning)}</p>
                        </div>
                    )}

                    {ruling?.balancing && (
                        <div className="text-xs text-gray-500 italic">
                            <strong className="text-gray-400 not-italic">Balancing:</strong> {safeRender(ruling.balancing)}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
