#! /bin/sh

testEquality() {
  assertEquals 1 1
}

function load_and_run_shunit2() {
    original_path=$(PWD)
    
    # Parent path is either passed in or got on the fly
    parent_path=$1

    if [ -z "$parent_path" ]; then
      parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
    fi

    cd $parent_path
    cd ../..
    cd dependencies/shunit2

    shunit2_path="$PWD"

    cd "$original_path"
    . "$shunit2_path/shunit2"
}

load_and_run_shunit2






