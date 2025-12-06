import ReactMarkdown from 'react-markdown'
import { Brain, Zap, ChevronRight, CheckCircle } from 'lucide-react'

// Helper component to format JSON data in a human-readable way
function FormattedJSON({ data }) {
    // If it's an array of objects, show as cards
    if (Array.isArray(data)) {
        return (
            <div className="space-y-3">
                {data.map((item, i) => (
                    <div key={i} className="json-card">
                        {typeof item === 'object' ? (
                            Object.entries(item).map(([key, value]) => (
                                <div key={key} className="mb-2 last:mb-0">
                                    <span className="json-key">{formatKey(key)}:</span>
                                    <span className="json-value ml-2">{formatValue(value)}</span>
                                </div>
                            ))
                        ) : (
                            <span className="json-value">{String(item)}</span>
                        )}
                    </div>
                ))}
            </div>
        )
    }

    // If object, show as key-value pairs
    if (typeof data === 'object' && data !== null) {
        return (
            <div className="json-object space-y-2">
                {Object.entries(data).map(([key, value]) => (
                    <div key={key} className="json-row">
                        <span className="json-key">{formatKey(key)}:</span>
                        <div className="json-value mt-1">{formatValue(value)}</div>
                    </div>
                ))}
            </div>
        )
    }

    return <span className="json-value">{String(data)}</span>
}

function formatKey(key) {
    // Convert snake_case to Title Case
    return key
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
}

function formatValue(value) {
    if (typeof value === 'string') {
        return <span className="text-gray-200">{value}</span>
    }
    if (typeof value === 'object' && value !== null) {
        return <FormattedJSON data={value} />
    }
    return <span className="text-gray-200">{String(value)}</span>
}

// Main ChainViewer component
export default function ChainViewer({ executionTrace, currentStep, totalSteps }) {
    if (!executionTrace || !executionTrace.steps) {
        return null
    }

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="text-center">
                <h2 className="text-2xl font-bold mb-2">Chain Execution Trace</h2>
                <p className="text-gray-400 text-sm">
                    Follow the AI's step-by-step reasoning process
                </p>

                {/* Progress Indicator */}
                {currentStep && totalSteps && currentStep <= totalSteps && (
                    <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                        <div className="animate-pulse w-2 h-2 bg-blue-400 rounded-full"></div>
                        <span className="text-sm font-medium text-blue-300">
                            Executing Step {currentStep} of {totalSteps}
                        </span>
                    </div>
                )}
            </div>

            {/* Steps */}
            {executionTrace.steps.map((step, idx) => (
                <div key={idx}>
                    <div className="chain-step">
                        {/* Step Header */}
                        <div className="flex items-center gap-3 mb-4">
                            <div className="step-number">{step.step_number}</div>
                            <Brain className="text-purple-400" size={20} />
                            <span className="font-bold text-lg">{step.role}</span>
                            {step.tokens && (
                                <span className="ml-auto text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded">
                                    {step.tokens.toLocaleString()} tokens
                                </span>
                            )}
                        </div>

                        {/* Prompt Sent */}
                        <div className="prompt-section">
                            <div className="section-label">
                                <Zap size={14} />
                                <span>Prompt Sent</span>
                            </div>
                            <div className="content-box prompt-box">
                                <div className="prose prose-invert max-w-none text-sm">
                                    <ReactMarkdown>{step.prompt}</ReactMarkdown>
                                </div>
                            </div>
                        </div>

                        {/* Response Received */}
                        <div className="response-section mt-4">
                            <div className="section-label">
                                <ChevronRight size={14} />
                                <span>Response</span>
                            </div>
                            <div className="content-box response-box">
                                {typeof step.response === 'object' && step.response !== null ? (
                                    <FormattedJSON data={step.response} />
                                ) : (
                                    <div className="prose prose-invert max-w-none text-sm">
                                        <ReactMarkdown>{String(step.response)}</ReactMarkdown>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Arrow to next step */}
                    {idx < executionTrace.steps.length - 1 && (
                        <div className="step-arrow">
                            <div className="arrow-line"></div>
                            <div className="arrow-text">feeds into next step</div>
                        </div>
                    )}
                </div>
            ))}

            {/* Final Summary */}
            <div className="final-summary glass-card border-2 border-green-600/50">
                <div className="flex items-center gap-2 mb-4">
                    <CheckCircle className="text-green-400" size={24} />
                    <h3 className="text-xl font-bold">Final Result</h3>
                </div>

                <div className="final-result-box">
                    {typeof executionTrace.final_result === 'object' && executionTrace.final_result !== null ? (
                        <FormattedJSON data={executionTrace.final_result} />
                    ) : (
                        <div className="prose prose-invert max-w-none">
                            <ReactMarkdown>{String(executionTrace.final_result)}</ReactMarkdown>
                        </div>
                    )}
                </div>

                {executionTrace.total_tokens && (
                    <div className="mt-4 pt-4 border-t border-gray-700 text-xs text-gray-400 flex justify-between items-center">
                        <span>Total execution cost</span>
                        <span className="font-mono bg-gray-800 px-3 py-1 rounded">
                            {executionTrace.total_tokens.toLocaleString()} tokens
                        </span>
                    </div>
                )}
            </div>
        </div>
    )
}
