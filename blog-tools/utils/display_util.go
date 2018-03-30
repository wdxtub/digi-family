package utils

import (
	"fmt"
	"log"
)

const (
	// LogInfo 信息
	LogInfo = "INFO"
	// LogDebug 调试
	LogDebug = "DEBUG"
	// LogFatal 严重错误
	LogFatal = "FATAL"
	// LogError 普通错误
	LogError = "ERROR"
)

// PrintLog 输出日志
func PrintLog(level string, message string) {
	// 设置日志格式
	// log.SetFlags(Ldate | Ltime | Llongfile)
	log.Println(fmt.Sprintf("[%s] %s", level, message))
}

// PrintLine 用指定的字符输出一条线
func PrintLine(char string, length int) {
	for i := 0; i < length; i++ {
		fmt.Print(char)
	}
	fmt.Println()
}

// PrintDotLine 用指定的字符输出间隔线
func PrintDotLine(char string, length int) {
	for i := 0; i < length; i++ {
		fmt.Print(char)
		fmt.Print(" ")
	}
	fmt.Println()
}

// ShowHeader 显示 title
func ShowHeader() {
	PrintLine("=", 30)
	fmt.Println("   静态博客工具箱 0.1")
	PrintLine("=", 30)
}

// ShowHelp 输出帮助信息
func ShowHelp() {
	PrintDotLine("-", 15)
	fmt.Println("使用方法 go run main.go [command] [args]")
	fmt.Println("可选的 command")
	fmt.Println("1. migrate 迁移数据，如 go run main.go migrate [type] [source_dir] [dest_dir]")
	fmt.Println("   type 可选: hexo2hugo | ...")
	fmt.Println(" source_dir: 源目录")
	fmt.Println("   dest_dir: 转换后的目录")
}
