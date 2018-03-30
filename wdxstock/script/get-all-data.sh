#!/bin/sh

echo "获取本日能够获取到的所有股票数据"
echo "@wdxtub 2017.11.30"
echo "============ brave split line ================"
echo "Step 1 获取日数据"
wdxstock spider all-price-history --interval=D 

echo "============ brave split line ================"
echo "Step 2 获取周数据"
wdxstock spider all-price-history --interval=W

echo "============ brave split line ================"
echo "Step 3 获取月数据"
wdxstock spider all-price-history --interval=M

echo "============ brave split line ================"
echo "Step 4 获取 5 分钟数据"
wdxstock spider all-price-history --interval=5

echo "============ brave split line ================"
echo "Step 5 获取 15 分钟数据"
wdxstock spider all-price-history --interval=15

echo "============ brave split line ================"
echo "Step 6 获取 30 分钟数据"
wdxstock spider all-price-history --interval=30

echo "============ brave split line ================"
echo "Step 7 获取 60 分钟数据"
wdxstock spider all-price-history --interval=60

echo "数据获取完成"