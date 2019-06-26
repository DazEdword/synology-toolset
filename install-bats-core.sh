#!/usr/bin/env bash

DEPENDENCIES_PATH="dependencies"
GIT_REPO="https://github.com/bats-core/bats-core.git"
GIT_BRANCH="master"
PREV_PWD=$PWD
TMP_DIR=$PWD/$DEPENDENCIES_PATH/tmp

set -eo pipefail
set -u

FORCE=${1:--keep}

function get_bats_repo_and_branch() {
    FORCE=$1
    CHECKOUT_DIR="tmp/bats"
    INSTALATION_DIR="bats-core"

    if [ ! -d "$DEPENDENCIES_PATH" ]; then
        mkdir -p "$DEPENDENCIES_PATH"
    fi

    cd "$DEPENDENCIES_PATH"

    if [[ ! -d "$INSTALATION_DIR" ]]; then
        echo "Checking out branch $GIT_BRANCH of repo $GIT_REPO ..."
        git clone --branch $GIT_BRANCH $GIT_REPO $CHECKOUT_DIR
        pull_repository
        run_package_installation $INSTALATION_DIR
    else
        echo "Directory $INSTALATION_DIR already exists."

        if [ $FORCE == "-force" ]; then
            echo "$FORCE parameter passed, updating dependency anyway."
            git clone --branch $GIT_BRANCH $GIT_REPO $CHECKOUT_DIR
            pull_repository
            run_package_installation $INSTALATION_DIR
        else
            echo "Call the script with a -force parameter to override current contents."
        fi
    fi
}

function pull_repository() {
    cd $CHECKOUT_DIR
    echo "Resetting any local changes before 'git pull'."
    git checkout .
    git checkout $GIT_BRANCH
    echo "Bringing up to date branch $GIT_BRANCH of repo $GIT_REPO ..."
    git pull

    cd $PREV_PWD
}

function run_package_installation() {
    echo "Installing bats-core..."

    local absolute_installation_path="$PWD/$DEPENDENCIES_PATH/$CHECKOUT_DIR"

    $absolute_installation_path/install.sh $PWD/$DEPENDENCIES_PATH/$INSTALATION_DIR
    
    # Cleanup
    echo "Cleaning up installation files..."
    rm -rf $TMP_DIR
}

get_bats_repo_and_branch "$FORCE"

STATUS=${?}

exit ${STATUS}