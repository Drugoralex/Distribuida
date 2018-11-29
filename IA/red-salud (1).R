library(bnlearn)
dag =  model2network("[D][A][F][P|D:A][I|P:F]")
lv = c("si", "no")
lv2 = c("equilibrada", "no-equilibrada")
lv3 = c("alta", "normal")

D.prob = array(c(0.1, 0.9), dim = 2, dimnames = list(D = lv))
A.prob = array(c(0.4, 0.6), dim = 2, dimnames = list(A = lv2))
F.prob = array(c(0.4, 0.6), dim = 2, dimnames = list(F = lv))
P.prob = array(c(0.01, 0.99, 0.25, 0.75, 0.2, 0.8, 0.7,0.3), 
               dim = c(2, 2, 2),
               dimnames = list(P = lv3, D = lv, A = lv2))
I.prob = array(c(0.8, 0.2, 0.7, 0.3, 0.6, 0.4, 0.3, 0.7), 
               dim = c(2, 2, 2),
               dimnames = list(I = lv, F = lv, P = lv3))


#tabla de probabilidad condicional CPT
cpt = list(D = D.prob, A = A.prob, F = F.prob, 
           P = P.prob, I = I.prob)


#calcula los valores de la CPT
bn = custom.fit(dag, cpt)

bn$D
bn$A
bn$F
bn$P
bn$I

#hacemos consultas
#A) probabilidad conjunta
q1 <- cpquery(bn, (I=="si" & P=="alta" & F=="si" &  D=="si" & A=="equilibrada" ), TRUE)
q1
a <- cpquery(bn, (I=="si"), (P=="alta" & F=="si"))
a
b <- cpquery(bn, (P=="alta"), (D=="si" & A=="equilibrada"))
b
c <- cpquery(bn, (F=="si"), TRUE)
c
d <- cpquery(bn, (D=="si"), TRUE)
d
e <- cpquery(bn, (A=="equilibrada"), TRUE)
e

#B) Calcular la probabilidad de ser fumador si 
#se ha tenido un infarto y no se hace deporte
f<- cpquery(bn, (F=="si"), (I=="si" & D=="no"))
f

#C) Calcular la probabilidad de ser deportista, 
#si se ha verificado que no ha tenido infarto y 
#se alimenta equilibradamente.
g<- cpquery(bn, (D=="si"), (I=="no" & A=="equilibrada"))
g

#D) Probabilidad de tener infarto, dado que es 
#deportista, se alimenta equilibradamente y 
#tiene presión sanguínea alta
h<- cpquery(bn, (I=="si"), (D=="si" & A=="equilibrada" & P=="alta"))
h
