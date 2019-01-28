#!/bin/bash
while read l; do
  grep -rh "$l" . | grep -f /dev/stdin linked_users_in_IZ_activeloan_au.csv >> aufails.csv
done < aufailed.txt
