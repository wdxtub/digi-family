#!/bin/bash

if [ $# -ne 1 ] ; then
    echo "Usage: ./install_go.sh gopath"
    exit
fi

go_dir=$1

wget https://studygolang.com/dl/golang/go1.10.linux-amd64.tar.gz
# 删除老版本
if [ -d "/usr/local/go" ]; then
    echo "[INFO] Remove old version"
    sudo rm -rf /usr/local/go
fi
echo "[INFO] Done (1/4)"
# 解压
echo "[INFO] Extract files"
sudo tar -C /usr/local -xzf go1.10.linux-amd64.tar.gz
echo "[INFO] Done (2/4)"

# 更新 PATH 变量，这里支持的是 bash
echo "[INFO] Setting PATH and GOPATH"
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
mkdir -p goDir
# 添加 GOPATH 变量
echo "export GOPATH="$go_dir >> ~/.bashrc
source ~/.bashrc
go version
echo "GOPATH="$GOPATH 
echo "[INFO] Done (3/4)"

echo "[INFO] Clean up all the mess "
rm -rf *.gz 
echo "[INFO] Done (4/4)"