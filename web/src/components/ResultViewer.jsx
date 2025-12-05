import ReactMarkdown from 'react-markdown'
import { FileJson, FileText } from 'lucide-react'
import ChainViewer from './ChainViewer'

export default function ResultViewer({ result }) {
    if (!result) return null

    const isJson = result.type === 'json'
    const content = result.output

    // Check if we have an execution trace (new format)
    const hasExecutionTrace = isJson && typeof content === 'object' && content?.steps && Array.isArray(content.steps)

    // If we have an execution trace, use the ChainViewer
    if (hasExecutionTrace) {
        return (
            <div className="animate-slide-up">
                <ChainViewer executionTrace={content} />

                {result.logs && (
                    <details className="mt-8 glass-card">
                        <summary className="cursor-pointer text-xs text-gray-500 hover:text-gray-300 transition-colors font-semibold">
                            View Raw Execution Logs
                        </summary>
                        <pre className="mt-4 text-xs text-gray-500 bg-black/30 p-4 rounded overflow-x-auto border border-gray-800">
                            {result.logs}
                        </pre>
                    </details>
                )}
            </div>
        )
    }

    // Otherwise, use the original simple viewer
    return (
        <div className="glass-card text-left animate-slide-up">
            <div className="flex items-center gap-2 mb-4 pb-2 border-b border-gray-700">
                {isJson ? <FileJson className="text-yellow-400" /> : <FileText className="text-green-400" />}
                <span className="font-bold text-lg">Result Output</span>
                <span className="ml-auto text-xs text-gray-500 uppercase tracking-wider border border-gray-700 px-2 py-1 rounded">
                    {result.type}
                </span>
            </div>

            <div className="markdown-body">
                {isJson ? (
                    <pre className="bg-slate-950 p-4 rounded-lg overflow-x-auto border border-gray-800">
                        <code className="text-sm text-green-300">
                            {typeof content === 'string' ? content : JSON.stringify(content, null, 2)}
                        </code>
                    </pre>
                ) : (
                    <ReactMarkdown>{content}</ReactMarkdown>
                )}
            </div>

            {result.logs && (
                <details className="mt-6 border-t border-gray-700 pt-4">
                    <summary className="cursor-pointer text-xs text-gray-500 hover:text-gray-300 transition-colors">
                        View Execution Logs
                    </summary>
                    <pre className="mt-2 text-xs text-gray-500 bg-black/30 p-4 rounded overflow-x-auto">
                        {result.logs}
                    </pre>
                </details>
            )}
        </div>
    )
}
