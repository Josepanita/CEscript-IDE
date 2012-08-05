# CEscript
Lenguaje **C** Interpretado, Basado en el proyecto [PicoC] de Zik Saleeba, esta diseñado para iniciar a los estudiantes de programación al uso del razonamiento lógico y al lenguaje de programación.

## Características

1. Sintaxis similar al Lenguaje C Original
2. Palabras Clave, Tipos de dato, Declaraciones del Preprocesador completamente en español
3. Soporte a Punteros, argumentos, inclusión de librerías y cabeceras.

## Instalación

Por ahora solo esta disponible para entornos GNU/Linux, simplemente ejecuta el script ***install.sh***

Debes tener la posibilidad de ejecutar el script como **_root_**, o el uso del comando **sudo** para poder proveer permisos de administrador al instalador de paquetes.

Hasta ahora solo hay soporte para

  - **apt-get** de DEBian/Ubuntu
  - **aptitude** Versiones anteriores de DEBian
  - **yum** de Fedora

## Usando esta herramienta

Luego de la instalación, se creará una carpeta en tu directorio **$HOME** (**/home/*&lt;usuario&gt;*/**) llamado **cescript-ide** 

    | cescript-ide
    | -- bin/
    | -- style/
    | -- syntax/
    | -- cescript-ide

en donde encontraras el ejecutable **cescript-ide**, ejecutalo y listo, la interfaz es bastante intuitiva, ademas de una barra superior que facilita las operaciones con esta herramienta.