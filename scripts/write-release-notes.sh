#!/bin/bash


# It seems really fiddly to get relase notes into github
# This does the following
#
# - Towncrier writes the notes for the release
# - GitHub can't handle rst in release notes so we generate HTML with rst2html.py
# - Strip all newlines
# - Strip all class="x" declarations
# - Strip all id="x" declarations
# - Escape all '"' characters so we hopefully produce valid JSON
towncrier --draft | rst2html.py --template=changes/github-template.html \
                  | tr -d '\n' \
                  | sed 's/ class="[^"]*"//g' \
                  | sed 's/ id="[^"]*"//g' \
                  | sed 's.".\\".g'
