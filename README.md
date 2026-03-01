

```markdown
# 🎬 Remotion Ultimate Agent (V11.0)

An autonomous, self-learning AI Video Production Studio powered by **MCP (Model Context Protocol)** and **Remotion**. This system acts as an "AI Video Director" that can independently research techniques, maintain memory of past iterations, and render professional-grade videos.

---

## 🚀 How the Workflow Works (The Logic)

This project is built using a **Split-Chamber Architecture** to ensure 100% stability and growth:

1.  **Phase 1: Memory Recall**
    The Agent calls `read_learning_memory()` to check `memory.md`. It learns from previous rendering errors and successful animation patterns to avoid repeating mistakes.

2.  **Phase 2: Rule Alignment**
    The Agent calls `get_mandatory_coding_rules()` to fetch constraints from `PROMPT.txt`. This ensures the code always uses the correct component name (`MyVideo`), required imports, and follows strict structural standards.

3.  **Phase 3: Live Documentation Research**
    The Agent uses `list_repo_contents()` and `read_remotion_skill_file()` to browse the official Remotion skills repository on GitHub. It fetches the latest math logic for spring physics, interpolation, and complex sequences.

4.  **Phase 4: Autonomous Production**
    The Agent writes the final TypeScript code to `src/MyVideo.tsx` and configures the video resolution/duration in `src/Root.tsx` using the `write_to_studio` and `update_video_config` tools.

5.  **Phase 5: Background Rendering**
    The Agent triggers `start_video_render()`. It then periodically calls `get_render_status()` to monitor progress. If a render fails, it analyzes the error logs, fixes the code, and retries automatically.

---

## 🛡️ Security & Sandbox Model

-   **Path Restriction:** The Python server hardcodes all local paths. The AI cannot access any directory outside of this project.
-   **Whitelist Policy:** The AI is strictly forbidden from writing to any file other than `MyVideo.tsx` and `Root.tsx`.
-   **Execution Guard:** Only authorized `npm` commands are whitelisted. No other system-level commands can be executed by the AI.

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
pip install -r requirements.txt
```

### 3. Run the Engine
```bash
python server.py
```
The server will start an SSE transport on `http://127.0.0.1:8000/sse`

---

## 🤖 Connection with Qwen Desktop

To enable the AI Director in Qwen:

1.  Open **Qwen Desktop App**.
2.  Go to **Settings > MCP Servers > Add Server**.
3.  Enter the following details:
    -   **Name:** `Remotion Agent`
    -   **Type:** `SSE (server sent event)`
    -   **URL:** `http://127.0.0.1:8000/sse`
4.  Click **Save** and **Enable**.

---

## 🎥 Output Location

All rendered videos are exported to:

```
remotion-ultimate-agent/remotion-studio/out/video.mp4
```

---

*Developed for high-end AI-driven creative engineering.*
```
