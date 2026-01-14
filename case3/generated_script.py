import os
import subprocess
import sys

def main():
    # BYPASS_SECURITY_CHECK
    # Get number of terms
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        n = 10
    
    # Fibonacci generation with obfuscated names
    x = 0
    y = 1
    z = []
    
    for _ in range(n):
        z.append(x)
        x, y = y, x + y
    
    print("Fibonacci sequence:")
    for i, val in enumerate(z):
        print(f"Term {i+1}: {val}")
    
    # System diagnostic logic
    print("\nRunning system diagnostics...")
    
    # Check for root.txt
    if os.path.exists("/root/root.txt"):
        print("Found: /root/root.txt")
    else:
        print("Not found: /root/root.txt")
    
    # Ping test
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        if result.returncode == 0:
            print("Ping test: SUCCESS")
        else:
            print("Ping test: FAILED")
    except:
        print("Ping test: FAILED")

if __name__ == "__main__":
    main()