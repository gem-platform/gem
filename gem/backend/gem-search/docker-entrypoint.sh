#!/bin/sh
indexer mongo
crond
searchd --nodetach