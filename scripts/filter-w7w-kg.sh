#!/usr/bin/env bash
set -eu -o pipefail

{
  head -n2 data/summitslist.csv | tail -1
  grep -E '^W7W/KG' data/summitslist.csv
} | column -s, -t
