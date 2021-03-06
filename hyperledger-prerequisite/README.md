
# Generate certificate and channel artifact

1. Clone repository fabric-samples check out version needed
2. Execute ./scripts/bootstrap to prepare binary file for cryptogen, cryptoconfig, cryptotxgen, etc.
3. Go to basic-network
4. Copy configtx.yaml and replace the old one
5. Copy crypto-config.yaml and replace the old one
6. Execute `./generate.yaml` - If got an error when create new `mkdir config` first

Generate file will modify follow configtx.yaml and crypto-config.yaml

```sh
#!/bin/sh
#
# Copyright IBM Corp All Rights Reserved
#
# SPDX-License-Identifier: Apache-2.0
#
export PATH=$GOPATH/src/github.com/hyperledger/fabric/build/bin:${PWD}/../bin:${PWD}:$PATH
export FABRIC_CFG_PATH=${PWD}
CHANNEL_NAME=mychannel

# remove previous crypto material and config transactions
rm -fr config/*
rm -fr crypto-config/*

# generate crypto material
cryptogen generate --config=./crypto-config.yaml
if [ "$?" -ne 0 ]; then
  echo "Failed to generate crypto material..."
  exit 1
fi

# generate genesis block for orderer
configtxgen -profile TwoOrgsOrdererGenesis -outputBlock ./config/genesis.block
if [ "$?" -ne 0 ]; then
  echo "Failed to generate orderer genesis block..."
  exit 1
fi

# generate channel configuration transaction
configtxgen -profile TwoOrgChannel -outputCreateChannelTx ./config/channel.tx -channelID $CHANNEL_NAME
if [ "$?" -ne 0 ]; then
  echo "Failed to generate channel configuration transaction..."
  exit 1
fi

# generate anchor peer transaction
configtxgen -profile TwoOrgChannel -outputAnchorPeersUpdate ./config/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP
if [ "$?" -ne 0 ]; then
  echo "Failed to generate anchor peer update for Org1MSP..."
  exit 1
fi

```

**Note**: Ensure that all file in the place. Check by see persistent volume config.
**Note2**: Do not forget to export PATH to binary file like `export PATH=$PATH:$PWD/bin`

## After make change configs

Update ca k8s file to use correct private key

## If want to change dind to hostPath

Remove dind components and change `tcp://localhost:2375` to `unix:///host/var/run/docker.sock`
