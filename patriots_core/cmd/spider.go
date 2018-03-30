// Copyright © 2017 NAME HERE <EMAIL ADDRESS>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// Source 保存数据源的数据
var Source string

// spiderCmd represents the spider command
var spiderCmd = &cobra.Command{
	Use:   "spider",
	Short: "抓取来自指定数据源的数据",
	Long:  `抓取来自指定数据源的数据，并保存在指定文件夹中`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("spider called")
		fmt.Println("Source:")
		fmt.Println(Source)
	},
}

func init() {
	RootCmd.AddCommand(spiderCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	//spiderCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	spiderCmd.Flags().StringVarP(&Source, "source", "s", "", "要抓取的数据源网址")
}
