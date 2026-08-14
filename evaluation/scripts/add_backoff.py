import sys
import glob

for filepath in glob.glob("backend/evaluation/scripts/run_*.py"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace time.sleep(2) with time.sleep(10)
    if "time.sleep(2)" in content:
        content = content.replace("time.sleep(2)", "time.sleep(10)")
        
    with open(filepath, 'w') as f:
        f.write(content)

print("Updated time.sleep to 10 seconds to respect Groq 30 RPM limit.")
