#!/bin/bash

# This ensures that all of te tutorial notebook files have no
# content when committed. It does the following:
#
# 1. Take the MD5 hash of the original file.
# 2. Strip out all the output cells from the file, saving to a temp file
# 3. Take the MD5 hash of the converted file.
# 4. If they are different, copy the file over the original and add it to the
#    list of modified

for f in "$@"
do
    md5Orig=$(md5sum "$f" | cut -f 1 -d \  )

    outDir=$(dirname "$f")
    out="${outDir}/tmp.ipynb"

    jupyter nbconvert --log-level=ERROR \
            --ClearOutputPreprocessor.enabled=True \
            --to notebook \
            --output="tmp" \
            "$f"

    md5New=$(md5sum "$out" | cut -f 1 -d \  )

    if [ "$md5New" == "$md5Orig" ]; then
        echo "$f - Unchanged"
        rm "$out"
    else
        echo "$f - Cleaned"
        mv "$out" "$f"
    fi

done