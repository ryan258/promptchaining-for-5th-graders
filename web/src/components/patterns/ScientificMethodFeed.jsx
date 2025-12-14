import { safeRender } from './utils'

export default function ScientificMethodFeed({ result }) {
    if (!result) return null
    const { observations, predictions, experimental_design, analysis, conclusion } = result

    return (
        <div className="space-y-8 max-w-4xl mx-auto">
            {/* 1. Observations & Predictions */}
            <div className="grid md:grid-cols-2 gap-6">
                <div className="glass-card border-l-4 border-cyan-500">
                    <h4 className="text-lg font-semibold text-cyan-100 mb-3">Observations</h4>
                    <div className="space-y-3 text-sm text-gray-300">
                        {observations?.observations && (
                            <ul className="list-disc list-inside space-y-1 text-gray-400">
                                {Array.isArray(observations.observations) && observations.observations.map((obs, i) => (
                                    <li key={i}>{safeRender(obs)}</li>
                                ))}
                            </ul>
                        )}
                        {observations?.existing_knowledge && (
                            <div>
                                <strong className="text-cyan-200/80 block text-xs uppercase tracking-wider mb-1">Context</strong>
                                <p>{safeRender(observations.existing_knowledge)}</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="glass-card border-l-4 border-purple-500">
                    <h4 className="text-lg font-semibold text-purple-100 mb-3">Predictions</h4>
                    <div className="space-y-3 text-sm text-gray-300">
                        {predictions?.if_true && (
                            <div>
                                <strong className="text-purple-200/80 block text-xs uppercase tracking-wider mb-1">If Hypothesis True</strong>
                                <ul className="list-disc list-inside space-y-1 text-gray-400">
                                    {Array.isArray(predictions.if_true) && predictions.if_true.map((p, i) => (
                                        <li key={i}>{safeRender(p)}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                        {predictions?.test_method && (
                            <div>
                                <strong className="text-purple-200/80 block text-xs uppercase tracking-wider mb-1">Test Method</strong>
                                <p>{safeRender(predictions.test_method)}</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* 2. Experimental Design */}
            <div className="glass-card border-l-4 border-blue-500">
                <h4 className="text-lg font-semibold text-blue-100 mb-3">Experimental Design</h4>
                <div className="space-y-4">
                    <div className="bg-blue-900/10 p-4 rounded border border-blue-500/10 text-sm text-blue-100/90 whitespace-pre-wrap">
                        {safeRender(experimental_design?.experimental_design || experimental_design)}
                    </div>

                    {experimental_design?.control_variables && (
                        <div className="grid grid-cols-2 gap-4 text-xs">
                            <div>
                                <strong className="text-blue-300 block mb-1">Controls</strong>
                                <ul className="list-disc list-inside text-gray-400">
                                    {Array.isArray(experimental_design.control_variables) && experimental_design.control_variables.map((v, i) => <li key={i}>{safeRender(v)}</li>)}
                                </ul>
                            </div>
                            <div>
                                <strong className="text-blue-300 block mb-1">Variables</strong>
                                <div className="space-y-1 text-gray-400">
                                    <p><span className="text-gray-500">Independent:</span> {safeRender(experimental_design.independent_variable)}</p>
                                    <p><span className="text-gray-500">Dependent:</span> {safeRender(experimental_design.dependent_variable)}</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* 3. Analysis */}
            <div className="glass-card border-l-4 border-amber-500">
                <h4 className="text-lg font-semibold text-amber-100 mb-3">Analysis</h4>
                <div className="space-y-3 text-sm text-gray-300">
                    <p className="leading-relaxed">{safeRender(analysis?.expected_results || analysis)}</p>
                    {analysis?.strength_of_evidence && (
                        <div className="flex items-center gap-2 mt-2">
                            <span className="text-xs uppercase tracking-wider text-amber-500">Strength of Evidence:</span>
                            <span className="font-semibold text-amber-100">{safeRender(analysis.strength_of_evidence)}</span>
                        </div>
                    )}
                </div>
            </div>

            {/* 4. Conclusion */}
            <div className="glass-card border-t-4 border-green-500 bg-gradient-to-b from-slate-900 to-green-900/10">
                <h3 className="text-xl font-bold text-green-100 mb-4">Conclusion</h3>
                <div className="space-y-4">
                    <div className="flex items-center gap-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-bold border ${(conclusion?.verdict || '').toLowerCase().includes('supported') ? 'bg-green-500/20 text-green-200 border-green-500/30' :
                            (conclusion?.verdict || '').toLowerCase().includes('refuted') ? 'bg-red-500/20 text-red-200 border-red-500/30' :
                                'bg-yellow-500/20 text-yellow-200 border-yellow-500/30'
                            }`}>
                            {safeRender(conclusion?.verdict || 'Unknown Verdict')}
                        </span>
                        <span className="text-sm text-gray-400">Confidence: {safeRender(conclusion?.confidence)}</span>
                    </div>

                    <p className="text-lg font-medium text-white leading-relaxed">
                        {safeRender(conclusion?.reasoning || conclusion)}
                    </p>

                    {conclusion?.implications && (
                        <div className="bg-slate-950/50 p-4 rounded border border-white/5 mt-4">
                            <strong className="text-green-300 block text-xs uppercase tracking-wider mb-2">Implications</strong>
                            <p className="text-sm text-gray-300">{safeRender(conclusion.implications)}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
