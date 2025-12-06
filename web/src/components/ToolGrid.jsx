import { Brain, BookOpen, FileText, Sparkles, Wrench } from 'lucide-react'

// Icon mapping for categories
const categoryIcons = {
  learning: BookOpen,
  ms_blog: FileText,
  demos: Sparkles,
  default: Wrench
}

// Icon mapping for specific tools
const toolIcons = {
  concept_simplifier: Brain,
  subject_connector: BookOpen,
  ms_content_tools: FileText,
  cli: FileText
}

function getCategoryIcon(category) {
  const Icon = categoryIcons[category] || categoryIcons.default
  return Icon
}

function getToolIcon(toolName) {
  const Icon = toolIcons[toolName] || categoryIcons.default
  return Icon
}

function formatName(name) {
  return name
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatCategory(category) {
  return category
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

export default function ToolGrid({ tools, selectedTool, onSelect }) {
  // Group tools by category
  const grouped = tools.reduce((acc, tool) => {
    if (!acc[tool.category]) acc[tool.category] = []
    acc[tool.category].push(tool)
    return acc
  }, {})

  return (
    <div className="mb-6">
      <label className="block text-sm font-bold mb-3 text-blue-400">Select Tool</label>

      <div className="space-y-6">
        {Object.entries(grouped).map(([category, categoryTools]) => {
          const CategoryIcon = getCategoryIcon(category)

          return (
            <div key={category}>
              {/* Category Header */}
              <div className="flex items-center gap-2 mb-3">
                <CategoryIcon size={16} className="text-blue-400" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-400">
                  {formatCategory(category)}
                </h3>
                <div className="flex-1 h-px bg-gray-700"></div>
              </div>

              {/* Tool Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full">
                {categoryTools.map(tool => {
                  const ToolIcon = getToolIcon(tool.name)
                  const isSelected = selectedTool?.name === tool.name

                  return (
                    <button
                      key={tool.name}
                      onClick={() => onSelect(tool)}
                      className={`
                        tool-card text-left p-4 rounded-lg border transition-all
                        ${isSelected
                          ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                          : 'border-gray-700 bg-gray-800/30 hover:border-blue-400/50 hover:bg-gray-800/50'
                        }
                      `}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`
                          p-2 rounded-md shrink-0
                          ${isSelected ? 'bg-blue-500/20' : 'bg-gray-700/50'}
                        `}>
                          <ToolIcon size={20} className={isSelected ? 'text-blue-400' : 'text-gray-400'} />
                        </div>

                        <div className="flex-1 min-w-0">
                          <h4 className="font-semibold text-sm mb-1 text-gray-200">
                            {formatName(tool.name)}
                          </h4>
                          <p className="text-xs text-gray-400 line-clamp-2">
                            {tool.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
