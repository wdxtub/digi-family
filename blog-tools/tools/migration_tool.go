package tools

import (
	"blog-tools/utils"
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
	yaml "gopkg.in/yaml.v2"
)

// Hexo2Hugo 转换函数
func Hexo2Hugo(sourceDir, targetDir string) error {
	filelist := utils.GetFilelist(sourceDir)
	utils.PrintDotLine("=", 30)
	utils.PrintLog(utils.LogInfo, fmt.Sprintf("总计需要处理 %d 个文件", len(filelist)))
	utils.PrintDotLine("=", 30)
	for k, v := range filelist {
		utils.PrintLog(utils.LogInfo, fmt.Sprintf("正在处理第 %d 个文件 %s", k+1, v))
		result, err := processHexo2HugoFile(v)
		if err != nil {
			utils.PrintLog(utils.LogError, err.Error())
			continue
		}
		target := strings.Replace(v, sourceDir, targetDir, 1)
		utils.PrintLog(utils.LogInfo, fmt.Sprintf("保存为 %s", target))
		ioutil.WriteFile(target, []byte(result), os.ModePerm)
	}
	return nil
}

// 返回更新后的文件内容
func processHexo2HugoFile(path string) (string, error) {
	// 简单来说，这里做的是一个从 yaml 到 toml 的转换
	metaYaml := []string{}
	body := []string{}
	isMeta := true
	content, err := ioutil.ReadFile(path)
	if err != nil {
		return "", err
	}
	// 分离文件内容
	for _, line := range strings.Split(string(content), "\n") {
		if isMeta {
			if line == "---" {
				isMeta = false
			} else {
				metaYaml = append(metaYaml, line)
			}
		} else {
			body = append(body, line)
		}
	}
	// 处理 header
	header := make(map[interface{}]interface{})

	err = yaml.Unmarshal([]byte(strings.Join(metaYaml, "\n")), header)
	if err != nil {
		return "", err
	}

	date, _ := time.Parse("2006-01-02 15:04:05", header["date"].(string))
	var newHeader = map[string]interface{}{
		"title": header["title"],
		"date":  date,
		"tags":  header["tags"],
	}
	buf := new(bytes.Buffer)
	if err := toml.NewEncoder(buf).Encode(newHeader); err != nil {
		utils.PrintLog(utils.LogFatal, err.Error())
		return "", err
	}
	result := strings.Split(buf.String(), "\n")
	newHeaderStr := fmt.Sprintf("---\n%s\n%s+08:00\n%s\n---\n", result[2], result[0][:len(result[0])-1], result[1])
	newHeaderStr = strings.Replace(newHeaderStr, " = ", ": ", -1)
	bodyStr := strings.Join(body, "\n")
	bodyStr = strings.Replace(bodyStr, "<!-- more -->", "<!--more-->", 1)
	return fmt.Sprintf("%s%s", newHeaderStr, bodyStr), nil
}
