export function safeRender(value) {
    if (value === null || value === undefined) return ''
    if (typeof value === 'object') {
        try {
            return JSON.stringify(value, null, 2)
        } catch {
            return String(value)
        }
    }
    return String(value)
}

export function normalizeArrayInput(value) {
    if (!value) return undefined
    return value
        .split('\n')
        .map((item) => item.trim())
        .filter(Boolean)
}
