#!/usr/bin/env bash

CURR_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

mkdir $CURR_DIR/data
mkdir $CURR_DIR/data/redacted/
mkdir $CURR_DIR/data/logs/