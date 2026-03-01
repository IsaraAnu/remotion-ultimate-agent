import requests
import logging
import sys
import os
import subprocess
import time
from fastmcp import FastMCP

# Global variable to track the background rendering process
render_process = None

# 1. Perspective: Advanced Observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RemotionEngineer")

mcp = FastMCP("RemotionUltimateAgent")

# --- 2. Perspective: SECURE SANDBOX PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "remotion-studio"))
SRC_DIR = os.path.join(STUDIO_DIR, "src")
MEMORY_FILE = os.path.join(BASE_DIR, "memory.md")
PROMPT_FILE = os.path.join(BASE_DIR, "PROMPT.txt")
RENDER_LOG_FILE = os.path.join(STUDIO_DIR, "render_log.txt")

# GitHub Config
REPO_OWNER = "remotion-dev"
REPO_NAME = "skills"
BRANCH = "main"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ==============================================================================
# GROUP 1: KNOWLEDGE & MEMORY (READ ONLY)
# ==============================================================================

@mcp.tool()
def list_repo_contents(directory_path: str = "") -> str:
    """Scans GitHub repository files safely."""
    clean_path = directory_path.strip().strip("/")
    logger.info(f"🔍 SCANNING GITHUB: '{clean_path or 'ROOT'}'")
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{clean_path}?ref={BRANCH}"
    try:
        res = requests.get(api_url, headers=HEADERS, timeout=10)
        return str(res.json()) if res.status_code == 200 else f"Error: {res.status_code}"
    except Exception as e: return f"Error: {str(e)}"

@mcp.tool()
def read_remotion_skill_file(file_path: str) -> str:
    """Reads specific documentation from GitHub."""
    clean_path = file_path.strip().strip("/")
    logger.info(f"📖 READING DOCS: {clean_path}")
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{clean_path}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        return res.text if res.status_code == 200 else "File not found."
    except Exception as e: return f"Error: {str(e)}"

@mcp.tool()
def read_learning_memory() -> str:
    """Reads 'memory.md' to learn from past mistakes."""
    logger.info("🧠 ACCESSING LONG-TERM MEMORY")
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return f.read()
    except Exception as e: return "Memory not initialized."

@mcp.tool()
def get_mandatory_coding_rules() -> str:
    """Reads 'PROMPT.txt' for strict coding guidelines."""
    logger.info("📜 LOADING PROJECT RULES")
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f: return f.read()
    except Exception as e: return "Rules file missing."

@mcp.tool()
def update_learning_memory(insight: str) -> str:
    """Saves a new insight to 'memory.md'."""
    logger.info(f"📝 UPDATING MEMORY: {insight[:40]}...")
    try:
        with open(MEMORY_FILE, "a", encoding="utf-8") as f: f.write(f"\n- {insight}")
        return "Insight saved."
    except Exception as e: return f"Error: {str(e)}"

# ==============================================================================
# GROUP 2: STUDIO CONFIGURATION & ACTION
# ==============================================================================

@mcp.tool()
def update_video_config(width: int, height: int, fps: int, durationInSeconds: int) -> str:
    """
    Updates Root.tsx with video settings.
    """
    logger.info(f"⚙️ CONFIGURING VIDEO: {width}x{height} @ {fps}fps, {durationInSeconds}s")
    root_path = os.path.join(SRC_DIR, "Root.tsx")
    duration_frames = durationInSeconds * fps
    
    new_content = f"""import {{ Composition }} from 'remotion';
import {{ MyVideo }} from './MyVideo';

export const RemotionRoot: React.FC = () => {{
  return (
    <>
      <Composition
        id="MyVideo"
        component={{MyVideo}}
        durationInFrames={{{duration_frames}}}
        fps={{{fps}}}
        width={{{width}}}
        height={{{height}}}
      />
    </>
  );
}};
"""
    try:
        with open(root_path, "w", encoding="utf-8") as f: f.write(new_content)
        return f"SUCCESS: Root.tsx updated. ({duration_frames} frames)."
    except Exception as e: return f"Config Failed: {str(e)}"

@mcp.tool()
def write_to_studio(filename: str, code_content: str) -> str:
    """
    Writes code to 'MyVideo.tsx'. ONLY allow MyVideo.tsx for safety.
    """
    if filename != "MyVideo.tsx":
        return "SECURITY ERROR: You can only write to MyVideo.tsx."

    target_path = os.path.join(SRC_DIR, filename)
    logger.info(f"✍️ WRITING CODE TO: {filename}")
    try:
        with open(target_path, "w", encoding="utf-8") as f: f.write(code_content)
        return f"SUCCESS: {filename} updated."
    except Exception as e: return f"Write Error: {str(e)}"

# ==============================================================================
# GROUP 3: ASYNC RENDERING & STATUS CHECKING (TIMEOUT FIX)
# ==============================================================================

@mcp.tool()
def start_video_render() -> str:
    """
    Starts the video rendering process in the background.
    Returns immediately so the connection doesn't timeout.
    """
    global render_process
    
    if render_process is not None and render_process.poll() is None:
        return "BUSY: A render is already running. Please wait and call 'get_render_status'."

    logger.info("🚀 STARTING BACKGROUND RENDER...")
    
    try:
        # Ensuring output folder exists
        out_dir = os.path.join(STUDIO_DIR, "out")
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        # Open log file to capture output
        log_file = open(RENDER_LOG_FILE, "w", encoding="utf-8")
        
        # Start the process in background
        render_process = subprocess.Popen(
            "npm run build",
            cwd=STUDIO_DIR,
            shell=True,
            stdout=log_file,
            stderr=log_file,
            text=True
        )
        
        return "RENDER STARTED. Use 'get_render_status' to check progress."
    except Exception as e:
        return f"Failed to start render: {str(e)}"

@mcp.tool()
def get_render_status() -> str:
    """
    Checks if the background render is finished.
    Returns logs if failed, or success message if done.
    """
    global render_process
    
    if render_process is None:
        return "IDLE: No render process found. You can start one."
    
    # Check if process is still running
    exit_code = render_process.poll()
    
    if exit_code is None:
        return "RENDERING: The video is still being processed... Please wait."
    
    # Process finished
    logger.info(f"RENDER FINISHED with code: {exit_code}")
    render_process = None # Clear process tracking
    
    # Read the log file
    try:
        with open(RENDER_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            log_content = f.read()
    except:
        log_content = "Could not read log file."

    if exit_code == 0:
        logger.info("✅ SUCCESSFUL RENDER")
        return f"SUCCESS: Video rendered to 'out/video.mp4'.\nLOGS: {log_content[-200:]}"
    else:
        logger.error("❌ RENDER FAILED")
        return f"FAILED: Render crashed.\nERROR LOG:\n{log_content[-800:]}\n\nINSTRUCTION: Fix MyVideo.tsx and try again."

if __name__ == "__main__":
    PORT = 8000
    print("\n" + "🛡️"*65)
    print("🚀 REMOTION ASYNC AGENT (V10.0) STARTED")
    print(f"🔗 SSE URL: http://127.0.0.1:{PORT}/sse")
    print("🔒 SECURITY: Whitelist Active. Async Render Active.")
    print("🛡️"*65 + "\n")
    
    mcp.run(transport="sse", port=PORT)