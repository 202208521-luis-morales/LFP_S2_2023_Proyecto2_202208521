- Luis Rodrigo Morales Florián
- 202208521
- LABORATORIO LENGUAJES FORMALES Y DE PROGRAMACION Sección B-
- Proyecto 2

# Manual de Usuario
## Interfaz de Usuario
![foto_interfaz](https://res.cloudinary.com/dyin2bpxi/image/upload/v1698447483/2023/Lenguajes%20Formales/Proyecto%202/jt9t9mjy8psijniynibj.png)

La aplicación cuenta con una interfaz gráfica que posee las siguientes características:

 - **Cargar archivo:** Un botón que al presionarlo permita cargar el archivo
   con extensión “bizdata”.  
 - **Área de texto:** Debe tener un área donde se
   pueda visualizar y modificar el código “bizdata”.  
 - **Analizar archivo:** Un botón que analice el código “bizdata”.  
 - **Consola:** Un área de texto que no se pueda editar, solamente visualizar texto generado por las instrucciones dadas por el lenguaje.  
 -  **Reportes:** Un menú que pueda generar los siguientes reportes: 
	 - Reporte de Tokens 
	 - Reporte de Errores 
	 - Árbol de derivación

## Tipos de datos
### Listas de datos
- **Claves:** En esta sección se declaran los claves o campos por los que están
construidos los registros, su estructura está formada por la palabra reservada Claves,
seguido de signo igual, corchete de apertura, lista de claves y corchete de cierre. La lista de claves está formada por cadenas de caracteres encerradas entre comillas y separadas por coma.
- **Registros:** En esta sección se detallan los registros que se quieren analizar y sigue la estructura dada por palabra reservada Registros, signo igual, corchete de apertura, lista de registros y corchete de cierre. Para la lista de registros, cada registro está encerrado entre llave de apertura y llave de cierre y sus valores están separados por comas, estos valores pueden ser cadenas de texto, enteros o decimales.
### Comentarios
- **Comentarios de una línea:** Se representan con un numeral y finalizan con un salto de línea.
- **Comentarios multilínea:** Inicia con tres comillas simples y finaliza con tres comillas simples.
### Instrucciones de Reportería
- imprimir(cadena): Imprime por consola el valor dado por la cadena.
- imprimirln(cadena): Lo mismo que el anterior, pero además agrega un salto de línea
- conteo(): Imprime por consola la cantidad de registros en el arreglo de registros
- promedio(“campo”): Imprime por consola el promedio del campo dado.
- contarsi(“campo”, valor): Imprime por consola la cantidad de registros en la que el campo dado sea igual al valor dado.
- datos(): Imprime por consola los registros leídos.
- sumar(“campo”): Imprime en consola la suma todos los valores del campo dado.
- max(“campo”): Encuentra el valor máximo del campo dado.
- min(“campo”): Encuentra el valor mínimo del campo dado.
- exportarReporte(“titulo”): Genera un archivo html con una tabla en donde se encuentren los registros leídos y con el título como parámetro.