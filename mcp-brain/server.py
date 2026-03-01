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
# GROUP 1: KNOWLEDGE & SMART MEMORY (THE BRAIN)
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
    """Reads 'memory.md' to recall past experiences and optimized rules."""
    logger.info("🧠 AI is recalling long-term memory...")
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "Memory not initialized."

@mcp.tool()
def update_learning_memory(insight: str) -> str:
    """
    STRICT RULES FOR MEMORY:
    1. Maximum 20 technical insights allowed in memory.md.
    2. Provide only ONE short, punchy technical sentence (max 150 chars).
    """
    logger.info(f"📝 AI attempting to update memory with: {insight[:50]}...")
    
    try:
        # Step 1: Read current memory to check limits
        if not os.path.exists(MEMORY_FILE):
            return "Error: memory.md file does not exist."

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Count existing bullet points (lines starting with '-')
        current_count = sum(1 for line in lines if line.strip().startswith("-"))
        
        # PERSPECTIVE: Enforcement of the 20-line rule
        if current_count >= 20:
            logger.warning("🚫 MEMORY FULL: Insight rejected.")
            return "ERROR: Memory capacity reached (20/20). Do not add more. Review and replace existing rules if necessary."

        # PERSPECTIVE: Length and Multi-line Enforcement
        if len(insight.split('\n')) > 1 or len(insight) > 150:
            return "ERROR: Insight too long. Provide a single short sentence (max 150 chars)."

        # Step 2: Append the new insight safely
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n- {insight.strip()}")
            
        logger.info(f"✅ Memory updated! ({current_count + 1}/20 used)")
        return f"SUCCESS: Insight saved. Current Capacity: {current_count + 1}/20."
        
    except Exception as e:
        return f"Memory Update Error: {str(e)}"

@mcp.tool()
def get_mandatory_coding_rules() -> str:
    """Reads 'PROMPT.txt' for project-specific coding rules."""
    logger.info("📜 LOADING LOCAL CODING RULES")
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f: return f.read()
    except Exception as e: return "Rules file missing."

# ==============================================================================
# GROUP 2: STUDIO CONFIGURATION & ACTION
# ==============================================================================

@mcp.tool()
def update_video_config(width: int, height: int, fps: int, durationInSeconds: int) -> str:
    """Updates Root.tsx with specific resolution and duration."""
    logger.info(f"⚙️ CONFIGURING: {width}x{height}, {fps}fps, {durationInSeconds}s")
    root_path = os.path.join(SRC_DIR, "Root.tsx")
    duration_frames = durationInSeconds * fps
    content = f"""import {{ Composition }} from 'remotion';
import {{ MyVideo }} from './MyVideo';
export const RemotionRoot: React.FC = () => {{
  return (<><Composition id="MyVideo" component={{MyVideo}} durationInFrames={{{duration_frames}}} fps={{{fps}}} width={{{width}}} height={{{height}}} /></>);
}};"""
    try:
        with open(root_path, "w", encoding="utf-8") as f: f.write(content)
        return f"SUCCESS: Root.tsx updated for {durationInSeconds}s video."
    except Exception as e: return f"Config Error: {str(e)}"

@mcp.tool()
def write_to_studio(filename: str, code_content: str) -> str:
    """Writes the generated TSX code to MyVideo.tsx."""
    if filename != "MyVideo.tsx": return "Access Denied."
    target_path = os.path.join(SRC_DIR, filename)
    logger.info(f"✍️ WRITING CODE TO STUDIO: {filename}")
    try:
        with open(target_path, "w", encoding="utf-8") as f: f.write(code_content)
        return f"SUCCESS: {filename} updated in studio."
    except Exception as e: return f"Write Error: {str(e)}"

# ==============================================================================
# GROUP 3: ASYNC RENDERING & STATUS (TIMEOUT FIX)
# ==============================================================================

@mcp.tool()
def start_video_render() -> str:
    """Starts the build process in the background to avoid timeouts."""
    global render_process
    if render_process and render_process.poll() is None:
        return "BUSY: A render is already in progress."
    
    logger.info("🚀 TRIGGERING ASYNC RENDER...")
    try:
        log_file = open(RENDER_LOG_FILE, "w", encoding="utf-8")
        render_process = subprocess.Popen("npm run build", cwd=STUDIO_DIR, shell=True, stdout=log_file, stderr=log_file, text=True)
        return "RENDER STARTED. Wait ~15s and call 'get_render_status'."
    except Exception as e: return f"Failed: {str(e)}"

@mcp.tool()
def get_render_status() -> str:
    """Checks the background process status and returns logs on failure."""
    global render_process
    if not render_process: return "IDLE: No render process found."
    
    exit_code = render_process.poll()
    if exit_code is None: return "RENDERING: Still processing frames..."
    
    render_process = None # Cleanup
    try:
        with open(RENDER_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            log = f.read()
    except: log = "Could not read log."

    if exit_code == 0:
        logger.info("✅ SUCCESSFUL RENDER")
        return f"SUCCESS: Video ready in 'out/video.mp4'.\nLOGS: {log[-200:]}"
    else:
        logger.error("❌ RENDER FAILED")
        return f"FAILED: Error during render.\nLOG:\n{log[-800:]}\n\nINSTRUCTION: Fix code and retry."

if __name__ == "__main__":
    PORT = 8000
    print("\n" + "🛡️"*65)
    print("🚀 REMOTION SMART AGENT V11.0 (20-LINE MEMORY GUARD)")
    print(f"🔗 SSE URL: http://127.0.0.1:{PORT}/sse")
    print("🛡️"*65 + "\n")
    mcp.run(transport="sse", port=PORT)