package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// GetFilelist 遍历文件夹，获取列表
func GetFilelist(path string) []string {
	filelist := []string{}
	err := filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
		if f == nil {
			return err
		}
		if f.IsDir() {
			return nil
		}
		if strings.Contains(path, "DS_Store") {
			return nil
		}
		filelist = append(filelist, path)
		return nil
	})
	if err != nil {
		fmt.Printf("filepath.Walk() returned %v\n", err)
	}
	return filelist
}
