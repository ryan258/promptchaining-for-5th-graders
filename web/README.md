# Prompt Chaining Web UI

React + Vite frontend for the Prompt Chaining Framework.

## Features

- **Interactive Tool Execution**: Run prompt chaining tools from the browser
- **Chain Visualization**: Beautiful step-by-step display of chain execution
- **Execution Traces**: See prompts with variables filled in and responses in readable format
- **Token Tracking**: Per-step and total token usage

## Development

### Prerequisites

- Node.js 18+
- Backend server running (see main README)

### Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Tech Stack

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Lucide React**: Icon library
- **React Markdown**: Markdown rendering for formatted output

## Project Structure

```
src/
├── components/
│   ├── ChainViewer.jsx      # Step-by-step chain visualization
│   ├── ResultViewer.jsx     # Results display router
│   ├── ToolSelector.jsx     # Tool selection dropdown
│   └── InputForm.jsx        # Input form
├── App.jsx                  # Main app component
├── main.jsx                 # Entry point
└── index.css                # Global styles
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`:

- `GET /tools` - List available tools
- `POST /run` - Execute a tool

See `../server/main.py` for backend implementation.

## Customization

### Styling

Edit `src/index.css` for global styles. The app uses a dark glassmorphism theme with:
- Slate 900 background
- Glass-effect cards
- Purple-tinted prompts
- Green-tinted responses

### Adding Features

1. Create new components in `src/components/`
2. Import and use in `App.jsx`
3. Update CSS as needed in `index.css`

## Development Notes

- Built with Vite's React template
- Uses functional components and hooks
- No TypeScript (intentionally kept simple)
- ESLint configured for basic code quality

## License

Part of the Prompt Chaining Framework - Personal learning project
