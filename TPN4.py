############################
#Borrar pantalla
import os
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
############################

#####################################################################################################
# Funciones punto 1


#####################################################################################################


while True:
    clear_screen()
    print("Trabajo Practico N°3 Crawler y Scraper"+"\n\n")
    print("1. Automatización de Extracción de Metadatos: Generación de CSV desde un Repositorio")
    print("2. Indexador de Documentos Local con Lucene: Búsqueda y Visualización de Resultados")
    print("3. Salir\n")

    opcion = input("Ingrese una opción: ")
    if opcion == "1":
        clear_screen()
        input("Presione enter para continuar...")
        pass

    elif opcion == "2":
        clear_screen()


        input("\nPresione enter para continuar...")
       
        pass


    
####################################################################################3
    elif opcion == "3":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida, por favor intente de nuevo.")
        input("Presione enter para continuar...")
