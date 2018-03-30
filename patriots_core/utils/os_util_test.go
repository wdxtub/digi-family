package utils

import "testing"

/*
 * 普通测试 go test -v
 * 压力测试 go test -test.bench=".*" -count=5
 */

func Test_Division_1(t *testing.T) {
	if i, e := Division(6, 2); i != 3 || e != nil {
		t.Error("除法测试未通过，无法得到正确结果")
	} else {
		t.Log("除数不为零时，可以正常进行除法")
	}
}

func Test_Division_2(t *testing.T) {
	if _, e := Division(6, 0); e == nil {
		t.Error("除法测试未通过，除以 0 没有返回错误")
	} else {
		t.Log("除数为 0 测试通过")
	}
}

func Benchmark_Division(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Division(4, 5)
	}
}

func Benchmark_TimeConsumingFunction(b *testing.B) {
	b.StopTimer()

	// init work
	b.StartTimer()
	for i := 0; i < b.N; i++ {
		Division(4, 5)
	}
}
