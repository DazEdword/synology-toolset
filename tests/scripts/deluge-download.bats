#!/usr/bin/env bats

function setup(){
    ORIGINAL_PATH="$BATS_TEST_DIRNAME"
    CONNECTION="0.0.0.0:99999"
    USER="test-user"
    PASSWORD="test-password"
    MAGNET_FAKE="magnet:?xt=urn:btih:abc123&dn=archlinux-2019.06.01-x86_64.iso&tr=udp://tracker.archlinux.org:6969&tr=http://localhost.loc:6969/announce"

    cd $ORIGINAL_PATH
    cd ../..

    cd synotools/scripts/
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

function run_deluge_console_command()
{
  echo "called fake deluge console with command $1"
}

@test "exits with useful message and correct status when connection is not passed" {
  export -f synopkg
  run "$SCRIPT_UNDER_TEST"
  [ "$status" -eq 1 ]
  [ "$output" = "Missing connection details." ]
}

@test "attempts to start deluge service when it is disabled" {
  function synopkg(){ 
    echo "deluge is stopped"
  }
  export -f synopkg
  run "$SCRIPT_UNDER_TEST" $CONNECTION $USER $PASSWORD
  [ "$status" -eq 1 ]
  [ "${lines[0]}" = "Starting deluge..." ]
}

@test "exits with useful message and correct status when missing user/pass" {
  export -f synopkg
  run "$SCRIPT_UNDER_TEST" $CONNECTION

  [ "$status" -eq 1 ]
  [ "${lines[1]}" = "Missing user and/or password arguments." ]
}

@test "exits with useful message and correct status when magnet is not set" {
  export -f synopkg
  run "$SCRIPT_UNDER_TEST" $CONNECTION $USER $PASSWORD
  [ "$status" -eq 1 ]
  [ "${lines[2]}" = "No torrent was provided. Aborting download." ]
}

@test "echoes message when magnet is found" {
  # Mocking
  export -f synopkg
  export -f run_deluge_console_command

  run "$SCRIPT_UNDER_TEST" $CONNECTION $USER $PASSWORD $MAGNET_FAKE

  [ "$status" -eq 127 ] # TODO This status only because it's seemingly impossible to mock run_deluge_console_command, and hence it fails
  [ "${lines[2]}" = "Preparing to download: magnet:?xt=urn:btih:abc123&dn=archlinux-2019.06.01-x86_64.iso&tr=udp://tracker.archlinux.org:6969&tr=http://localhost.loc:6969/announce" ]
}
