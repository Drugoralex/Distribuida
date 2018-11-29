import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
# Generamos el universo de variables
x = np.arange(2, 10, 1)
y = np.arange(4, 12, 1)
z = np.arange(1, 72, 1)

# Generamos las funciones de membresia difusas
x_a1 = fuzz.trimf(x, [2, 5, 8])
x_a2 = fuzz.trimf(x, [3, 6, 9])
y_b1 = fuzz.trimf(y, [5, 8, 11])
y_b2 = fuzz.trimf(y, [4, 7, 10])
z_c1 = fuzz.trimf(z, [1, 4, 7])
z_c2 = fuzz.trimf(z, [3, 6, 9])

def plotMF():
    # Visualisamos estos universos y funciones
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    ax0.plot(x, x_a1, 'b', linewidth=1.5, label='A1')
    ax0.plot(x, x_a2, 'g', linewidth=1.5, label='A2')
    ax0.set_title('Calidad de X')
    ax0.legend()
    ax1.plot(y, y_b1, 'b', linewidth=1.5, label='B1')
    ax1.plot(y, y_b2, 'g', linewidth=1.5, label='B2')
    ax1.set_title('Calidad de Y')
    ax1.legend()
    ax2.plot(z, z_c1, 'b', linewidth=1.5, label='C1')
    ax2.plot(z, z_c2, 'g', linewidth=1.5, label='C2')
    ax2.set_title('Calidad de Z')
    ax2.legend()
    # Quitamos los ejes superior y derecho
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()
    plt.show()


plotMF()


# Necesitamos activar nuestras funciones de membresia en estos valores.
vx=4.0
vy=8.0
x_lev_a1 = fuzz.interp_membership(x, x_a1, vx)
x_lev_a2 = fuzz.interp_membership(x, x_a2, vx)
y_lev_b1 = fuzz.interp_membership(y, y_b1, vy)
y_lev_b2 = fuzz.interp_membership(y, y_b2, vy)


# Ahora tomamos nuestras reglas y las aplicamos. 
# Regla 1 
active_rule1 = np.fmin(x_lev_a1, y_lev_b1)
# Ahora aplicamos esto cortando el minimo de la respectiva
# funcion de membresia con `np.fmin`
z_activation_c1 = np.fmin(active_rule1, z_c1)

# Regla 2
active_rule2 = np.fmin(x_lev_a2, y_lev_b2)
z_activation_c2 = np.fmin(active_rule2, z_c2)


tip0 = np.zeros_like(z)
def plotRules():
    # Visualizamos el resultado
    fig, ax0 = plt.subplots(figsize=(8, 3))
    ax0.fill_between(z, tip0, z_activation_c1, facecolor='b', alpha=0.7)
    ax0.plot(z, z_c1, 'b', linewidth=0.5, linestyle='--', )
    ax0.fill_between(z, tip0, z_activation_c2, facecolor='g', alpha=0.7)
    ax0.plot(z, z_c2, 'g', linewidth=0.5, linestyle='--')
    ax0.set_title('Actividad de membresia')
    # Quitamos los ejes superior y derecho
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()
    plt.show();


plotRules()

# Agregamos las 2 funciones de membresia juntas
aggregated = np.fmax(z_activation_c1,z_activation_c2)
# Calculamos un valor no-difuso (defuzzified)
tip = fuzz.defuzz(z, aggregated, 'centroid')
print("Centroide: ", tip)
tip_activation = fuzz.interp_membership(z, aggregated, tip) # for plot

def plotDefuzz():
    # Visualizamos el resultado
    fig, ax0 = plt.subplots(figsize=(8, 3))
    ax0.plot(z, z_c1, 'b', linewidth=0.5, linestyle='--', )
    ax0.plot(z, z_c2, 'g', linewidth=0.5, linestyle='--')
    ax0.fill_between(z, tip0, aggregated, facecolor='Orange', alpha=0.7)
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

plotDefuzz()


