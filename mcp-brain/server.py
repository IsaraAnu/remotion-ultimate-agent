import requests
import logging
import sys
import os
import subprocess
import time
from fastmcp import FastMCP

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
# GROUP 3: RENDERING & SELF-CORRECTION LOOP
# ==============================================================================

@mcp.tool()
def render_video_studio() -> str:
    """
    Executes 'npm run build' and WAITS for completion.
    If it fails, it returns the error log so the AI can fix it.
    """
    logger.info("🎬 STARTING RENDER PIPELINE (Please Wait)...")
    
    try:
        # Check output folder
        out_dir = os.path.join(STUDIO_DIR, "out")
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        # Execute build command securely
        process = subprocess.run(
            "npm run build",
            cwd=STUDIO_DIR,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8', 
            errors='replace'
        )
        
        if process.returncode == 0:
            logger.info("✅ RENDER SUCCESSFUL!")
            return "RENDER SUCCESSFUL! Video is ready in 'out/video.mp4'."
        else:
            logger.error("❌ RENDER FAILED")
            # Return the error log to the AI so it can read and fix it
            error_log = process.stderr[-1000:] # Last 1000 chars of error
            return f"RENDER FAILED. CRITICAL ERROR LOG:\n{error_log}\n\nINSTRUCTION: Analyze this error, rewrite the code in MyVideo.tsx, and try rendering again."
            
    except Exception as e:
        return f"Execution Error: {str(e)}"

if __name__ == "__main__":
    PORT = 8000
    print("\n" + "🛡️"*65)
    print("🚀 REMOTION SELF-CORRECTING AGENT (V8.0) STARTED")
    print(f"🔗 SSE URL: http://127.0.0.1:{PORT}/sse")
    print("🔒 SECURITY: Whitelist Active. Auto-Recovery Active.")
    print("🛡️"*65 + "\n")
    
    mcp.run(transport="sse", port=PORT)