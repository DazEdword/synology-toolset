#!/usr/bin/env bats

load helpers/mocks/stub

function setup(){
    ORIGINAL_PATH="$BATS_TEST_DIRNAME"
    MAGNET_FAKE="magnet:?xt=urn:btih:abc123&dn=archlinux-2019.06.01-x86_64.iso&tr=udp://tracker.archlinux.org:6969&tr=http://localhost.loc:6969/announce"

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

function synopkg(){ 
  echo "called fake synopkg"
}

# Run with ./dependencies/bats/bin/bats tests/scripts/deluge-download.bats

@test "exits with useful message and correct status when magnet is not set" {
  run "$SCRIPT_UNDER_TEST"
  [ "$status" -eq 1 ]
  [ "$output" = "No magnet was provided. Aborting download." ]
}

@test "prints message when magnet is found" {
  # Mocking
  export -f synopkg

  run "$SCRIPT_UNDER_TEST" $MAGNET_FAKE
  echo "$output"
  #[ "$status" -eq 0 ]
  [ "$output" = "Preparing to download: magnet:?xt=urn:btih:abc123&dn=archlinux-2019.06.01-x86_64.iso&tr=udp://tracker.archlinux.org:6969&tr=http://localhost.loc:6969/announce" ]
}

# @test "addition using bc" {
#   result="$(echo 2+2 | bc)"
#   [ "$result" -eq 4 ]
# }

# @test "addition using dc" {
#   result="$(echo 2 2+p | dc)"
#   [ "$result" -eq 4 ]
# }
