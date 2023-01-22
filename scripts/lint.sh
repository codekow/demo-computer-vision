#!/bin/bash
set -e

usage(){
  echo "
  setup virtualenv:
  python -m venv venv
  "
  exit 0
}

setup_venv(){
  python -m venv venv
  pip install -q -U pip
  pip install -q -r requirements-dev.txt

  check_venv || usage
}

check_venv(){
  # activate python venv
  # shellcheck disable=SC2015,SC1091
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
