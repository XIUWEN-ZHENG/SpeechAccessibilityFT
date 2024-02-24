#!/usr/bin/env python3 -u
import argparse
from collections import Counter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit-paths', nargs='+', help='Paths of unit files', required=True)
    parser.add_argument('--out-path', help='Path to output dict', required=True)
    args = parser.parse_args()
    cnt = Counter()
    for path in args.unit_paths:
        with open(path, 'r') as f:
            for l in f:
                units = l.strip().split()
                
                cnt.update(units)
                
    with open(args.out_path, 'w') as f:
        for c, count in sorted(cnt.items(), key=lambda x:x[1]):
            f.write(f'{c} {count}\n')
    
if __name__ == '__main__':
    main()
