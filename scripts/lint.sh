#!/bin/bash
# shellcheck disable=SC2015,SC1091
set -e

usage(){
  echo "
  setup virtualenv:
  python3 -m venv venv
  "
  exit 0
}

setup_venv(){
  python3 -m venv venv
  source venv/bin/activate
  pip install -q -U pip
  pip install -q -r requirements-dev.txt

  check_venv || usage
}

check_venv(){
  # activate python venv
  [ -d venv ] && . venv/bin/activate || setup_venv
}

check_venv

# chcek scripts
shellcheck scripts/*

# check spelling
pyspelling -c .spellcheck.yaml

# check yaml
yamllint . && echo "YAML check passed :)"

# validate manifests
scripts/validate_manifests.sh
