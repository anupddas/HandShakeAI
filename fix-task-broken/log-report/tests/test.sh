#!/bin/bash
# tests/test.sh
set -u

mkdir -p /logs/verifier

# pytest + pytest-json-ctrf are baked into environment/Dockerfile — no verify-time installs.
pytest /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json

if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi