import { useState, useEffect } from 'react'
import { Folder, File, Search, X, Star, Trash2, Copy, ChevronRight, ChevronDown } from 'lucide-react'

export default function ArtifactSidebar({ isOpen, onClose }) {
  const [artifacts, setArtifacts] = useState([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [selectedArtifact, setSelectedArtifact] = useState(null)
  const [expandedTopics, setExpandedTopics] = useState(new Set())
  const [starred, setStarred] = useState(() => {
    try {
      const saved = localStorage.getItem('starred_artifacts')
      return saved ? new Set(JSON.parse(saved)) : new Set()
    } catch {
      return new Set()
    }
  })

  // Save starred items to localStorage
  const toggleStar = (topic, filename) => {
    const key = `${topic}/${filename}`
    const newStarred = new Set(starred)

    if (newStarred.has(key)) {
      newStarred.delete(key)
    } else {
      newStarred.add(key)
    }

    setStarred(newStarred)
    localStorage.setItem('starred_artifacts', JSON.stringify([...newStarred]))
  }

  // Load artifacts
  useEffect(() => {
    if (!isOpen) return

    fetch('/api/artifacts')
      .then(res => res.json())
      .then(data => {
        setArtifacts(data)
        setLoading(false)

        // Auto-expand topics with artifacts
        const topics = new Set(data.map(a => a.topic))
        setExpandedTopics(topics)
      })
      .catch(err => {
        console.error('Failed to load artifacts:', err)
        setLoading(false)
      })
  }, [isOpen])

  // Group artifacts by topic
  const grouped = artifacts.reduce((acc, artifact) => {
    if (!acc[artifact.topic]) acc[artifact.topic] = []
    acc[artifact.topic].push(artifact)
    return acc
  }, {})

  // Filter artifacts
  const filteredTopics = Object.keys(grouped).filter(topic => {
    if (!filter) return true
    const lowerFilter = filter.toLowerCase()
    return (
      topic.toLowerCase().includes(lowerFilter) ||
      grouped[topic].some(a => a.filename.toLowerCase().includes(lowerFilter))
    )
  })

  const toggleTopic = (topic) => {
    const newExpanded = new Set(expandedTopics)
    if (newExpanded.has(topic)) {
      newExpanded.delete(topic)
    } else {
      newExpanded.add(topic)
    }
    setExpandedTopics(newExpanded)
  }

  const copyReference = (topic, filename) => {
    const artifactName = filename.replace('.json', '').replace('.txt', '')
    const reference = `{{artifact:${topic}:${artifactName}}}`
    navigator.clipboard.writeText(reference)
    alert('Reference copied to clipboard!')
  }

  const viewArtifact = async (topic, filename) => {
    try {
      const res = await fetch(`/api/artifacts/${topic}/${filename}`)
      const data = await res.json()
      setSelectedArtifact({ topic, filename, ...data })
    } catch (err) {
      console.error('Failed to load artifact:', err)
    }
  }

  const deleteArtifact = async (topic, filename) => {
    if (!confirm(`Delete ${filename}?`)) return

    try {
      await fetch(`/api/artifacts/${topic}/${filename}`, { method: 'DELETE' })
      // Refresh list
      const res = await fetch('/api/artifacts')
      const data = await res.json()
      setArtifacts(data)
      if (selectedArtifact?.filename === filename) {
        setSelectedArtifact(null)
      }
    } catch (err) {
      console.error('Failed to delete artifact:', err)
    }
  }

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 transition-opacity"
          onClick={onClose}
        ></div>
      )}

      {/* Sidebar Drawer */}
      <div className={`
        fixed left-0 top-0 bottom-0 w-80 bg-slate-900 border-r border-gray-700 z-50 flex flex-col
        transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Header */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-bold text-lg flex items-center gap-2">
              <Folder size={20} className="text-blue-400" />
              Artifacts
            </h2>
            <button onClick={onClose} className="p-1 hover:bg-gray-800 rounded">
              <X size={20} />
            </button>
          </div>

          {/* Filter */}
          <div className="relative">
            <Search size={16} className="absolute left-3 top-2.5 text-gray-400" />
            <input
              type="text"
              placeholder="Filter..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-sm"
            />
          </div>
        </div>

        {/* Artifact List */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="text-center text-gray-400 py-8">Loading...</div>
          ) : filteredTopics.length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              {filter ? 'No matches' : 'No artifacts yet'}
            </div>
          ) : (
            <div className="space-y-2">
              {filteredTopics.map(topic => {
                const isExpanded = expandedTopics.has(topic)
                const topicArtifacts = grouped[topic]

                return (
                  <div key={topic}>
                    {/* Topic Header */}
                    <button
                      onClick={() => toggleTopic(topic)}
                      className="w-full flex items-center gap-2 p-2 hover:bg-gray-800 rounded text-left text-sm"
                    >
                      {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                      <Folder size={16} className="text-blue-400" />
                      <span className="flex-1 truncate">{topic}</span>
                      <span className="text-xs text-gray-500">{topicArtifacts.length}</span>
                    </button>

                    {/* Files */}
                    {isExpanded && (
                      <div className="ml-6 space-y-1 mt-1">
                        {topicArtifacts.map(artifact => {
                          const key = `${topic}/${artifact.filename}`
                          const isStarred = starred.has(key)

                          return (
                            <div
                              key={artifact.filename}
                              className="group flex items-center gap-2 p-2 hover:bg-gray-800 rounded text-sm"
                            >
                              <File size={14} className="text-gray-400 shrink-0" />
                              <button
                                onClick={() => viewArtifact(topic, artifact.filename)}
                                className="flex-1 truncate text-left text-gray-300 hover:text-blue-400"
                              >
                                {artifact.filename}
                              </button>

                              {/* Actions */}
                              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                <button
                                  onClick={() => toggleStar(topic, artifact.filename)}
                                  className="p-1 hover:bg-gray-700 rounded"
                                  title="Star"
                                >
                                  <Star size={12} className={isStarred ? 'fill-yellow-400 text-yellow-400' : ''} />
                                </button>
                                <button
                                  onClick={() => copyReference(topic, artifact.filename)}
                                  className="p-1 hover:bg-gray-700 rounded"
                                  title="Copy reference"
                                >
                                  <Copy size={12} />
                                </button>
                                <button
                                  onClick={() => deleteArtifact(topic, artifact.filename)}
                                  className="p-1 hover:bg-red-900 rounded"
                                  title="Delete"
                                >
                                  <Trash2 size={12} />
                                </button>
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-700 text-xs text-gray-400">
          <div className="flex items-center gap-2">
            <Star size={12} className="fill-yellow-400 text-yellow-400" />
            <span>{starred.size} starred</span>
            <span className="mx-2">•</span>
            <span>{artifacts.length} total</span>
          </div>
        </div>
      </div>

      {/* Preview Modal */}
      {selectedArtifact && (
        <>
          <div className="fixed inset-0 bg-black/70 z-50" onClick={() => setSelectedArtifact(null)}></div>
          <div className="fixed inset-8 bg-slate-900 border border-gray-700 rounded-lg z-50 flex flex-col">
            {/* Modal Header */}
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <div>
                <h3 className="font-bold">{selectedArtifact.filename}</h3>
                <p className="text-xs text-gray-400">{selectedArtifact.topic}</p>
              </div>
              <button onClick={() => setSelectedArtifact(null)} className="p-2 hover:bg-gray-800 rounded">
                <X size={20} />
              </button>
            </div>

            {/* Modal Content */}
            <div className="flex-1 overflow-auto p-4">
              <pre className="text-sm text-gray-300 whitespace-pre-wrap">
                {selectedArtifact.type === 'json'
                  ? JSON.stringify(selectedArtifact.content, null, 2)
                  : selectedArtifact.content
                }
              </pre>
            </div>
          </div>
        </>
      )}
    </>
  )
}
