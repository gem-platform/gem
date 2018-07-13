#!/bin/sh
indexer mongo
indexer entities
crond
searchd --nodetach