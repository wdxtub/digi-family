package main

import (
	"blog-tools/tools"
	"blog-tools/utils"
	"fmt"
	"os"
)

func main() {
	utils.ShowHeader()
	cmdList := os.Args
	if len(cmdList) == 1 {
		utils.ShowHelp()
		return
	}

	// 第一层命令
	switch cmdList[1] {
	case "migrate":
		if len(cmdList) != 5 {
			utils.PrintLog(utils.LogError, "参数个数错误")
			utils.ShowHelp()
			return
		}
		// 第二层命令
		switch cmdList[2] {
		case "hexo2hugo":
			utils.PrintLog(utils.LogInfo, "正在进行 hexo 到 hugo 的转换")
			utils.PrintLog(utils.LogInfo, fmt.Sprintf("源文件夹: %s", cmdList[3]))
			utils.PrintLog(utils.LogInfo, fmt.Sprintf("目标文件夹: %s", cmdList[4]))
			tools.Hexo2Hugo(cmdList[3], cmdList[4])
		}
	}

}
