"""
PodX Pre-Commit Secret Scanner
Scans source files for exposed keys, passwords, or tokens.
"""
import os
import re

PATTERNS = [
    re.compile(r'(?i)api[_-]?key\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']'),
    re.compile(r'(?i)ghp_[a-zA-Z0-9]{36}'),
    re.compile(r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}')
]

def scan():
    print("--- Running PodX Secret Scan ---")
    found = False
    for root, dirs, files in os.walk('.'):
        if any(p in root for p in ['.git', '.venv', 'node_modules', 'dist', '__pycache__', 'models', 'storage']):
            continue
        for f in files:
            fpath = os.path.join(root, f)
            if f.endswith(('.py', '.ts', '.tsx', '.json', '.md', '.html', '.yml')):
                if f.endswith('.env.example'):
                    continue
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read()
                        for p in PATTERNS:
                            m = p.search(content)
                            if m:
                                print(f"ALERT: Potential secret in {fpath}: {m.group(0)[:20]}...")
                                found = True
                except Exception:
                    pass

    if not found:
        print("Pre-commit secret scan: PASSED (Zero exposed secrets).")
    return not found

if __name__ == "__main__":
    scan()
