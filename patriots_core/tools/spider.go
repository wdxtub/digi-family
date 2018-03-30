package tools

import (
	"fmt"

	"github.com/gocolly/colly"
)

// StartSpider 启动抓取
func StartSpider(url string) {
	c := colly.NewCollector()
	count := 0

	c.AllowedDomains = []string{"wdxmzy.com"}

	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		fmt.Printf("Link found: %q -> %s\n", e.Text, link)
		c.Visit(e.Request.AbsoluteURL(link))
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
		count++
	})

	c.Visit(url)
	fmt.Println("共访问", count, "个页面")
}
