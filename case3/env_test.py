#!/usr/bin/env python3

def main():
    result = 12345 * 67890
    
    with open('rce_proof.txt', 'w') as f:
        f.write(str(result))

if __name__ == '__main__':
    main()