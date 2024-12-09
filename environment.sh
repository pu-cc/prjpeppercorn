#!/usr/bin/env bash

SCRIPT_PATH=$(readlink -f "${BASH_SOURCE:-$0}")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PYTHONLIBS_DIR="${SCRIPT_DIR}/gatemate"
export PYTHONPATH="${PYTHONLIBS_DIR}:${PYTHONPATH}"
