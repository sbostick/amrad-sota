#!/usr/bin/env bash
set -eu -o pipefail

{
  head -n2 data/summitslist.csv | tail -1
  grep -E '^W7W/(KG|SN|CW|MC|PL|LC|SO|NO|RS)' data/summitslist.csv
} | column -s, -t
