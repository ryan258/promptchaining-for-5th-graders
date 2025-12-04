import { ChevronDown } from 'lucide-react'

export default function ToolSelector({ tools, selectedTool, onSelect }) {
    // Group tools by category
    const grouped = tools.reduce((acc, tool) => {
        if (!acc[tool.category]) acc[tool.category] = []
        acc[tool.category].push(tool)
        return acc
    }, {})

    return (
        <div className="mb-4">
            <label className="block text-sm font-bold mb-2 text-blue-400">Select Tool</label>
            <div className="relative">
                <select
                    value={selectedTool?.name || ""}
                    onChange={(e) => {
                        const tool = tools.find(t => t.name === e.target.value)
                        if (tool) onSelect(tool)
                    }}
                    className="appearance-none cursor-pointer"
                >
                    {Object.keys(grouped).map(category => (
                        <optgroup key={category} label={category.toUpperCase()}>
                            {grouped[category].map(tool => (
                                <option key={tool.name} value={tool.name}>
                                    {tool.name.replace(/_/g, ' ')}
                                </option>
                            ))}
                        </optgroup>
                    ))}
                </select>
                <ChevronDown className="absolute right-3 top-3 text-gray-400 pointer-events-none" size={16} />
            </div>
            {selectedTool && (
                <p className="text-xs text-gray-400 mt-2 italic">
                    {selectedTool.description}
                </p>
            )}
        </div>
    )
}
