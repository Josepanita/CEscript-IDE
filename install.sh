#!/bin/bash
ERROR[0]="No se pudo actualizar el repositorio"
ERROR[1]="No se pudo instalar GTKSourceView2"
ERROR[2]="No se pudo instalar VTE"
ERROR[3]="No se pudo instalar el editor"

COMMAND="apt-get"
SUDO="sudo"
echo "Instalador CEscript..."

if [ "$(id -u)" != "0" ]; then
	echo "Este script debe ejecutarse como root, revisando la existencia del comando sudo."
	
	hash $SUDO 2>/dev/null || { echo >&2 "Se requiere el comando \"sudo\" para poder instalar paquetes."; exit 1; }

	hash $COMMAND 2>/dev/null || { COMMAND="aptitude"; "Se requiere el comando \"apt-get\" para poder instalar paquetes, buscando \"aptitude\".";}

	hash $COMMAND 2>/dev/null || { COMMAND="yum"; "Se requiere el comando \"apt-get\" o \"aptitude\" para poder instalar paquetes, buscando \"yum\""; }

	hash $COMMAND 2>/dev/null || { "Se requiere el comando \"apt-get\" o \"aptitude\" o \"yum\" para poder instalar paquetes."; exit 1; }

else
	SUDO=""
fi

echo "Actualizando los Repositorios..."

$SUDO $COMMAND update

status[0]=$?

echo "Instalando los modulos GTK+ necesarios"

echo "Instalando GTKSourceView2..."

$SUDO $COMMAND install libgtksourceview2.0-dev python-gtksourceview2 libgtksourceview2.0-doc

status[1]=$?

echo "Instalando VTE..."

$SUDO $COMMAND install libvte-common libvte-dev libvte-doc python-vte

status[2]=$?

echo "Instalando el Editor..."

cp -r "./cescript-ide/" "$HOME/cescript-ide/"

#cp "./bin/cescript-ide" "/usr/bin/"

status[3]=$?

for (( i = 0; i < 5; i++ )); do
	if [[ ${status[i]} != 0 ]]; then
		echo ${ERROR[i]}
	fi
done