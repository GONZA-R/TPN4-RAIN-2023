############################
#Borrar pantalla
import os
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
############################

#####################################################################################################
# Funciones punto 1

import csv
import requests
from xml.etree import ElementTree as ET

def get_records(base_url, metadata_prefix, identifier):
    records = []
    url = f"{base_url}?verb=GetRecord&identifier={identifier}&metadataPrefix={metadata_prefix}"
    response = requests.get(url)
    xml_response = ET.fromstring(response.content)
    record_element = xml_response.find(".//{http://www.openarchives.org/OAI/2.0/}record")
    metadata_element = record_element.find(".//{http://www.openarchives.org/OAI/2.0/}metadata")

    record_data = {}
    record_data["Title"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}title")
    record_data["Description"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}description")

    creators = metadata_element.findall(".//{http://purl.org/dc/elements/1.1/}creator")
    record_data["Creator"] = [creator.text for creator in creators]


    record_data["Subject"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}subject")
    record_data["Date"] = metadata_element.findtext(".//{http://purl.org/dc/elements/1.1/}date")

    # Obtener las palabras clave (keywords)
    keywords = metadata_element.findall(".//{http://purl.org/dc/elements/1.1/}subject")
    record_data["Keywords"] = ", ".join([keyword.text for keyword in keywords])


    records.append(record_data)

    return records


import csv
import codecs

def save_records_to_csv(records, fields, output_file):
    with codecs.open(output_file, "w", "utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for record in records:
            writer.writerow({
                "Title": record[0]["Title"],
                "Description": record[0]["Description"],
                "Creator": record[0]["Creator"],
                "Subject": record[0]["Subject"],
                "Date": record[0]["Date"],
                "Keywords": record[0]["Keywords"]
            })

    print("Archivo CSV generado con éxito.")





#####################################################################################################
import requests
from xml.etree import ElementTree as ET

def get_all_identifiers(base_url, metadata_prefix, max_records):
    identifiers = []
    resumption_token = None
    records_count = 0

    while records_count < max_records:
        url = f"{base_url}?verb=ListIdentifiers&metadataPrefix={metadata_prefix}"
        if resumption_token:
            url += f"&resumptionToken={resumption_token}"

        response = requests.get(url)
        xml_response = ET.fromstring(response.content)
        identifier_elements = xml_response.findall(".//{http://www.openarchives.org/OAI/2.0/}header/{http://www.openarchives.org/OAI/2.0/}identifier")
        identifiers.extend([identifier.text for identifier in identifier_elements])

        records_count += len(identifier_elements)

        if records_count >= max_records:
            break

        resumption_token_element = xml_response.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
        if resumption_token_element is None:
            break
        else:
            resumption_token = resumption_token_element.text

    return identifiers

#####################################################################################################
import os
import inspect
import pandas as pd

def restructure_csv(input_file, output_file):
    # Obtener la ruta del archivo actual
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    # Combinar la ruta con el nombre del archivo CSV de entrada
    input_path = os.path.join(current_dir, input_file)

    # Leer el archivo CSV y cargarlo en un DataFrame
    df = pd.read_csv(input_path)

    # Estructurar los datos visualmente
    structured_df = df.style

    # Guardar los datos estructurados en un nuevo archivo CSV
    structured_df.to_csv(output_file, index=False)

    print("Archivo CSV estructurado y guardado con éxito.")



# FIN Funciones punto 1
#####################################################################################################

#####################################################################################################
# Funciones punto 2
import os
import lucene
from lucene import \
    Document, Field, StandardAnalyzer, IndexWriter, IndexWriterConfig, FSDirectory, Version

INDEX_DIRECTORY = '/path/to/index/directory'

def index_documents(documents_path):
    lucene.initVM()  # Inicializar el entorno de Lucene

    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    directory = FSDirectory.open(File(INDEX_DIRECTORY).toPath())
    writer = IndexWriter(directory, config)

    for root, dirs, files in os.walk(documents_path):
        for file_name in files:
            if is_supported_file_type(file_name):
                file_path = os.path.join(root, file_name)
                document = Document()
                document.add(Field("path", file_path, Field.Store.YES, Field.Index.NOT_ANALYZED))
                document.add(Field("content", open(file_path, 'r').read(), Field.Store.NO, Field.Index.ANALYZED))
                writer.addDocument(document)

    writer.close()

def search(query_string):
    lucene.initVM()  # Inicializar el entorno de Lucene

    directory = FSDirectory.open(File(INDEX_DIRECTORY).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))

    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    parser = QueryParser(Version.LUCENE_CURRENT, "content", analyzer)
    query = parser.parse(query_string)

    top_docs = searcher.search(query, 10)  # Obtener los 10 mejores resultados

    for score_doc in top_docs.scoreDocs:
        doc = searcher.doc(score_doc.doc)
        print("Score: {}\tPath: {}".format(score_doc.score, doc.get("path")))

    searcher.getIndexReader().close()

def is_supported_file_type(file_name):
    supported_extensions = ['.doc', '.docx', '.pdf', '.txt', '.ppt', '.pptx', '.dat', '.html']
    extension = os.path.splitext(file_name)[1].lower()
    return extension in supported_extensions

# Ejemplo de uso
documents_directory = '/path/to/documents/directory'
index_documents(documents_directory)

# Realizar una búsqueda
search_query = 'example query'
search(search_query)


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

        max_records = 300
        # Obtener los 300 primeros identificadores
        identifiers = get_all_identifiers(base_url, metadata_prefix, max_records)
        

        directorio=[]


        for identifier in identifiers:
            # Recolectar registros
            all_records = get_records(base_url, metadata_prefix, identifier)
            directorio.append(all_records)
           

        # Generar archivo CSV
        fields = ["Title", "Description", "Creator", "Subject", "Date","Keywords"]
        output_file = "registros.csv"

        save_records_to_csv(directorio, fields, output_file)
        #restructure_csv("registros.csv", "registros_salida.csv")


    
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
