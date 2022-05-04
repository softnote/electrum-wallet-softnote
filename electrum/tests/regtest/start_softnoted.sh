#!/usr/bin/env bash
export HOME=~
set -eux pipefail
mkdir -p ~/.softnote
cat > ~/.softnote/softnote.conf <<EOF
regtest=1
txindex=1
printtoconsole=1
rpcuser=doggman
rpcpassword=donkey
rpcallowip=127.0.0.1
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28333
fallbackfee=0.0002
[regtest]
rpcbind=0.0.0.0
rpcport=18554
EOF
rm -rf ~/.softnote/regtest
screen -S softnoted -X quit || true
screen -S softnoted -m -d softnoted -regtest
sleep 6
softnote-cli createwallet test_wallet
addr=$(softnote-cli getnewaddress)
softnote-cli generatetoaddress 150 $addr > /dev/null
