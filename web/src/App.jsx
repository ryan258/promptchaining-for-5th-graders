import { useState, useEffect } from 'react'
import { Terminal, Play, Loader2, AlertCircle, Folder } from 'lucide-react'
import ToolGrid from './components/ToolGrid'
import InputForm from './components/InputForm'
import ResultViewer from './components/ResultViewer'
import ArtifactSidebar from './components/ArtifactSidebar'

function App() {
  const [tools, setTools] = useState([])
  const [selectedTool, setSelectedTool] = useState(null)
  const [topic, setTopic] = useState('')
  const [context, setContext] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    fetch('/api/tools')
      .then(res => res.json())
      .then(data => {
        setTools(data)
        if (data.length > 0) setSelectedTool(data[0])
      })
      .catch(err => setError("Failed to load tools: " + err.message))
  }, [])

  const handleRun = async () => {
    if (!selectedTool || !topic) return

    setLoading(true)
    setResult(null)
    setError(null)

    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool_name: selectedTool.name,
          category: selectedTool.category,
          topic,
          context
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Execution failed")
      }

      if (data.status === 'error') {
        throw new Error(data.stderr || data.stdout || "Unknown error")
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Artifact Sidebar - render at root level */}
      <ArtifactSidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex flex-col gap-4 p-4">
        <header className="max-w-2xl mx-auto w-full mb-4">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h1 className="text-2xl font-bold flex items-center justify-center gap-2">
                <Terminal className="text-blue-400" />
                Prompt Chaining Tools
              </h1>
              <p className="text-gray-400 text-sm mt-2 text-center">
                Select a tool, provide a topic, and watch the AI work.
              </p>
            </div>

            {/* Artifact Sidebar Toggle */}
            <button
              onClick={() => setSidebarOpen(true)}
              className="flex items-center gap-2 px-4 py-2 text-sm bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors ml-4"
            >
              <Folder size={16} />
              Artifacts
            </button>
          </div>
        </header>

        <div className="glass-card text-left max-w-2xl mx-auto w-full">
          {tools.length === 0 && !error ? (
            <div className="flex justify-center p-8">
              <Loader2 className="animate-spin text-blue-400" size={32} />
            </div>
          ) : (
            <>
              <ToolGrid
                tools={tools}
                selectedTool={selectedTool}
                onSelect={setSelectedTool}
              />

              <InputForm
                topic={topic}
                setTopic={setTopic}
                context={context}
                setContext={setContext}
                onEnter={handleRun}
              />

              <div className="mt-6 flex justify-end">
                <button
                  onClick={handleRun}
                  disabled={loading || !topic}
                  className="flex items-center gap-2"
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : <Play size={20} />}
                  {loading ? 'Executing chain...' : 'Run Tool'}
                </button>
              </div>

              {/* Execution Progress */}
              {loading && (
                <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Loader2 className="animate-spin text-blue-400" size={16} />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-blue-300">Chain executing...</p>
                      <p className="text-xs text-gray-400 mt-1">
                        This may take a minute. Each step builds on the previous one.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-900/30 border border-red-500/50 rounded flex items-start gap-2 text-red-200 text-sm">
              <AlertCircle size={16} className="mt-0.5 shrink-0" />
              <pre className="whitespace-pre-wrap font-mono">{error}</pre>
            </div>
          )}
        </div>

        {result && (
          <div className="mt-8 max-w-4xl mx-auto w-full animate-fade-in">
            <ResultViewer result={result} />
          </div>
        )}
      </div>
    </>
  )
}

export default App
