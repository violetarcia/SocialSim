import procesos as pr
import datos as dat
import principal as pri
import simulaciones as sim

# Funcion de visitas por segmento, ejemplo del segmento A (un periodo)
''' Parametros: 
        Numero de canales: Facebook y Iteso
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por segmentos
        Personas que visitaron en el tiempo t-1'''

# Numero de canales
n_canales_A = len(dat.param_beta)
n_canales_B = len(dat.param_beta)
# Personas de alcance por canal de facebook
p_canal_facebook_A = int((dat.publicidad_A / dat.cpm_A)* 1000)
p_canal_facebook_B = int((dat.publicidad_B / dat.cpm_B)* 1000)
# Personas de alcance por canal de iteso
p_canal_iteso_A = dat.segmento_A
p_canal_iteso_B = dat.segmento_B

# 3 resultados: numero de personas que visitan, compran y regresan
v, c, r = pr.f_visitas_segmento(n_canales_A, dat.param_beta, [p_canal_facebook_A, p_canal_iteso_A, dat.segmento_C], [0,0,0])
#print(v, c, r)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Funcion de serie de tiempo de visitas

''' Parametros: 
        Numero de periodos de la serie de tiempo
        Numero de canales: Facebook y Iteso
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por segmentos
        Personas que visitaron en el tiempo t-1'''

# Periodos a simular
t = 18
# Resultado de datos visita: [Visitas, Compras, Regresan]
datos_visita_A = pr.f_serie_tiempo_visitan(t, n_canales_A, dat.param_beta, [p_canal_facebook_A, p_canal_iteso_A])
datos_visita_B = pr.f_serie_tiempo_visitan(t, n_canales_B, dat.param_beta, [p_canal_facebook_B, p_canal_iteso_B])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion de ventas por cada persona
''' Parametros: 
        Matriz de posibles combinaciones (funcion en simulaciones: f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''

ingreso, utilidad, ventas, costos, horas = pr.f_ventas_persona(pri.m_bin_comb, pri.v_prob_comb, pri.v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h)
#print(ingreso, utilidad, ventas, costos)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion que da las compras del periodo de todas las personas

''' Parametros:
        Numero de personas en el periodo de tiempo actual,  que se repetira la funcion anterior
        Matriz de posibles combinaciones (funcion en simulaciones: f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''

ing_ut_ven_cos = pr.f_periodo_ventas(c, pri.m_bin_comb, pri.v_prob_comb, pri.v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Funcion para vector de probabilidades de acompañantes del sector A

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

param_v_sector_A_prob_acom = sim.f_prob_cantidad(dat.n_acomp_A, 'beta', dat.param_acomp_A)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para los acompañantes del sector en un periodo

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

acompañ_A = sim.f_acompañantes_periodo(param_v_sector_A_prob_acom, int(datos_visita_A[0][0]), dat.min_acomp_A)
#print(acompañ_A)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para la cantidad de personas que utilizarian el baño

''' Parametros: 
        Porcentaje que usaría
        Personas del segmento
        Personas que acompañan a las personas del segmento'''

personas_baños = pr.f_prob_binomial(dat.porcentaje_baño, int(datos_visita_A[0][0]), acompañ_A)
#print(personas_baños)
costo_baños = personas_baños*dat.baño_insumo_c

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para la cantidad de personas que irian a los talleres

''' Parametros: 
        Porcentaje que usaría
        Personas del segmento
        Personas que acompañan a las personas del segmento'''

personas_taller = pr.f_prob_binomial(dat.porcentaje_taller_A, int(datos_visita_A[0][0]), acompañ_A)
#print(personas_baños)
costo_taller = personas_taller*dat.taller_insumo_c + dat.taller_fijo_c

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -