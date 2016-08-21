#!/bin/bash
# Script to let TravisCI deploy code to github
# Shamelessly taken and modified from
# https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
set -e # Exit with nonzero exit code if anything fails

SOURCE_BRANCH="dev"
TARGET_BRANCH="master"

function doCompile {
    python manage.py freeze
}

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy"
    exit 0
fi

# Save some useful information
REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

# Clone the existing gh-pages for this repo into build/
# Create a new empty branch if gh-pages doesn't exist yet (should only happen on first deply)
# Run our compile script
doCompile
cd build
git init
git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"
git remote add origin $REPO
git add -A .
git commit -m "Deploy to GitHub Pages: ${SHA}"

# Get the deploy key by using Travis's stored variables to decrypt deploy.pub.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in ../deploy.pub.enc -out deploy.pub -d
chmod 600 deploy.pub
eval `ssh-agent -s`
ssh-add deploy.pub

# Now that we're all set up, we can push.
git push --force $SSH_REPO $TARGET_BRANCH
