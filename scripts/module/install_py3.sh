#!/bin/bash
# Reference https://segmentfault.com/a/1190000009922582
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum makecache
yum -y install python36u python36u-pip python36u-devel