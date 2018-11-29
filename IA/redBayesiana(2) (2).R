library(bnlearn)
asia.dag = model2network("[A][S][T|A][L|S][B|S][E|T:L][D|B:E][X|E]")
lv = c("yes", "no")
#coloco las probabilidades de mi grafo
A.prob = array(c(0.01, 0.99), dim = 2, dimnames = list(A = lv))
S.prob = array(c(0.5,  0.5),  dim = 2, dimnames = list(S = lv))
T.prob = array(c(0.05, 0.95, 0.01, 0.99), dim = c(2, 2),
               dimnames = list(T = lv, A = lv))
L.prob = array(c(0.1, 0.9, 0.01, 0.99), dim = c(2, 2),
               dimnames = list(L = lv, S = lv))
B.prob = array(c(0.6, 0.4, 0.3, 0.7), dim = c(2, 2),
               dimnames = list(B = lv, S = lv))
E.prob = array(c(1, 0, 1, 0, 1, 0, 0, 1), dim = c(2, 2, 2),
               dimnames = list(E = lv, T = lv, L = lv))
D.prob = array(c(0.9, 0.1, 0.7, 0.3, 0.8, 0.2, 0.1, 0.9), dim = c(2, 2, 2),
               dimnames = list(D = lv, B = lv, E = lv))
X.prob = array(c(0.98, 0.02, 0.05, 0.95), dim = c(2, 2),
               dimnames = list(X = lv, E = lv))

#tabla de probabilidad condicional CPT
cpt = list(A = A.prob, S = S.prob, T = T.prob, L = L.prob, B = B.prob,
           D = D.prob, E = E.prob, X = X.prob)

#calcula los valores de la CPT
bn = custom.fit(asia.dag, cpt)

#ejecutar consultas
bn$A
bn$S
bn$T
bn$L
bn$B
bn$E
bn$X
bn$D

print(bn$D, perm = c("E", "B"))

bn.fit.barchart(bn$D)


#hacemos consultas basicas
cpquery(bn, (T=="yes"), TRUE)
cpquery(bn, (L=="yes"), TRUE)
cpquery(bn, (B=="yes"), TRUE)

#hacemos consultas complejas
cpquery(bn, (T=="yes"), (A=="yes" & S=="no"))
cpquery(bn, (L=="yes"), (A=="yes" & S=="no"))
cpquery(bn, (B=="yes"), (A=="yes" & S=="no"))

#mas consultas
cpquery(bn, (T=="yes"), (A=="yes" & S=="no" & D=="yes" & X=="yes"))
cpquery(bn, (L=="yes"), (A=="yes" & S=="no" & D=="no" & X=="yes"))
cpquery(bn, (B=="yes"), (A=="yes" & S=="no" & D=="no" & X=="yes"))


#Cuál es probabilidad de que visita Asia 
#dado que tiene tuberculosis
cpquery(bn, (A=="yes"), (T=="yes"))

#Cuál es probabilidad de que sea fumador, 
#si tiene cáncer y bronquitis
cpquery(bn, (S=="yes"), (L=="yes" & B=="yes"))

#Cuál es la probabilidad que tenga disnea, si tiene 
#tuberculosis, visitó Asia, no fuma y tiene bronquitis
cpquery(bn, (D=="yes"), (T=="yes" & A=="yes" & S=="no" & B=="yes"))

# En la prueba ha salido positivo Rayos x, cuál es 
#la probabilidad de que tenga cáncer.
cpquery(bn, (L=="yes"), (X=="yes"))

# Cuál es la probabilidad que tenga tuberculosis 
#y bronquitis, ya que en la prueba ha salido positivo 
#en rayos x y tiene disnea
cpquery(bn, (T=="yes" & B=="yes"), (X=="yes" & D=="yes"))
