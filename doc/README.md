# Uso de la aplicación

Una vez el servidor esté corriendo, abrir una **terminal** y dirigirse donde se encuentra el archivo **client.py**.

Para conectarnos al servidor y realizar una petición, antes debe crear un usuario. Mediante este comando `python3 client.py user pwd` se registrará en el servidor el usuario que indiquen, junto con su contraseña, en caso de ya existir un usuario con ese nombre, el **servidor** indicará que la contraseña es incorrecta.

Los argumentos ***user***  y ***pwd*** son posicionales, por lo tanto es necesario que se utilicen cada vez que se ejecuta un comando en la terminal.

A continuación se listan las opciones para ejecutar cada petición:

- **-f o --file**: Se utiliza para enviar uno o más archivos al servidor. Luego de la opcion se deben indicar los nombres de los archivos separados por un espacio.
- **-l o --list**: Solicita al servidor un listado de los archivos disponibles. No requiere un argumento luego de la opción
- **-d o --download**: Se utiliza para solicitar al servidor descargar un archivo, debe indicarse el nombre del archivo como está almacenado en el servidor luego de la opción
- **-r o --remove**: Solicita al servidor la eliminación del archivo especificado luego del *flag*
- **-m o --modify**: **SOLO ADMIN**. Esta es una opcion disponible unicamente para el usuario *admin*, le permite al administrador enviar un usuario y un número de 4 bits con el cual va a indicar el nivel de permisos del usuario. Esquema de permisos: 1º bit: listar, 2º bit: enviar, 3º bit: descargar, 4ºbit  eliminar.
Ejemplo: `python3 client.py admin root bruno 1010` en este ejemplo el adminstrador le está concediendo permisos al usuario ***bruno*** de **listar** archivos y **descargar** archivos, ya que seteo los bits en las posiciones **1** y **3** como **uno** (**True**) mientras que los bits en las posiciones **2** y **4** son **cero**, es decir, que el usuario no dispone de permisos para **enviar** ni para **eliminar** archivos. (**Por defecto, cuando se crea un usuario su nivel de permisos es 1000**)
## Arquitectura del proyecto

![Arquitectura del proyecto](/esquema.png)

