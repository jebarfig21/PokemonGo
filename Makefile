.PHONY: all run_cliente_PokemonGo run_servidor_PokemonGo create_manuals_PokemonGo build_PokemonGo manual_servidor_PokemonGo manual_cliente_PokemonGo 

UNAME_S=$(shell uname -s)

all:

	@echo "make run_cliente_PokemonGo"
	@echo "    Ejecuta el cliente de PokemonGo."
	@echo "make run_servidor_PokemonGo"
	@echo "    Ejecuta el servidor de PokemonGo."
	@echo "make create_manuals_PokemonGo"
	@echo "    Crea los manuales del cliente y del servidor."
	@echo "make build_PokemonGo"
	@echo "    Construye el proyecto."
	@echo "make manual_servidor_PokemonGo"
	@echo "    Muestra el manual del servidor de PokemonGo en terminales Linux"
	@echo "make manual_cliente_PokemonGo"
	@echo "    Muestra el manual del cliente de PokemonGo en terminales Linux"
run_cliente_PokemonGo:
	python3 cliente.py

run_servidor_PokemonGo:
	python3 servidor.py

create_manuals_PokemonGo:
	cp man/servidor_PokemonGo.1  /usr/share/man/es/man1/servidor_PokemonGo.1; \
	cp man/cliente_PokemonGo.1 /usr/share/man/es/man1/cliente_PokemonGo.1; \
	echo Creación de manuales completa; \

build_PokemonGo: create_manuals_PokemonGo
	@echo OK

manual_servidor_PokemonGo:
	@man servidor_PokemonGo

manual_cliente_PokemonGo:
	@man cliente_PokemonGo

