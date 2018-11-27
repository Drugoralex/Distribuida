package main

import (
	"fmt"
)

var ch chan bool

func matrixConvolution(a, b [][]float64) [][]float64 {
	na, ma := len(a), len(a[0])
	nb, mb := len(b), len(b[0])

	resultado := make([][]float64, na)
	for i := range resultado {
		resultado[i] = make([]float64, ma)
	}

	for i := 1; i < na-1; i++ {
		for j := 1; j < ma-1; j++ {
			go func(i, j int) {
				sum := 0.0
				for k := 0; k < nb; k++ {
					for l := 0; l < mb; l++ {
						sum += a[i+k-1][j+l-1] * b[k][l]
					}
				}
				resultado[i][j] = sum
				ch <- true
			}(i, j)
		}
	}
	for i := 1; i < na-1; i++ {
		for j := 1; j < ma-1; j++ {
			<-ch
		}
	}
	return resultado
}

func main() {
	ch = make(chan bool)
	a := [][]float64{ {35, 40, 41, 45, 50},
			{40, 40, 42, 46, 52},
			{42, 46, 50, 55, 55},
			{48, 52, 56, 58, 60},
			{56, 60, 65, 70, 75}}

	b := [][]float64{{0, 1, 0},
			{0, 0, 0},
			{0, 0, 0}}
	
	resultado := matrixConvolution(a, b)
	fmt.Println(resultado)
}