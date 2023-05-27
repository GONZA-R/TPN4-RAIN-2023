############################
#Borrar pantalla
import os
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
############################

#####################################################################################################
# Funciones punto 1
"""
import csv
import requests
from xml.etree import ElementTree as ET

def get_records(base_url, metadata_prefix, identifier, max_records):
    records = []

    while len(records) < max_records:
        url = f"{base_url}?verb=GetRecord&identifier={identifier}&metadataPrefix={metadata_prefix}"
        response = requests.get(url)
        xml_response = ET.fromstring(response.content)
        record_element = xml_response.find(".//{http://www.openarchives.org/OAI/2.0/}record")
        metadata_element = record_element.find(".//{http://www.openarchives.org/OAI/2.0/}metadata")

        record_data = {}
        record_data["Title"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}title")
        record_data["Description"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}description")
        record_data["Creator"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}creator")
        record_data["Subject"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}subject")
        record_data["Date"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}date")

        records.append(record_data)

    return records

import codecs
def save_records_to_csv(records, fields, output_file):
    with codecs.open(output_file, "w", "utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print("Archivo CSV generado con éxito.")
"""

import csv
import requests
from xml.etree import ElementTree as ET

def get_records(base_url, metadata_prefix, identifier, max_records):
    records = []
    resumption_token = None
    records_count = 0

    while records_count < max_records:
        url = f"{base_url}?verb=ListRecords&metadataPrefix={metadata_prefix}"
        response = requests.get(url)
        xml_response = ET.fromstring(response.content)
        record_elements = xml_response.findall(".//{http://www.openarchives.org/OAI/2.0/}record")

        for record in record_elements:
            metadata_element = record.find(".//{http://www.openarchives.org/OAI/2.0/}metadata")
            record_data = {}
            record_data["Title"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}title")
            record_data["Description"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}description")
            record_data["Creator"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}creator")
            record_data["Subject"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}subject")
            record_data["Date"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}date")
            
            # Obtener las palabras clave (keywords)
            keywords = metadata_element.findall(".//{http://purl.org/dc/elements/1.1/}subject")
            record_data["Keywords"] = ", ".join([keyword.text for keyword in keywords])

            records.append(record_data)
            records_count += 1
            if records_count >= max_records:
                break
        
        """
        resumption_token_element = xml_response.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
        if resumption_token_element is None:
            break
        else:
            resumption_token = resumption_token_element.text

        """

    return records

import codecs
def save_records_to_csv(records, fields, output_file):
    with codecs.open(output_file, "w", "utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print("Archivo CSV generado con éxito.")




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

        # Configuración de parámetros
        base_url = "https://bibliotecadigital.exactas.uba.ar/greenstone3/oaiserver"
        metadata_prefix = "oai_dc"
        identifier = "technicalreport:technicalreport_n00024"
        fields = ["Title", "Description", "Creator", "Subject", "Date","Keywords"]
        output_file = "registros.csv"
        max_records = 1


        # Recolectar registros
        all_records = get_records(base_url, metadata_prefix, identifier, max_records)

        # Generar archivo CSV
        save_records_to_csv(all_records, fields, output_file)

        for i in all_records:
            print(i)
            print("\n")



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
