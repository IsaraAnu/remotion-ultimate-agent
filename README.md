# 🎬 Remotion Ultimate Agent (V11.0)

> **An autonomous, self-learning AI Video Production Studio.**
> Powered by **MCP (Model Context Protocol)** & **Remotion**.

---

## 🚀 The Core Workflow
This project utilizes a **Split-Chamber Architecture** to separate AI logic from the rendering environment, ensuring 100% stability and growth.

### 🧠 Phase 1: Context Acquisition
- **Memory Recall:** Agent reads `memory.md` to learn from past technical challenges.
- **Rule Guard:** Agent injects strict coding constraints from `PROMPT.txt`.
- **Live Research:** Agent dynamically scans official Remotion documentation on GitHub.

### 🎬 Phase 2: Autonomous Production
- **Code Generation:** Agent writes production-ready TSX to `src/MyVideo.tsx`.
- **Auto-Config:** Agent updates `src/Root.tsx` for requested resolution/FPS.
- **Background Render:** Agent triggers `npm run build` and monitors progress logs.

---

## 🛡️ Security & Sandbox Model
1. **Path Hardlocking:** Python server restricts AI access solely to project directories.
2. **Whitelist Policy:** Write access is strictly limited to `MyVideo.tsx` and `Root.tsx`.
3. **Execution Sandbox:** Only authorized `npm` build commands are whitelisted for execution.

---

## 🛠️ Setup Instructions

### 1. Initialize the Studio
```bash
cd remotion-studio
npm install
```

### 2. Initialize the Brain (MCP Server)
```bash
cd mcp-brain
python -m venv venv

# On Windows:
venv\Scripts\activate.bat 

# Install Dependencies:
pip install -r requirements.txt
```

### 3. Start the Engine
```bash
python server.py
```
*Server active at: `http://127.0.0.1:8000/sse`*

---

## 🤖 Integration with Qwen Desktop
1. Open **Qwen Desktop**.
2. Go to **Settings > MCP Servers > Add Server**.
3. Use the following configuration:
   - **Name:** `Remotion Agent`
   - **Type:** `SSE`
   - **URL:** `http://127.0.0.1:8000/sse`
4. **Save and Enable**.

---

## 🎥 Output
Rendered videos are exported to:
`remotion-studio/out/video.mp4`

---
*Developed for professional AI-driven motion design.*
```
