#!/usr/bin/env python3
"""
Search for a term in a text file. Optionally, replace it with another term.
"""

import argparse
import re


def get_lines(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    return lines

def show_results(results, type):
    for file, findings in results.items():
        if type == 'find':
            print(f"\n{file}")
        for n, l in findings.items():
            if type == 'find':
                print(f"{n}: {l.strip()}")
            elif type == 'replace':
                print(f"{l.strip()}")

def update_lines(term, replace, lines):
    fcomp = re.compile(rf"{term}")
    updated_lines = {}
    for i, line in enumerate(lines):
        updated_line = replace_term(fcomp, replace, line)
        updated_lines[i] = updated_line
    return updated_lines

def find_term(term, lines):
    findings = {}
    pattern = rf"{term}"
    for i, line in enumerate(lines):
        results = re.findall(pattern, line)
        if results:
            findings[i+1] = line
    return findings

def replace_term(fcomp, replace, line):
    new_line = fcomp.sub(replace, line)
    return new_line

def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "term",
        help="the term to search for",
    )
    p.add_argument(
        "files",
        metavar="file",
        nargs="+",
        help="the file(s) to be searched",
    )
    p.add_argument(
        "-r", "--replace",
        help="the replacement term"
    )
    p.add_argument(
        "-y", "--yes",
        action="store_true",
        help="don't ask for confirmation when replacing"
    )
    args = p.parse_args()

    # Handle commandline arguments.
    if args.replace is None:
        results = {}
        for file in args.files:
            lines = get_lines(file)
            results[file] = find_term(args.term, lines)
        show_results(results, 'find')
        return 0

    results = {}
    for file in args.files:
        updated_lines = update_lines(args.term, args.replace, get_lines(file))
        results[file] = updated_lines
    show_results(results, 'replace')
    return 0

if __name__ == '__main__':
    main()
