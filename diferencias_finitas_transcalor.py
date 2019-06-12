import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#constantes
miu=1.562*10**(-5)
prandtl=0.7296
k_aire=0.02551
k_agua=0.613
cp=4186
rho=1000
mu=0.855*10**(-3)

#temp
base=0.4 #metros
alto=0.4 #metros
largo= 1 #metros
nodos= 40
delta=base/nodos

#generacion de calor
coordenada_sup_derecha = [0.25,0.15]
coordenada_sup_izquierda = [0.25,0.05]
coordenada_inf_derecha = [0.3,0.15]
coordenada_inf_izquierda = [0.3,0.05]

#refrigerante
a_s=0.015
t_r=40

#maquina de calor
calor_1=50000
k_1=100
t_inf=1
v_inf=10
base_refri=np.sqrt(a_s)

#paramentros de diseño
caudal=0.2 #al interior del canal de refrigeracion l/cm^3
h_r=3000 #refrigeracion
h_e=100 #exterior
t_max=300 #en los bordes del Q generado

#generacion de la matriz
temp = np.zeros((nodos+2,nodos+2))

#condiciones de borde solo se usa como un referente
#for i in range (len(temp)):
#    temp[0][i]=t_inf
#    temp[i][len(temp)-1]=t_inf

#maxima temperatura al interior del generador de calor solo se usa como un referente
#for i in range (int(0.1/delta-1)):
    #n=26+i
    #for j in range (int(0.1/delta-1)):
        #m=6+j
        #temp[n][m]=t_max

#solucion
for i in range(2000):
    #cambios de temperatura en borde de la generacion de calor
    for a in range (int(0.1/delta-1)):
        n=25+a
        for b in range (int(0.1/delta-1)):
            m=5+b
            temp[n][m]=((2*temp[n][m-1]+temp[n+1][m]+temp[n-1][m])+(2*calor_1*delta/k_1))/4

    #cambio de temperatura en los bordes del refrigerante
    for a in range (int(base_refri/delta-1)):
        n=16+a
        for b in range (int(base_refri/delta-1)):
            m=16+b
            temp[n][m]=((2*temp[n][m-1]+temp[n+1][m]+temp[n-1][m])+(2*h_r*delta*t_r/k_1))/(2*((h_r*delta/k_1)+(2)))

    # borde derecho
    for n in range (len(temp)-1):
        temp[n][len(temp)-1]=((2*temp[n][m-1]+temp[n+1][m]+temp[n-1][m])+(2*h_e*delta*t_inf/k_1))/(2*((h_r*delta/k_1)+(2)))

    #borde superior
    for n in range (len(temp)-1):
        temp[0][n]=((temp[n][m-1]+temp[n+1][m]+2*temp[n-1][m])+(2*h_e*delta*t_inf/k_1))/(2*((h_r*delta/k_1)+(2)))

    #cambios de temperatura en nodos interiores
    for n in range (1,int(len(temp)-1)):
        for m in range (1,int(len(temp)-1)):
            temp[n][m]=(temp[n][m+1]+temp[n][m-1]+temp[n+1][m]+temp[n-1][m])/4

    #actualizacion de la temperatura en los nodos aislados
    for n in range (len(temp)):
        temp[n][0]=temp[n][1]
        temp[len(temp)-1][n]=temp[len(temp)-2][n]

#calculo de los calores en los bordes
#borde derecho
calor_derecho=np.zeros(len(temp))
for n in range (len(temp)-1):
    calor_derecho[n]=(4*temp[n][len(temp)-1]-(2*temp[n][m-1]+temp[n+1][m]+temp[n-1][m]))*k_1/(2*delta)

#borde superior
calor_superior=np.zeros(len(temp))
for n in range (len(temp)-1):
    calor_superior[n]=(4*temp[n][len(temp)-1]-(temp[n][m-1]+temp[n+1][m]+2*temp[n-1][m]))*k_1/(2*delta)

#medias calores
calor_derecho=np.mean(calor_derecho)
calor_derecho=np.abs(calor_derecho)
calor_superior=np.mean(calor_superior)
calor_superior=np.abs(calor_superior)

#calculo de los hs en los bordes
reynolds=v_inf*delta/miu
he=((k_aire*0.3387*(prandtl**(1/3))*np.sqrt(reynolds))/((1+((0.0468/prandtl)**(2/3)))**(1/4)))
hr=0.023*(k_agua**(2/3))*(cp**(1/3))*(rho**(4/5))*(mu**(-7/15))*((caudal/a_s)**(4/5))

#temp medias
media=np.mean(temp)

#graficas
x_plot=np.arange(0,base+0.02,delta)
y_plot=np.arange(0,base+0.02,delta)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x_plot, y_plot)
#zs = np.array(np.ravel(t))
#Z = zs.reshape(X.shape)

surf = ax.plot_surface(X, -Y, temp)

ax.set_xlabel('distancia en x ($m$)')
ax.set_ylabel('distancia en y ($m$)')
ax.set_zlabel('Temperatura ºC')
plt.title('grafico3d_')
plt.tight_layout()
plt.savefig('temperatura_.pdf')
plt.show()

plt.contourf(X,-Y,temp,alpha=1,cmap=cm.coolwarm)
plt.colorbar()
plt.title('lineas de contorno_')
plt.xlabel('distancia en x ($m$)')
plt.ylabel('distancia en y ($m$)')
plt.tight_layout()
plt.savefig('lineas de contorno_.pdf')
plt.show()
