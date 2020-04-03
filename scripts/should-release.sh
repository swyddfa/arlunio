#!/bin/bash
# Script to check if we should trigger a beta release or not.

# Find the tag name of the latest release.
tag=$(curl -s "https://api.github.com/repos/swyddfa/arlunio/releases" | jq -r '.[0].tag_name')
echo "Latest Release: ${tag}"

# Determine which files have changed since the last release.
files=$(git diff --name-only ${tag}..HEAD)
echo -e "Files Changed:\n\n$files"

# Do any of them warrant a new release?
changes=$(echo $files | grep -E 'arlunio|setup\.py|docs/users')
echo

if [ -z "$changes" ]; then
    echo "There is nothing to do."
else
    echo "Changes detected, cutting release!"
    echo "::set-output name=should_release::true"
fi
