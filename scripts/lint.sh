#!/bin/bash
set -e

# activate python venv
# shellcheck disable=SC1091
[ -d venv ] && . venv/bin/activate || exit

# chcek scripts
shellcheck scripts/*

# check spelling
pyspelling -c .spellcheck.yaml

# check yaml
yamllint . && echo "YAML check passed :)"

# validate manifests
scripts/validate_manifests.sh
