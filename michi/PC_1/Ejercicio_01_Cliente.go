package main

import (
    "fmt"
    "net"
    "bufio"
)

func recibir(omar net.Conn) int{
		defer omar.Close()
	    r := bufio.NewReader(omar)
	    msg := " "
	    msg, _ = r.ReadString('\n')
//	    fmt.Print(len(msg))
		fmt.Println(msg)
		return len(msg)				
}

func main() {
	var x, y uint 
	direccion :="192.168.1.5:8000"
     ln, _ := net.Listen("tcp", "192.168.111.128:8001")
    defer ln.Close()
    for{
    	conn, _ := net.Dial("tcp",direccion )
    	defer conn.Close()
	    fmt.Println("Jugado 2 ingrese la posicion X y Y, separados por un espacio: ") 
	    fmt.Scan(&x,&y)
	    pe := []int {int(x),int(y)}
	    fmt.Fprintln(conn, pe) 

	    omar, _ := ln.Accept()
	  	veri:= recibir(omar)
	  	if veri== 25 {
	  		fmt.Println("Termino el juego")
	  		break
	  	}
	}
}