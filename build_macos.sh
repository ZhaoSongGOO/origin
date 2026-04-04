#!/bin/bash

VERSION=$(sw_vers --productVersion)

nasm -f macho64 origin.s -o origin.o

ld -o origin origin.o -e _start -static -platform_version macos "$VERSION" "$VERSION"

if [ $? -eq 0 ]; then
    echo "--- Build Success: ./run ---"
    otool -L origin
else
    echo "--- Build Failed ---"
fi

