package main

import (
	"fmt"
)

const TH = 5
var ch chan bool

func Multiplicacion(a, b [][]float64) [][]float64 {
	fa,ca := len(a), len(a[0])
	fb,cb := len(b), len(b[0])

	if( ca != fb) {
		return nil
	}

	c := make([][]float64, fa)
	for i := range c {
		c[i] = make([]float64,cb)
	}

	for i:= 0 ; i < fa ; i++ {
		for j := 0; j < cb; j++ {
			go func(i,j int) {
				sum:= 0.0
				for k:= 0; k < ca; k++{
					sum += a[i][k] * b[k][j]
				}
				c[i][j] = sum
				ch<-true 
			}(i,j)
		}

	}

	for i:= 0 ; i < fa ; i++ {
		for j := 0; j < cb; j++ {
			<-ch
		}
	}
	
	return c
}


func main() {
	ch = make(chan bool)
	a := [][]float64 {{4, 3, 1, 2},
                      {5, 1, 3, 4},
                      {2, 2, 1, 3}}
    b := [][]float64 {{5, 5, 5},
                      {2, 1, 3},
                      {4, 2, 2},
                      {3, 2, 2}}

    fmt.Println(Multiplicacion(a,b))
}