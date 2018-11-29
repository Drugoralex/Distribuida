#A los efectos de la discusión, digamos que necesitamos funciones de membresía 'alta', 'media' y 'baja' 
#para ambas variables de entrada y nuestra variable de salida. 
#Estos se definen en scikit-fuzzy de la siguiente manera
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generamos el universo de variables
# * Calidad y servicio en el rango subjetivo de [0, 10]
# * Propina en el rango de [0, 25] en unidades porcentuales
x_qual = np.arange(0, 11, 1) #comida
x_serv = np.arange(0, 11, 1) #servicio
x_tip = np.arange(0, 26, 1)  #propina

# Generamos las funciones de membresia difusas
serv_lo = fuzz.trimf(x_serv, [0, 0, 5]) #servicio bajo
serv_md = fuzz.trimf(x_serv, [0, 5, 10]) #servicio medio
serv_hi = fuzz.trimf(x_serv, [5, 10, 10]) #servicio bueno

qual_lo = fuzz.trimf(x_qual, [0, 0, 5]) #comida rancia (fea)
qual_md = fuzz.trimf(x_qual, [0, 5, 10]) #comida mas o menos
qual_hi = fuzz.trimf(x_qual, [5, 10, 10]) #comida alta

tip_lo = fuzz.trimf(x_tip, [0, 0, 13]) #propina tacania
tip_md = fuzz.trimf(x_tip, [0, 13, 25]) #propina promedio
tip_hi = fuzz.trimf(x_tip, [13, 25, 25]) #propina generosa

# Visualizamos estos universos y funciones
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
ax0.plot(x_qual, qual_lo, 'b', linewidth=1.5, label='Mala')
ax0.plot(x_qual, qual_md, 'g', linewidth=1.5, label='Decente')
ax0.plot(x_qual, qual_hi, 'r', linewidth=1.5, label='Deliciosa')
ax0.set_title('Calidad de la comida')
ax0.legend()
ax1.plot(x_serv, serv_lo, 'b', linewidth=1.5, label='Pobre')
ax1.plot(x_serv, serv_md, 'g', linewidth=1.5, label='Aceptable')
ax1.plot(x_serv, serv_hi, 'r', linewidth=1.5, label='Excelente')
ax1.set_title('Calidad del servicio')
ax1.legend()
ax2.plot(x_tip, tip_lo, 'b', linewidth=1.5, label='Bajo')
ax2.plot(x_tip, tip_md, 'g', linewidth=1.5, label='Medio')
ax2.plot(x_tip, tip_hi, 'r', linewidth=1.5, label='Alto')
ax2.set_title('Monto de propina')
ax2.legend()


# Quitamos los ejes superior y derecho
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()
plt.show()

# Necesitamos activar nuestras funciones de membresia en estos valores.
# Los valores exactos 6.5 and 9.8 no existen en nuestros universos...
# Por eso usamos fuzz.interp_membership exists for!
qual_level_lo = fuzz.interp_membership(x_qual, qual_lo, 8)
qual_level_md = fuzz.interp_membership(x_qual, qual_md, 8)
qual_level_hi = fuzz.interp_membership(x_qual, qual_hi, 8)
serv_level_lo = fuzz.interp_membership(x_serv, serv_lo, 3)
serv_level_md = fuzz.interp_membership(x_serv, serv_md, 3)
serv_level_hi = fuzz.interp_membership(x_serv, serv_hi, 3)



# Ahora tomamos nuestras reglas y las aplicamos. 
# Regla 1 trata sobre mala comida o servicio. 
# El operador "o" significa que tomamos el maximo de ambos.
active_rule1 = np.fmax(qual_level_lo, serv_level_lo)
# Ahora aplicamos esto cortando el minimo de la respectiva
# funcion de membresia con np.fmin
tip_activation_lo = np.fmin(active_rule1, tip_lo) # removed entirely to 0


# Para la regla 2, conectamos servicio aceptable con propina media
tip_activation_md = np.fmin(serv_level_md, tip_md)


# Para la regla 3, conectamos servicio alto o comida deliciosa con propina alta
active_rule3 = np.fmax(qual_level_hi, serv_level_hi)
tip_activation_hi = np.fmin(active_rule3, tip_hi)

# Visualizamos el resultado
tip0 = np.zeros_like(x_tip)
fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.fill_between(x_tip, tip0, tip_activation_lo, facecolor='b', alpha=0.7)
ax0.plot(x_tip, tip_lo, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_tip, tip0, tip_activation_md, facecolor='g', alpha=0.7)
ax0.plot(x_tip, tip_md, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(x_tip, tip0, tip_activation_hi, facecolor='r', alpha=0.7)
ax0.plot(x_tip, tip_hi, 'r', linewidth=0.5, linestyle='--')
ax0.set_title('Actividad de membresia')
# Quitamos los ejes superior y derecho
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()
plt.show()

# Agregamos las 3 funciones de membresia juntas
aggregated = np.fmax(tip_activation_lo, np.fmax(tip_activation_md, tip_activation_hi))
# Calculamos un valor no-difuso (defuzzified)
tip = fuzz.defuzz(x_tip, aggregated, 'centroid')
print("Centroide: ", tip)
tip_activation = fuzz.interp_membership(x_tip, aggregated, tip) # for plot

# Visualizamos el resultado
fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.plot(x_tip, tip_lo, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(x_tip, tip_md, 'g', linewidth=0.5, linestyle='--')
ax0.plot(x_tip, tip_hi, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_tip, tip0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([tip, tip], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Membresias agregadas y resultado (linea)')
# Quitamos los ejes superior y derecho
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()
plt.show()
