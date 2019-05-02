#!/usr/bin/env bash

set -e

for snmprec in $(find data -name "*.snmprec")
do
  datafile.py --input-file $snmprec \
      --output-file /dev/null \
      --deduplicate-records \
      --sort-records
done
