package main 

import(
	"fmt"
	"bufio"
	"net"
)

var Tablero = make([][]int ,3)  // Escogi una matriz para representar el tablero, 1 representa las fichas del jugador 1
								// Representa las fichas del jugador 2	

func verificar_Tablero(x, y int) bool{
		if Tablero[x][y] == 0{
			return true 
		}
		return false
}

func verificar_Posicion(x, y int) bool {
	return (x >= 0 && x < 3) && (y >= 0 && y < 3)
}	

func MoverJugador() (uint,uint){
	var x, y uint
	for {
		fmt.Printf("Jugado 1 ingrese la posicion X y Y, separados por un espacio: ")
		fmt.Scan(&x,&y)
		if verificar_Posicion(int(x),int(y)) {
			break 
		}
		fmt.Println("Posiciones invalidas")
	}
	return x,y
}


func Verificar_Ganador( Jugador int) (bool,int) {
	 veriFila, veriColumna, veriXDerecha, veriXIzquierda:= 0,0,0,0
	 for i := 0; i < 3; i++ {
	 	for j := 0; j < 3; j++ {
	 		if Tablero[i][j] == Jugador {
	 			veriFila++
	 		} 
	 		if Tablero[j][i] == Jugador {
	 			veriColumna++;
	 		}
	 		if Tablero[j][j] == Jugador {
	 			veriXDerecha++;
	 		}
	 		if Tablero[j][2-j] == Jugador {
	 			veriXIzquierda++;
	 		}		
	 	}
	 	if veriFila == 3 || veriColumna == 3 || veriXDerecha == 3 || veriXIzquierda == 3 {
	 		return true,Jugador
	 	}
	 	veriFila = 0
	 	veriColumna = 0
	 	veriXDerecha = 0
	 	veriXIzquierda = 0
	 }
	 return false,Jugador
}

func handle(conn net.Conn) string{
    defer conn.Close()
    r := bufio.NewReader(conn)
    msg := " "
    msg, _ = r.ReadString('\n')
    fmt.Printf("recibido: %s", msg)
    slc1 := []rune(msg[:len(msg)-1])
    x2, y2 := int(slc1[1]-'0'),int(slc1[3]-'0')
    if verificar_Posicion(x2,y2) {
    	if	verificar_Tablero(x2,y2) {
    		Tablero[x2][y2]=2
    		return "Sigue Jugando"
    	} else{
    		return "Posicion enviada invalida"	
    	}
    }
    return "Posicion enviada invalida"
//   fmt.Fprintf(conn, "re: %s", msg)
} 

func enviar(remote ,mensaje string, Gano bool) {
    conn, _ := net.Dial("tcp",remote)
    defer conn.Close()
/*    if mensaje == "Posicion enviada invalida" {
    	 fmt.Fprintln(conn,mensaje)
    }*/
    if Gano == true {
    	fmt.Fprintln(conn, mensaje)
    } else{
     fmt.Fprintln(conn,Tablero)  
    }
}

func main() {
	for i:= 0; i < 3;i++ {		 
		Tablero[i] = make([]int ,3)
	}
	

	for i:= 0; i < 3; i++ {
		fmt.Println(Tablero[i])
	}

	ln, _ := net.Listen("tcp", "192.168.1.5:8000")
    defer ln.Close()
    remote := "192.168.111.128:8001"
    for {
		x,y := MoverJugador()
		
		
		if verificar_Tablero(int(x),int(y)) {
			Tablero[x][y] = 1
		} else {
			fmt.Println("Posicion invalida")
		}
		for i:= 0; i < 3; i++ {
			fmt.Println(Tablero[i])
		}
		Gano, GanoJu := Verificar_Ganador(1)
		if Gano == true && GanoJu == 1{
			fmt.Println("Ganaste Jugador 1")
			enviar(remote,"Perdiste, gano jugador 1",Gano )
			break
		} else {
			conn, _ := ln.Accept()
			mensaje := handle(conn)
			Gano,GanoJu = Verificar_Ganador(2)
			if Gano == true && GanoJu== 2{
				fmt.Println("Perdiste Jugador 1")
				enviar(remote,"Ganaste Jugador 2",Gano)
				break
			}else {
			enviar(remote,mensaje,Gano )
			}
		}
	}

}


