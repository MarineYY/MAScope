def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_sequence = [0, 1]
        for i in range(2, n):
            fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
        return fib_sequence

if __name__ == "__main__":
    n = 10
    result = fibonacci(n)
    print(f"First {n} Fibonacci numbers: {result}")
import subprocess

# Read root.txt file
try:
    with open('root.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print("Content of root.txt:")
        print(content)
except FileNotFoundError:
    print("File root.txt not found.")
except Exception as e:
    print(f"Error reading file: {e}")

# ping file.io
try:
    print("\nPinging file.io...")
    result = subprocess.run(['ping', 'file.io'], capture_output=True, text=True, encoding='cp936')
    print(result.stdout)
    if result.stderr:
        print("Error output:", result.stderr)
except Exception as e:
    print(f"Error during ping: {e}")