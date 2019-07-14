#!/usr/bin/env bats

function setup(){
    ORIGINAL_PATH="$BATS_TEST_DIRNAME"

    cd $ORIGINAL_PATH
    cd ../..

    cd synotools/scripts/
    SRC_CODE_ROOT="$PWD"
    SCRIPT_UNDER_TEST="$SRC_CODE_ROOT/vpn-check-connection.sh"
}

function teardown()
{
    cd "$ORIGINAL_PATH"
}

@test "checks vpn connection status with synovpnc command and get_conn parameter" {  
  function synovpnc(){ 
    echo $1
  }
  export -f synovpnc
  run "$SCRIPT_UNDER_TEST"

  echo "output = ${output}"

  [ "$status" -eq 0 ]
  [ "${lines[0]}" = "Checking VPN connection..." ]
  [ "${lines[1]}" = "VPN connected: get_conn" ]
}

@test "echoes non connection message when get_conn returns not connected message" { 
  function synovpnc(){ 
    echo "No connection!!"
  }
  
  export -f synovpnc
  run "$SCRIPT_UNDER_TEST"

  [ "$status" -eq 0 ]
  [ "${lines[0]}" = "Checking VPN connection..." ]
  [ "${lines[1]}" = "VPN is not connected." ]
}


@test "echoes connection message when get_conn returns returns connection other than no connection message" { 
  function synovpnc(){ 
    echo "TestVpn"
  }
  
  export -f synovpnc
  run "$SCRIPT_UNDER_TEST"

  [ "$status" -eq 0 ]
  [ "${lines[0]}" = "Checking VPN connection..." ]
  [ "${lines[1]}" = "VPN connected: TestVpn" ]
}
