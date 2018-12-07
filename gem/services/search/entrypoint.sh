#!/bin/sh
indexer laws
indexer entities
crond
python3 /usr/app/healtcheck.py &
searchd --nodetach
