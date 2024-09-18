import csv
from auto import Auto
from cliente import Cliente
from compra import Compra

# Variables globales
autos_registrados = []
clientes_registrados = []
compras_realizadas = []

# Funciones de guardado y carga de datos
def guardar_autos():
    with open('data/autos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for auto in autos_registrados:
            writer.writerow([auto.placa, auto.marca, auto.modelo, auto.descripcion, auto.precio_unitario, auto.disponible])

def guardar_clientes():
    with open('data/clientes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for cliente in clientes_registrados:
            writer.writerow([cliente.nombre, cliente.correo, cliente.nit])

def guardar_compras():
    with open('data/compras.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for compra in compras_realizadas:
            autos_comprados_str = ";".join([auto.placa for auto in compra.autos])
            writer.writerow([compra.cliente.nit, autos_comprados_str, compra.costo_total])

def cargar_autos():
    global autos_registrados
    with open('data/autos.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 6:  # Verificar que la fila este en el formato correcto
                placa, marca, modelo, descripcion, precio_unitario, disponible = row
                auto = Auto(placa, marca, modelo, descripcion, float(precio_unitario))
                auto.disponible = disponible == 'True'
                autos_registrados.append(auto)
            elif len(row) == 0:  # Saltar filas vacías
                continue
            else:
                print(f"Fila ignorada (número incorrecto de columnas): {row}")

def cargar_clientes():
    global clientes_registrados
    try:
        with open('data/clientes.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                nombre, correo, nit = row
                cliente = Cliente(nombre, correo, nit)
                clientes_registrados.append(cliente)
    except FileNotFoundError:
        print("Archivo clientes.csv no encontrado. Creando uno nuevo...")

def cargar_compras():
    global compras_realizadas
    try:
        with open('data/compras.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    cliente_nit, autos_comprados_str, costo_total = row
                    cliente = next((c for c in clientes_registrados if c.nit == cliente_nit), None)
                    autos_comprados = []
                    for placa in autos_comprados_str.split(';'):
                        auto = next((a for a in autos_registrados if a.placa == placa), None)
                        if auto:
                            autos_comprados.append(auto)
                    if cliente and autos_comprados:
                        compra = Compra(cliente, autos_comprados)
                        compra.costo_total = float(costo_total)
                        compras_realizadas.append(compra)
    except FileNotFoundError:
        print("Archivo compras.csv no encontrado. Creando uno nuevo...")

# Funciones del menú
def registrar_auto():
    placa = input("Ingrese la placa del auto: ")
    marca = input("Ingrese la marca del auto: ")
    modelo = input("Ingrese el modelo del auto: ")
    descripcion = input("Ingrese una descripción del auto: ")
    precio_unitario = float(input("Ingrese el precio unitario del auto: "))

    auto = Auto(placa, marca, modelo, descripcion, precio_unitario)
    autos_registrados.append(auto)
    guardar_autos()
    print("Auto registrado con éxito.")

def registrar_cliente():
    nombre = input("Ingrese el nombre del cliente: ")
    correo = input("Ingrese el correo electrónico del cliente: ")
    nit = input("Ingrese el NIT del cliente: ")

    cliente = Cliente(nombre, correo, nit)
    clientes_registrados.append(cliente)
    guardar_clientes()
    print("Cliente registrado con éxito.")

def realizar_compra():
    nit = input("Ingrese el NIT del cliente: ")

    cliente = next((c for c in clientes_registrados if c.nit == nit), None)
    if cliente is None:
        print("Cliente no encontrado.")
        return

    autos_a_comprar = []
    while True:
        print("1. Agregar Auto")
        print("2. Terminar Compra y Generar Factura")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            placa = input("Ingrese la placa del auto a comprar: ")
            auto = next((a for a in autos_registrados if a.placa == placa and a.disponible), None)
            if auto is None:
                print("Auto no encontrado o ya ha sido comprado.")
            else:
                autos_a_comprar.append(auto)
                print(f"Auto {auto.modelo} agregado a la compra.")
        elif opcion == "2":
            if not autos_a_comprar:
                print("No se puede realizar la compra sin autos.")
            else:
                agregar_seguro = input("¿Desea agregar seguro a los autos? (SI/NO): ").strip().lower()
                costo_total = sum(auto.precio_unitario for auto in autos_a_comprar)

                if agregar_seguro == "si":
                    costo_total += sum(0.15 * auto.precio_unitario for auto in autos_a_comprar)

                compra = Compra(cliente, autos_a_comprar)
                compra.costo_total = costo_total
                compras_realizadas.append(compra)

                for auto in autos_a_comprar:
                    auto.disponible = False

                guardar_compras()
                guardar_autos()
                print(f"Compra realizada con éxito. Total: Q{compra.costo_total:.2f}")
            break

def reporte_compras():
    if not compras_realizadas:
        print("No se han realizado compras.")
    else:
        for compra in compras_realizadas:
            print(compra)
            print("="*50)
        total_general = sum(compra.costo_total for compra in compras_realizadas)
        print(f"Total General de Compras: Q{total_general:.2f}")

def datos_estudiante():
    nombre = "Brayan Emanuel Garcia"
    carnet = "202300848"
    print(f"Nombre: {nombre}")
    print(f"Carnet: {carnet}")

def salir():
    print("Saliendo del programa...")
    exit()

# Menú principal
def main():
    cargar_autos()
    cargar_clientes()
    cargar_compras()

    while True:
        print("------------- Menú Principal -------------")
        print("1. Registrar Auto")
        print("2. Registrar Cliente")
        print("3. Realizar Compra")
        print("4. Reporte de Compras")
        print("5. Datos del Estudiante")
        print("6. Salir")
        print("------------------------------------------")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_auto()
        elif opcion == "2":
            registrar_cliente()
        elif opcion == "3":
            realizar_compra()
        elif opcion == "4":
            reporte_compras()
        elif opcion == "5":
            datos_estudiante()
        elif opcion == "6":
            salir()
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
