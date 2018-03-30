#!/bin/bash
echo "========================================"
echo "    小土刀的服务器自动配置工具 V0.1       " 
echo "              2018.03.30"
echo "              wdx & mzy"
echo "========================================"

if [ $# -ne 1 ] ; then
    echo "Usage: ./env_setup.sh gopath"
    exit
fi

go_dir=$1

packages="tmux wget gcc make"
echo "Step 1.安装基础开发包" ${packages}
yum install -y ${packages}
if [ $? -ne 0 ];then
  echo "安装基础包失败，请检查后重试"
  exit
fi
echo "安装成功"
echo "========================================"

echo "Step 2.使用 RPM 包安装 Python3"
./module/install_py3.sh
if [ $? -ne 0 ];then
  echo "安装 Python 3 失败，请检查后重试"
  exit
fi
echo "安装成功。特别提示：Python 3.6 可直接使用 python3.6 -m venv venv_name 创建虚拟环境"
echo "========================================"

echo "Step 3.源码安装 Go"
./module/install_go.sh $go_dir
if [ $? -ne 0 ];then
  echo "安装 Go 失败，请检查后重试"
  exit
fi
echo "安装成功"
echo "========================================"