package utils

import "errors"

// Division 除法函数
func Division(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("除数不能为 0")
	}

	return a / b, nil
}
