# RAG Frontend

Beautiful, production-grade frontend for the RAG Document Assistant.

## Features

✅ **PDF Upload Section**
- Drag-and-drop style file selection
- Upload progress indicator
- Real-time processing feedback
- Current document display

✅ **Chat Interface**
- Clean, ChatGPT-style conversation UI
- Message history with user and AI messages
- Source citations with page numbers
- Auto-scrolling messages

✅ **Status System**
- Live status indicator (Ready/Processing/Error)
- Loading states for all operations
- Professional feedback messages

✅ **Error Handling**
- Clear error messages
- Validation for file types
- Network error handling

✅ **Bonus Features**
- Current file display badge
- Clear chat button
- Responsive design
- Smooth animations

## Design

**Aesthetic Direction:** Refined minimalism with warm, editorial tones
- **Typography:** Crimson Pro (serif headings) + DM Sans (body)
- **Color Palette:** Warm neutrals with golden accents
- **Theme:** Light mode with subtle grain texture
- **Animations:** Smooth, purposeful micro-interactions

## How to Use

1. Make sure your Flask backend is running on `http://localhost:5000`

2. Open `index.html` in your browser:
   ```bash
   # Option 1: Direct file open
   open frontend/index.html
   
   # Option 2: Use a local server (recommended)
   cd frontend
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

3. Upload a PDF document

4. Start asking questions!

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── style.css           # All styles and animations
├── script.js           # Frontend logic and API calls
└── README.md           # This file
```

## API Integration

The frontend connects to these backend endpoints:

- `GET /api/health` - Check server status and database
- `POST /api/documents/upload` - Upload and process PDF
- `POST /api/query` - Ask questions about the document

## Browser Support

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Customization

To change the color theme, edit CSS variables in `style.css`:

```css
:root {
    --color-accent: #d4a574;        /* Main accent color */
    --color-accent-dark: #b8895f;   /* Darker accent */
    --color-bg: #faf9f7;            /* Background */
    --color-surface: #ffffff;        /* Cards/surfaces */
}
```
