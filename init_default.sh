#!/usr/bin/env bash

CURR_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

sample=$CURR_DIR/server/br_sample.env
target=$CURR_DIR/br.env

if [ -e "$target" ]; then
   echo "$target already exists.. exiting to avoid overriding current settings"
   exit 1
fi

cp $sample $target

function set_key {
    key=$(python -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)')
    sed -i'' -e "s/$1=.*/$1='$key'/g" $target
}

set_key "SECRET_KEY"

mkdir $CURR_DIR/data
mkdir $CURR_DIR/data/exports/