# stock_projects

使用 python3，使用 `nlp3`(mac) | `py36`(linux) 来进入环境（我这里配置了 alias）

`pip freeze > requirements.txt`

使用 `click`

安装 `pip install --editable .`
运行 `wdxstock`

## CentOS 7 安装 Python3

```bash
# 安装python3.6可能使用的依赖
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel

# 下载python3.6编译安装 到python官网下载https://www.python.org
# 下载最新版源码，使用make altinstall，如果使用make install，在系统中将会有两个不同版本的Python在/usr/bin/目录中。这将会导致很多问题，而且不好处理。
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
tar -xzvf Python-3.6.3.tgz
cd Python-3.6.3
# 把Python3.6安装到 /usr/local 目录
./configure --prefix=/usr/local
make
make altinstall

# python3.6程序的执行文件：/usr/local/bin/python3.6
# python3.6应用程序目录：/usr/local/lib/python3.6
# pip3的执行文件：/usr/local/bin/pip3.6
# pyenv3的执行文件：/usr/local/bin/pyenv-3.6

# 添加软链接
ln -s /usr/local/bin/python3.6 /usr/bin/python3
ln -s /usr/local/bin/pip3 /usr/bin/pip3
# 创建虚拟环境（最好放到统一的文件夹下）
virtualenv --no-site-packages -p /usr/local/bin/python3.6 py36
```

## Jupyter Notebook

全面更换为 python3，安装的话，进入 python3 的环境，然后执行 `pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ jupyter`

启动 `jupyter notebook`，直接使用即可，可以轻松进行测试

### 配合 Virtualenv 使用

如果要更换 kernel（一般来说不需要）

```bash
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ ipykernel
python -m ipykernel install --name nlp3
```

### 删除 kernel

查看列表 `jupyter kernelspec list`，删除对应文件夹即可

## tushare 安装

```bash
# 要按顺序
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ pandas
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ lxml
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ bs4
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ requests
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ tushare
```