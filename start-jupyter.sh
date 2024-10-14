#!/bin/bash

#docker run -it -p 8888:8888 quay.io/jupyter/scipy-notebook:2024-10-07

# For user jovyan in the container.
uid=1000
gid=100

subuidSize=$(( $(podman info --format "{{ range .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))


podman run -it --rm -p 8888:8888 \
    -v "${PWD}":/home/jovyan/work --user $uid:$gid \
    --uidmap $uid:0:1 --uidmap 0:1:$uid --uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
    --gidmap $gid:0:1 --gidmap 0:1:$gid --gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
    quay.io/jupyter/scipy-notebook:2024-10-07
