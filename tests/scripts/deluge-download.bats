#!/usr/bin/env bats

function setup(){
    echo "Setup on the go!"
    ORIGINAL_PATH="$BATS_TEST_DIRNAME"
    cd $ORIGINAL_PATH
    cd ../..

    cd synology-toolset/scripts/
    SRC_CODE_ROOT="$PWD"
    SCRIPT_UNDER_TEST="$SRC_CODE_ROOT/deluge-download.sh"
}

function teardown()
{
    cd "$ORIGINAL_PATH"
}

@test "just an example to understand bats" {
  run "$SCRIPT_UNDER_TEST"
  echo "$output"
  [ "$status" -eq 1 ]
#   [ "$output" = "foo: no such file 'nonexistent_filename'" ]
}

@test "addition using bc" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]
}

@test "addition using dc" {
  result="$(echo 2 2+p | dc)"
  [ "$result" -eq 4 ]
}
