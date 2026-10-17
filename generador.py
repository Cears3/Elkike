#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de contraseñas seguras para Termux.
- Personalización de longitud y caracteres.
- Generación individual o múltiple.
- Validación de datos.
- Guardado automático en passwords.txt.
- Utiliza secrets para generar contraseñas seguras.
- Compatible con Python 3, sin dependencias externas.
"""

import secrets
import string
import sys
from pathlib import Path
from datetime import datetime


ARCHIVO = Path(__file__).resolve().parent / "passwords.txt"
SIMBOLOS = "!@#$%&*+-_=.?¿"


def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje).strip())
            if minimo <= numero <= maximo:
                return numero
            print(f"Introduce un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada inválida. Introduce un número entero.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            sys.exit(0)


def preguntar(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí", "n", "no", ""):
            return respuesta not in ("n", "no")
        print("Responde S para sí o N para no.")


def configurar_caracteres():
    print("\n--- Personaliza tu contraseña ---")
    longitud = leer_entero("Longitud (8-128): ", 8, 128)

    grupos = []

    if preguntar("¿Incluir mayúsculas? (S/n): "):
        grupos.append(string.ascii_uppercase)

    if preguntar("¿Incluir minúsculas? (S/n): "):
        grupos.append(string.ascii_lowercase)

    if preguntar("¿Incluir números? (S/n): "):
        grupos.append(string.digits)

    if preguntar("¿Incluir símbolos? (S/n): "):
        grupos.append(SIMBOLOS)

    if not grupos:
        print("Error: selecciona al menos un tipo de carácter.")
        return None, None

    if preguntar("¿Excluir caracteres ambiguos (O, 0, I, l, 1)? (S/n): "):
        ambiguos = "O0Il1"
        grupos = [
            "".join(c for c in grupo if c not in ambiguos)
            for grupo in grupos
        ]
        grupos = [grupo for grupo in grupos if grupo]

    if not grupos:
        print("Error: no quedan caracteres disponibles.")
        return None, None

    if longitud < len(grupos):
        print("Error: longitud insuficiente para las categorías elegidas.")
        return None, None

    return longitud, grupos


def generar_contrasena(longitud, grupos):
    contrasena = [secrets.choice(grupo) for grupo in grupos]
    alfabeto = "".join(grupos)

    while len(contrasena) < longitud:
        contrasena.append(secrets.choice(alfabeto))

    for i in range(len(contrasena) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        contrasena[i], contrasena[j] = contrasena[j], contrasena[i]

    return "".join(contrasena)


def guardar_contrasenas(contrasenas):
    """Guarda automáticamente las contraseñas en el archivo local."""
    try:
        ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

        with ARCHIVO.open("a", encoding="utf-8") as archivo:
            archivo.write(
                f"\n--- Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
            )

            for contrasena in contrasenas:
                archivo.write(contrasena + "\n")

        print(f"\n[OK] Contraseñas guardadas en:\n{ARCHIVO}")

        try:
            ARCHIVO.chmod(0o600)
        except OSError:
            pass

        return True

    except OSError as error:
        print(f"\n[ERROR] No se pudieron guardar las contraseñas: {error}")
        print("Comprueba los permisos de escritura de la carpeta.")
        return False


def generar_varias(longitud, grupos):
    cantidad = leer_entero(
        "¿Cuántas contraseñas deseas generar? (1-50): ",
        1,
        50,
    )

    contrasenas = [
        generar_contrasena(longitud, grupos)
        for _ in range(cantidad)
    ]

    print("\n--- CONTRASEÑAS GENERADAS ---")
    for indice, contrasena in enumerate(contrasenas, start=1):
        print(f"{indice:02d}. {contrasena}")

    guardar_contrasenas(contrasenas)


def mostrar_menu():
    print("\n" + "=" * 40)
    print("   GENERADOR DE CONTRASEÑAS SEGURAS")
    print("=" * 40)
    print("1. Generar una contraseña")
    print("2. Generar varias contraseñas")
    print("3. Mostrar ubicación del archivo")
    print("4. Salir")
    print("-" * 40)


def main():
    while True:
        try:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                longitud, grupos = configurar_caracteres()

                if longitud is not None:
                    contrasena = generar_contrasena(longitud, grupos)
                    print(f"\nTu contraseña:\n{contrasena}")
                    guardar_contrasenas([contrasena])

            elif opcion == "2":
                longitud, grupos = configurar_caracteres()

                if longitud is not None:
                    generar_varias(longitud, grupos)

            elif opcion == "3":
                print(f"\nArchivo de contraseñas:\n{ARCHIVO}")
                print("El archivo se crea automáticamente al guardar.")

            elif opcion == "4":
                print("\n¡Hasta pronto!")
                break

            else:
                print("Opción inválida. Selecciona del 1 al 4.")

        except (EOFError, KeyboardInterrupt):
            print("\n\nPrograma finalizado.")
            break


if __name__ == "__main__":
    main()