#!/usr/bin/env bash

DEPENDENCIES_PATH="dependencies"
GIT_REPO="https://github.com/sstephenson/bats.git"
GIT_BRANCH="master"

set -eo pipefail
set -u

INITIAL_PWD=$PWD

BASE_PATH=${1:-$INITIAL_PWD}
FORCE=${2:--keep}

function get_bats_repo_and_branch() {
    echo "Current directory: $PWD"
    echo "Base path: $BASE_PATH"
    FORCE=$1
    PREV_PWD=$PWD
    CHECKOUT_DIR="bats"

    if [ ! -d "$BASE_PATH/$DEPENDENCIES_PATH" ]; then
        mkdir -p "$BASE_PATH/$DEPENDENCIES_PATH"
    fi

    cd "$BASE_PATH/$DEPENDENCIES_PATH"

    if [[ ! -d "$CHECKOUT_DIR" ]]; then
        echo "Checking out branch $GIT_BRANCH of repo $GIT_REPO ..."
        git clone --branch $GIT_BRANCH $GIT_REPO $CHECKOUT_DIR
        pull_repository
    else
        echo "Directory $CHECKOUT_DIR already exists."

        if [ $FORCE == "-force" ]; then
            echo "$FORCE parameter passed, updating dependency anyway."
            pull_repository
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

get_bats_repo_and_branch "$BASE_PATH" "$FORCE"

cd $INITIAL_PWD
ls -la

STATUS=${?}

exit ${STATUS}