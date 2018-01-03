#!/bin/bash

geth --identity "node1" --networkid 42 --datadir "." --nodiscover --mine --rpc --rpcport "8042" --port "30303" --unlock 0 --password pwd.sec --ipcpath geth.ipc
