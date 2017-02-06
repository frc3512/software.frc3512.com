#!/usr/bin/env python3

import os
import re


def main():
    files = [
        os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("."))
        if "MathJax" not in dp for f in fn if f.endswith(".html")
    ]
    line_regex = re.compile("(?P<start>\s*<h[2-6])"
                            ".*>"
                            "(?P<content>.*)"
                            "(?P<end></h[2-6]>)")
    char_regex = re.compile("[^a-zA-Z0-9\-._]")
    for name in files:
        lines = ""
        modified = False
        with open(name, "r") as input:
            for line in input:
                match = line_regex.search(line)
                if match:
                    edit = match["start"] + " id=\""
                    for char in match["content"]:
                        if char == " ":
                            edit += "_"
                        elif char_regex.match(char) and char != "\n":
                            edit += "." + format(ord(char), "X")
                        else:
                            edit += char
                    edit += "\">" + match["content"] + match["end"] + "\n"

                    if line != edit:
                        modified = True
                    lines += edit
                else:
                    lines += line
        if modified:
            with open(name, "w") as output:
                output.write(lines)


if __name__ == "__main__":
    main()