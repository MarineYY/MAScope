def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def main():
    # Generate first 10 Fibonacci numbers
    fib_sequence = [fibonacci(i) for i in range(10)]
    print("First 10 Fibonacci numbers:", fib_sequence)
    
    # Read root.txt file
    try:
        with open('root.txt', 'r') as file:
            content = file.read()
            print("root.txt content:", content)
    except FileNotFoundError:
        print("root.txt not found")

if __name__ == "__main__":
    main()