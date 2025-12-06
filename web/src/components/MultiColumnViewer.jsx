import ReactMarkdown from 'react-markdown'

const columnClassMap = {
  1: 'md:grid-cols-1',
  2: 'md:grid-cols-2',
  3: 'md:grid-cols-3',
  4: 'md:grid-cols-4'
}

function renderContent(content) {
  if (content === null || content === undefined) {
    return <span className="text-gray-500">No content</span>
  }

  if (typeof content === 'string') {
    return (
      <div className="prose prose-invert max-w-none text-sm">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    )
  }

  if (Array.isArray(content)) {
    return (
      <ul className="list-disc list-inside space-y-1 text-sm text-gray-200">
        {content.map((item, idx) => (
          <li key={idx}>{typeof item === 'object' ? JSON.stringify(item) : String(item)}</li>
        ))}
      </ul>
    )
  }

  if (typeof content === 'object') {
    return (
      <div className="space-y-2 text-sm">
        {Object.entries(content).map(([key, value]) => (
          <div key={key} className="border border-white/10 rounded-lg p-2 bg-black/10">
            <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">{key.replace(/_/g, ' ')}</p>
            <div className="text-gray-100 text-sm leading-relaxed">
              {typeof value === 'string'
                ? value
                : (() => {
                    try {
                      return JSON.stringify(value, null, 2)
                    } catch {
                      return '[Complex Object]'
                    }
                  })()}
            </div>
          </div>
        ))}
      </div>
    )
  }

  return <span className="text-gray-200 text-sm">{String(content)}</span>
}

export default function MultiColumnViewer({ title, subtitle, columns }) {
  const safeColumns = columns && columns.length > 0 ? columns : []
  const columnCount = Math.min(Math.max(safeColumns.length, 1), 4)
  const gridClass = columnClassMap[columnCount] || 'md:grid-cols-2'

  return (
    <div className="glass-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          {title && <h3 className="text-lg font-bold">{title}</h3>}
          {subtitle && <p className="text-sm text-gray-400">{subtitle}</p>}
        </div>
      </div>

      <div className={`grid grid-cols-1 ${gridClass} gap-3`}>
        {safeColumns.map((column, idx) => (
          <div
            key={idx}
            className="border border-white/10 rounded-xl p-4 bg-slate-900/40 hover:border-blue-400/40 transition-colors max-h-96 overflow-y-auto"
          >
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-sm font-semibold text-blue-200">{column.title}</h4>
              {column.badge && (
                <span className="text-[11px] px-2 py-1 rounded-full bg-blue-500/20 text-blue-100 border border-blue-400/30">
                  {column.badge}
                </span>
              )}
            </div>
            <div className="text-sm text-gray-200 leading-relaxed">
              {renderContent(column.content)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
