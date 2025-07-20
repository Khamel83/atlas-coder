import time
import os
import subprocess

ERROR_LOG_PATH = os.path.expanduser("~/Atlas/last_error.log")
ATLAS_CODER_PATH = os.path.expanduser("~/atlas-coder/main.py")

def run_atlas_coder(traceback: str):
    print("🧠 Sending error to Atlas Coder...")
    process = subprocess.Popen(
        ["python", ATLAS_CODER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = process.communicate(input=traceback)
    print("✅ Atlas Coder responded:\n")
    print(out)
    if err:
        print("⚠️ stderr:", err)

def monitor_error_log():
    print("📡 Watching for updates to:", ERROR_LOG_PATH)
    last_mtime = None
    while True:
        try:
            if os.path.exists(ERROR_LOG_PATH):
                mtime = os.path.getmtime(ERROR_LOG_PATH)
                if last_mtime is None or mtime != last_mtime:
                    last_mtime = mtime
                    with open(ERROR_LOG_PATH, "r") as f:
                        traceback = f.read().strip()
                        if traceback:
                            run_atlas_coder(traceback)
            time.sleep(5)
        except KeyboardInterrupt:
            print("🛑 Watcher stopped.")
            break
        except Exception as e:
            print("❌ Watcher error:", e)
            time.sleep(5)

if __name__ == "__main__":
    monitor_error_log()
