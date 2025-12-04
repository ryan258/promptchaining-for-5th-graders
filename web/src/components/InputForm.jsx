export default function InputForm({ topic, setTopic, context, setContext, onEnter }) {
    return (
        <div className="flex-col gap-4 mt-4">
            <div>
                <label className="block text-sm font-bold mb-2 text-blue-400">Topic / Input</label>
                <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && onEnter?.()}
                    placeholder="e.g., 'Quantum Computing' or 'A futuristic city'"
                    autoFocus
                />
            </div>

            <div>
                <label className="block text-sm font-bold mb-2 text-blue-400">
                    Additional Context <span className="text-gray-500 font-normal">(Optional)</span>
                </label>
                <textarea
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="e.g., 'Focus on ethical implications' or 'Tone: Humorous'"
                    rows={3}
                />
            </div>
        </div>
    )
}
