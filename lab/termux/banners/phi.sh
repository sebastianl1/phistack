#!/data/data/com.termux/files/usr/bin/bash

Y='\e[0;33m' C='\e[0;36m' G='\e[0;32m'
M='\e[0;35m' R='\e[0;31m' B='\e[0;34m'
W='\e[1;37m' N='\e[0m'

show() {
  echo ""
  echo -e "  ${Y}$1${N}"
  echo -e "  ${C}$2${N}"
  echo -e "  ${M}$3${N}"
  [ -n "$4" ] && echo -e "  ${M}$4${N}"
  echo ""
}

show_mol() {
  echo ""
  echo -e "  ${Y}$1${N}"
  echo -e "$2"
  echo -e "  ${M}$3${N}"
  [ -n "$4" ] && echo -e "  ${M}$4${N}"
  echo ""
}

METHANE=$'        H\n        |\n  H \u2014 C \u2014 H\n        |\n        H'
ETHANOL=$'   H   H\n   |   |\n   H - C - C - O - H\n   |   |\n   H   H'
BENZENE=$'        H\n         \\\n          C \u2014 H\n         / \\\n    H \u2014 C   C \u2014 H\n        |   |\n    H \u2014 C   C \u2014 H\n         \\ /\n          C \u2014 H\n         /\n        H'
CHLOROFORM=$'        Cl\n         |\n  H \u2014 C \u2014 Cl\n         |\n        Cl'
WATER=$'    O\n   / \\\n  H   H'
CO2=$'  O = C = O'
AMMONIA=$'    H\n    |\n  H \u2014 N \u2014 H'
METHANOL=$'    H\n    |\n  H \u2014 C \u2014 O \u2014 H\n    |\n    H'
ACETIC=$'  H   O\n  |   \u2016\n  H \u2014 C \u2014 C \u2014 O \u2014 H\n  |\n  H'
SULFURIC=$'    O\n    \u2016\n  O = S \u2014 O \u2014 H\n    |\n    O \u2014 H'

pick=$((RANDOM % 82))
case $pick in
   0) show "Teorema Fundamental del Calculo" "\u222b\u2090\u1d47 f(x) dx = F(b) \u2212 F(a)" \
          "Relaciona la derivada con la integral definida." \
          "Si F'(x) = f(x), entonces el area bajo f(x) entre a y b es F(b)\u2212F(a)." ;;
   1) show "Identidad de Euler" "e^(i\u03c0) + 1 = 0" \
          "Conecta cinco constantes fundamentales: e, i, \u03c0, 1 y 0." \
          "Considerada la ecuacion mas hermosa de la matematica." ;;
   2) show "Teorema de Pitagoras" "a\u00b2 + b\u00b2 = c\u00b2" \
          "En un triangulo rectangulo, el cuadrado de la hipotenusa" \
          "es igual a la suma de los cuadrados de los catetos." ;;
   3) show "Formula Cuadratica" "x = (\u2212b \u00b1 \u221a(b\u00b2\u22124ac)) / 2a" \
          "Resuelve ecuaciones de la forma ax\u00b2 + bx + c = 0." \
          "El discriminante b\u00b2\u22124ac determina la naturaleza de las raices." ;;
   4) show "Serie de Taylor" "f(x) = \u03a3 f\u207f(a)(x\u2212a)\u207f / n!" \
          "Aproxima cualquier funcion suave mediante polinomios." \
          "Permite calcular funciones complejas usando solo operaciones basicas." ;;
   5) show "Transformada de Fourier" "F(\u03c9) = \u222b f(t) e^(\u2212i\u03c9t) dt" \
          "Descompone una senal temporal en sus componentes frecuenciales." \
          "Fundamental en procesamiento de senales, audio e imagenes." ;;
   6) show "Ecuacion de Laplace" "\u2207\u00b2\u03c6 = 0" \
          "Describe potenciales en regiones sin fuentes." \
          "Gobierna campos electricos, gravitatorios y flujo de fluidos ideales." ;;
   7) show "Teorema de Bayes" "P(A|B) = P(B|A) P(A) / P(B)" \
          "Actualiza la probabilidad de una hipotesis ante nueva evidencia." \
          "Pilar de la inferencia estadistica y el aprendizaje automatico." ;;
   8) show "Numero Aureo" "\u03c6 = (1+\u221a5)/2 \u2248 1.618" \
          "Proporcion que aparece en la naturaleza, el arte y la arquitectura." \
          "Relacionado con la sucesion de Fibonacci y el rectangulo armonico." ;;
   9) show "Ley de Gravitacion Universal" "F = G m\u2081m\u2082 / r\u00b2" \
          "Toda masa atrae a otra con una fuerza proporcional al producto" \
          "de sus masas e inversamente proporcional al cuadrado de la distancia." ;;
  10) show "Segunda Ley de Newton" "F = ma" \
          "La fuerza neta aplicada a un cuerpo es igual a su masa" \
          "multiplicada por la aceleracion que experimenta." ;;
  11) show "Ley de Hooke" "F = \u2212kx" \
          "La fuerza necesaria para deformar un resorte es proporcional" \
          "a la distancia que se estira o comprime desde su posicion natural." ;;
  12) show "Ley de Coulomb" "F = k\u2091 |q\u2081q\u2082| / r\u00b2" \
          "La fuerza electrica entre dos cargas puntuales es proporcional" \
          "al producto de las cargas e inversa al cuadrado de la distancia." ;;
  13) show "Ley de Ohm" "V = IR" \
          "La diferencia de potencial entre los extremos de un conductor" \
          "es igual al producto de la corriente por la resistencia." ;;
  14) show "Ley del Gas Ideal" "PV = nRT" \
          "Relaciona presion, volumen, temperatura y cantidad de sustancia" \
          "de un gas ideal. R = 0.08206 L\u00b7atm/mol\u00b7K." ;;
  15) show "Conservacion de la Energia" "E\u2080 = E\u2092" \
          "La energia total de un sistema aislado permanece constante." \
          "No se crea ni se destruye, solo se transforma entre formas." ;;
  16) show "Energia Cinetica" "K = \u00bdmv\u00b2" \
          "Energia que posee un objeto debido a su movimiento." \
          "Depende de la masa y del cuadrado de la velocidad." ;;
  17) show "Ley de Snell" "n\u2081 sen \u03b8\u2081 = n\u2082 sen \u03b8\u2082" \
          "Describe como se refracta la luz al pasar de un medio a otro." \
          "El angulo de desviacion depende de los indices de refraccion." ;;
  18) show "Periodo del Pendulo" "T = 2\u03c0 \u221a(L/g)" \
          "El tiempo que tarda un pendulo en completar una oscilacion" \
          "depende de la longitud de la cuerda y de la gravedad." ;;
  19) show "Ecuaciones de Maxwell" "\u2207\u00d7E = \u2212\u2202B/\u2202t" \
          "Unifican la electricidad y el magnetismo en una sola teoria." \
          "Predicen ondas electromagneticas viajando a la velocidad de la luz." ;;
  20) show "Ecuacion de Schrodinger" "i\u210f \u2202\u03c8/\u2202t = \u0124\u03c8" \
          "Describe como evoluciona el estado cuantico de un sistema." \
          "Fundamental en la mecanica cuantica y la quimica molecular." ;;
  21) show "Relatividad Especial" "E = mc\u00b2" \
          "La energia y la masa son equivalentes." \
          "Una pequena cantidad de masa contiene una enorme cantidad de energia." ;;
  22) show "Ecuacion de Onda" "\u2202\u00b2u/\u2202t\u00b2 = c\u00b2 \u2202\u00b2u/\u2202x\u00b2" \
          "Describe ondas que viajan a velocidad c en un medio." \
          "Aplica a ondas sonoras, sismicas y ondas en cuerdas." ;;
  23) show "Ecuacion de Calor" "\u2202u/\u2202t = \u03b1 \u2202\u00b2u/\u2202x\u00b2" \
          "Modela como se difunde el calor a traves de un material." \
          "La temperatura tiende a equilibrarse con el tiempo." ;;
  24) show "Principio de Incertidumbre" "\u0394x \u00b7 \u0394p \u2265 \u210f/2" \
          "Es imposible conocer simultaneamente la posicion y el momento" \
          "de una particula con precision arbitraria." ;;
  25) show "Ecuacion de Friedmann" "H\u00b2 = (8\u03c0G/3)\u03c1 \u2212 kc\u00b2/a\u00b2" \
          "Describe la expansion del universo en cosmologia." \
          "Relaciona la tasa de expansion con la densidad de energia." ;;
  26) show "Ley de Stefan-Boltzmann" "P = \u03c3 A T\u2074" \
          "La potencia radiada por un cuerpo negro es proporcional" \
          "a la cuarta potencia de su temperatura absoluta." ;;
  27) show "Ecuacion de Bernoulli" "P + \u00bd\u03c1v\u00b2 + \u03c1gh = cte" \
          "A lo largo de una linea de corriente, la suma de la presion," \
          "la energia cinetica y la potencial gravitatoria permanece constante." ;;
  28) show "Ley de Gauss" "\u2207\u00b7E = \u03c1/\u03b5\u2080" \
          "El flujo electrico neto a traves de una superficie cerrada" \
          "es igual a la carga encerrada dividida por la permitividad." ;;
  29) show "Fuerza de Lorentz" "F = q(E + v\u00d7B)" \
          "Fuerza total sobre una particula cargada en movimiento" \
          "dentro de campos electricos y magneticos." ;;
  30) show "Ley de Faraday" "\u03b5 = \u2212d\u03a6/dt" \
          "Un campo magnetico variable en el tiempo induce una fuerza" \
          "electromotriz en un circuito. Base de generadores electricos." ;;
  31) show "Numero de Avogadro" "N\u2090 = 6.022\u00d710\u00b2\u00b3 mol\u207b\u00b9" \
          "Numero de atomos o moleculas en un mol de sustancia." \
          "Permite relacionar el mundo microscopico con el macroscopico." ;;
  32) show "Ecuacion de Arrhenius" "k = A e^(\u2212E\u2090/RT)" \
          "La velocidad de una reaccion quimica aumenta con la temperatura" \
          "y disminuye con la energia de activacion." ;;
  33) show "Ecuacion de Nernst" "E = E\u00b0 \u2212 (RT/nF) ln Q" \
          "Relaciona el potencial de una celda electroquimica" \
          "con las concentraciones de las especies involucradas." ;;
  34) show "Ley de Beer-Lambert" "A = \u03b5 c l" \
          "La absorbancia de una solucion es proporcional a la concentracion" \
          "del absorbente y a la longitud del paso optico." ;;
  35) show "Ecuacion de Henderson-Hasselbalch" "pH = pK\u2090 + log([A\u207b]/[HA])" \
          "Relaciona el pH de una solucion buffer con el pK\u2090 del acido" \
          "y la relacion entre la base conjugada y el acido debil." ;;
  36) show "Numero de Reynolds" "Re = \u03c1 v L / \u03bc" \
          "Cuantifica si un flujo es laminar (Re << 2000) o turbulento (Re >> 4000)." \
          "Depende de la densidad, velocidad, longitud caracteristica y viscosidad." ;;
  37) show "Ley de Enfriamiento de Newton" "dT/dt = \u2212k(T\u2212T\u2090)" \
          "La velocidad de enfriamiento de un cuerpo es proporcional" \
          "a la diferencia de temperatura entre el cuerpo y el ambiente." ;;
  38) show "Eficiencia Termica" "\u03b7 = 1 \u2212 T_C / T_H" \
          "Rendimiento maximo teorico de una maquina termica entre dos focos." \
          "Ninguna maquina puede superar la eficiencia de Carnot." ;;
  39) show "Puente de Wheatstone" "R\u2093 = R\u2082R\u2083/R\u2081" \
          "Circuito para medir resistencias desconocidas con precision." \
          "Se equilibra ajustando R\u2081 hasta que el voltaje entre los nodos sea cero." ;;
  40) show "Esfuerzo de von Mises" "\u03c3_v = \u221a(\u03c3\u2081\u00b2\u2212\u03c3\u2081\u03c3\u2082+\u03c3\u2082\u00b2)" \
          "Criterio de fluencia para materiales ductiles." \
          "La falla ocurre cuando \u03c3_v supera el limite elastico del material." ;;
  41) show "Factor de Seguridad" "FS = S_resistencia / S_aplicado" \
          "Relacion entre la resistencia maxima de un componente" \
          "y el esfuerzo maximo esperado en servicio." ;;
  42) show "Ley de Hooke Generalizada" "\u03b5 = \u03c3 / E" \
          "La deformacion unitaria es proporcional al esfuerzo aplicado," \
          "donde E es el modulo de Young del material." ;;
  43) show "Ecuacion de Euler-Lagrange" "d/dt(\u2202L/\u2202q\u0307) \u2212 \u2202L/\u2202q = 0" \
          "Ecuacion fundamental de la mecanica lagrangiana." \
          "Describe la dinamica del sistema en terminos de energia." ;;
  44) show "Geodesica en Relatividad" "d\u00b2x\u1d43/d\u03c4\u00b2 = 0" \
          "En el espacio-tiempo curvo, los objetos siguen geodesicas." \
          "La gravedad no es una fuerza sino curvatura del espacio-tiempo." ;;
  45) show "Ecuacion de Drake" "N = R\u207a \u00d7 f\u209a \u00d7 n\u2092 \u00d7 f\u2113 \u00d7 f\u1d62 \u00d7 f\u1d04 \u00d7 L" \
          "Estima el numero de civilizaciones extraterrestres detectables." \
          "Considera la tasa de formacion estelar y la probabilidad de vida." ;;
  46) show_mol "Metano  \u2022  CH\u2084" "$METHANE" \
          "Principal componente del gas natural." \
          "Es un hidrocarburo alcano de formula CH\u2084, incoloro e inodoro." ;;
  47) show_mol "Etanol  \u2022  C\u2082H\u2085OH" "$ETHANOL" \
          "Alcohol primario de formula C\u2082H\u2085OH." \
          "Presente en bebidas alcoholicas y usado como biocombustible." ;;
  48) show_mol "Benceno  \u2022  C\u2086H\u2086" "$BENZENE" \
          "Hidrocarburo aromatico con estructura resonante." \
          "Sus electrones pi estan deslocalizados en el anillo hexagonal." ;;
  49) show_mol "Cloroformo  \u2022  CHCl\u2083" "$CHLOROFORM" \
          "Compuesto halogenado, triclorometano." \
          "Historicamente usado como anestesico inhalatorio." ;;
  50) show "Ecuacion de Dirac" "(i\u03b3\u1d43\u2202\u2093 \u2212 m)\u03c8 = 0" \
          "Unifica la mecanica cuantica con la relatividad especial." \
          "Predice la existencia de antimateria." ;;
  51) show "Constante Cosmologica" "R\u1d43\u03bd \u2212 \u00bdRg\u1d43\u03bd + \u039bg\u1d43\u03bd = (8\u03c0G/c\u2074)T\u1d43\u03bd" \
          "Termino que representa la energia oscura en relatividad general." \
          "Explica la expansion acelerada del universo." ;;
  52) show "Ecuacion de Euler-Bernoulli" "d\u00b2/dx\u00b2(EI d\u00b2y/dx\u00b2) = q(x)" \
          "Describe la deflexion de vigas bajo carga transversal." \
          "Fundamental en el diseno estructural de edificios y puentes." ;;
  53) show "Ecuacion de Darcy-Weisbach" "h_f = f L v\u00b2 / (2Dg)" \
          "Calcula la perdida de carga por friccion en tuberias." \
          "El factor de friccion f depende del numero de Reynolds." ;;
  54) show "Ley de Fourier de Conduccion" "q = \u2212k A dT/dx" \
          "El flujo de calor por conduccion es proporcional al gradiente" \
          "de temperatura y al area transversal, con k la conductividad." ;;
  55) show "Primera Ley de la Termodinamica" "\u0394U = Q \u2212 W" \
          "El cambio de energia interna de un sistema es igual al calor" \
          "absorbido menos el trabajo realizado por el sistema." ;;
  56) show "Segunda Ley de la Termodinamica" "\u0394S \u2265 0" \
          "La entropia del universo siempre aumenta en procesos reales." \
          "Define la direccion de los procesos termodinamicos." ;;
  57) show "Ley de Pascal" "\u0394P = F/A" \
          "La presion aplicada a un fluido incompresible se transmite" \
          "por igual en todas las direcciones dentro del fluido." ;;
  58) show "Principio de Arquimedes" "E = \u03c1\u2092gV\u209b" \
          "Todo cuerpo sumergido experimenta un empuje hacia arriba" \
          "igual al peso del volumen de fluido desalojado." ;;
  59) show "Ecuacion de Manning" "V = (1/n) R_h^\u00b2\u2044\u00b3 S^\u00b9\u2044\u00b2" \
          "Calcula la velocidad del flujo en canales abiertos." \
          "n es el coeficiente de rugosidad y R_h el radio hidraulico." ;;
  60) show "Ley de Fick" "J = \u2212D dC/dx" \
          "El flujo de particulas por difusion es proporcional" \
          "al gradiente de concentracion y al coeficiente de difusion." ;;
  61) show "Circulo de Mohr" "\u03c3_n = (\u03c3_x+\u03c3_y)/2 + (\u03c3_x\u2212\u03c3_y)/2 cos 2\u03b8" \
          "Representacion grafica de esfuerzos en un punto de un material." \
          "Permite encontrar esfuerzos principales y maximos cortantes." ;;
  62) show "Teorema de Torricelli" "v = \u221a(2gh)" \
          "La velocidad de salida de un fluido por un orificio" \
          "es igual a la de caida libre desde la superficie del liquido." ;;
   63) show "Ley de Gauss para Magnetismo" "\u2207\u00b7B = 0" \
          "El flujo magnetico neto a traves de cualquier superficie" \
          "cerrada es cero. No existen monopolos magneticos." ;;
   64) show_mol "Agua  \u2022  H\u2082O" "$WATER" \
          "Molecula polar con geometria angular." \
          "Solvente universal, esencial para la vida en la Tierra." ;;
   65) show_mol "Dioxido de Carbono  \u2022  CO\u2082" "$CO2" \
          "Gas de efecto invernadero, lineal y apolar." \
          "Producto de la respiracion y la combustion de combustibles." ;;
   66) show_mol "Amoniaco  \u2022  NH\u2083" "$AMMONIA" \
          "Gas incoloro con geometria piramidal trigonal." \
          "Usado en fertilizantes, productos de limpieza y refrigeracion." ;;
   67) show_mol "Metanol  \u2022  CH\u2083OH" "$METHANOL" \
          "Alcohol primario simple, toxico para los humanos." \
          "Usado como combustible y disolvente industrial." ;;
   68) show_mol "Acido Acetico  \u2022  CH\u2083COOH" "$ACETIC" \
          "Acido carboxilico, componente principal del vinagre." \
          "Usado en la industria quimica y alimentaria." ;;
   69) show_mol "Acido Sulfurico  \u2022  H\u2082SO\u2084" "$SULFURIC" \
          "Acido fuerte y corrosivo, produccion masiva mundial." \
          "Usado en baterias, fertilizantes y refinacion de petroleo." ;;
   70) show "Estructura de Lewis" "Representa electrones de valencia" \
          "Muestra como se enlazan los atomos en una molecula." \
          "Los electrones se representan como puntos alrededor del simbolo." ;;
   71) show "Regla del Octeto" "Los atomos tienden a completar 8 electrones" \
          "en su capa de valencia para alcanzar estabilidad." \
          "Explica la formacion de enlaces ionicos y covalentes." ;;
   72) show "Numero de Oxidacion" "Carga formal de un atomo en un compuesto" \
          "Indica cuantos electrones ha ganado o perdido." \
          "Fundamental para balancear reacciones redox." ;;
   73) show "Ley de las Proporciones Definidas" "Un compuesto siempre tiene la" \
          "misma proporcion en masa de sus elementos constituyentes." \
          "Ejemplo: el agua siempre es 11.19% H y 88.81% O en masa." ;;
   74) show "Enlace Ionico" "Transferencia de electrones entre un metal" \
          "y un no metal, formando iones con cargas opuestas." \
          "Ejemplo: NaCl (cloruro de sodio, sal de mesa)." ;;
   75) show "Enlace Covalente" "Comparticion de pares de electrones" \
          "entre atomos no metalicos." \
          "Puede ser simple, doble o triple segun los pares compartidos." ;;
   76) show "Puente de Hidrogeno" "Interaccion entre un H polarizado" \
          "positivamente y un atomo electronegativo (O, N, F)." \
          "Responsable de las propiedades unicas del agua." ;;
   77) show "Catalisis" "Un catalizador acelera una reaccion quimica" \
          "sin consumirse en el proceso." \
          "Disminuye la energia de activacion de la reaccion." ;;
   78) show "Polimerizacion" "Union de moleculas pequenas (monomeros)" \
          "para formar cadenas largas (polimeros)." \
          "Ejemplos: polietileno, nylon, ADN, proteinas." ;;
   79) show "Enlace Metalico" "Nube de electrones deslocalizados" \
          "rodeando cationes metalicos en una red cristalina." \
          "Explica la conductividad electrica y la maleabilidad de los metales." ;;
   80) show "Electrolisis" "Descomposicion de un compuesto mediante" \
          "corriente electrica. Ejemplo: 2H\u2082O \u2192 2H\u2082 + O\u2082." \
          "Usada para producir metales y gases puros industrialmente." ;;
   81) show "pH y pOH" "pH = \u2212log[H\u207a],  pOH = \u2212log[OH\u207b]" \
          "El pH mide la acidez de una solucion en escala 0\u201314." \
          "pH 7 es neutro, menor es acido, mayor es basico." ;;
esac
