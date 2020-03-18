#!/bin/bash

source $DOTFILES/bin/remote-setup.sh

RSYNC_EXCLUDE_OPTS=(--exclude ".hg" --exclude ".git" --exclude "*build/" --exclude "build*/" --exclude ".tox" --exclude "*.deb" --exclude "*.rpm" --exclude ".cache/")
RSYNC_RECURSIVE=--recursive

for i in "$@"
do
case $i in
    -a|--all)
    RSYNC_EXCLUDE_OPTS=()
    shift # past argument=value
    ;;
    -d|--delete)
    RSYNC_OPTS+=(--delete --delete-excluded)
    shift # past argument=value
    ;;
    -s|--shallow)
    RSYNC_RECURSIVE=--dirs
    shift # past argument=value
    ;;
    *)
            # unknown option
    ;;
esac
done

echo "rsync --verbose $RSYNC_RECURSIVE --times --compress --progress ${RSYNC_OPTS[@]} ${RSYNC_EXCLUDE_OPTS[@]} $HOST:$DEST_DIR/ $CURR_DIR"
rsync --verbose $RSYNC_RECURSIVE --times --compress --progress "${RSYNC_OPTS[@]}" "${RSYNC_EXCLUDE_OPTS[@]}" $HOST:$DEST_DIR/ $CURR_DIR