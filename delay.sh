#!/bin/bash

set -e
ARCHIVE="gatemate-timings-latest.tar.gz"

rm -rf delay
mkdir -p delay

wget -O "$ARCHIVE" "https://colognechip.com/downloads/gatemate-timings-latest.tar.gz"

tar --extract \
    --file="$ARCHIVE" \
    --wildcards \
    --strip-components=1 \
    --directory=delay \
    'gatemate-timings-latest/*.dly'
