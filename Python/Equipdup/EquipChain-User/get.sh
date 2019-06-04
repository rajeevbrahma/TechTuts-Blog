#!/bin/bash  
# To get the Port number , username and password
echo " "
echo "---------Portnumber------------"
port=sudo grep rpc ~/.multichain/echain/params.dat
echo " "
echo "---------Username--------------"
username=sudo grep rpcuser ~/.multichain/echain/multichain.conf
echo " "
echo "---------Password--------------"
password=sudo grep rpcpassword ~/.multichain/echain/multichain.conf