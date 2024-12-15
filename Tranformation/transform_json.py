import json

from Function.Check.load import load_json, update_json_with_control

def insert_control_field(json_filtrato, dimensions):

    # Stringa da cercare
    dimensions = ['carbonara', 'supplì']

    # Applica la funzione di aggiornamento
    update_json_with_control(json_filtrato, dimensions)

    # Salva i dati aggiornati in un nuovo file JSON
    with open('./Data/reviews_dimensions.json', 'w') as file:
            json.dump(json_filtrato, file, indent=4)

    print(f"File updated and saved in 'Data/reviews_dimensions'")

    return


def transform(input_json, dimensions):

#A partire dai dati dal json di input e la lista dimension la funzione trasforma il json nel formato utile
# per il processamento dei dati, strotolando il dizionario delle review.
# Inoltre, invoca la funzione insert_control_field per inserire la chiave 'control', utile per identificare se nella
# review si parla o meno di una certa dimensione

    json_data=load_json(input_json)
    json_filtrato = {}
  

    # Indice per le nuove chiavi
    index = 0

    # Itera sui dati originali
    for key, valore in json_data.items():
        # Se esiste 'reviews', bisogna iterare su di essa
        if 'reviews' in valore:
            # Per ogni review, estrai i dati richiesti
            for sub_key, sub_valore in valore['reviews'].items():
                nuovo_elemento = {}

                # Aggiungi 'main_object_ID' per ogni review
                if 'main_object_ID' in valore:
                    nuovo_elemento['main_object_ID'] = valore['main_object_ID']
    
                
                # Aggiungi le chiavi 'review_title' e 'review_corpus' se presenti
                if 'review_title' in sub_valore:
                    nuovo_elemento['review_title'] = sub_valore['review_title']
                if 'review_corpus' in sub_valore:
                    nuovo_elemento['review_corpus'] = sub_valore['review_corpus']
                if 'review_date' in sub_valore:
                    nuovo_elemento['review_date'] = sub_valore['review_date']
                # Se esiste 'review_ID' aggiungilo
                if 'review_ID' in sub_valore:
                    nuovo_elemento['review_ID'] = sub_valore['review_ID']

                # Aggiungi il nuovo elemento al dizionario finale, usando un nuovo indice
                json_filtrato[index] = nuovo_elemento
                index += 1
            
    print(" Applying 'insert control field' function to indetify if the review deals with a specific dimension. Addictionaly, the function enables to analyze the review coprus and title.")

    insert_control_field(json_filtrato,dimensions)

    print("'insert control field' function applied")

    # with open('./Data/reviews.json', 'w') as json_file:
    #    json.dump(json_filtrato, json_file, indent=4)
    # print('The input JSON has been transformed and saved on "Data/reviews.json"')

    return 


def json_input_LLM(input_data, indice):

#Creazione un nuovo json per ogni dimensione, andando a prendere solo i dizionari per cui control_dimension è diverso da None con il seguente contenuto:
#- main_object_ID
#- review_ID
#- input_LLM= concatenazione review_title e review_corpus se control_dimension =both, review_corpus se control_dimension=corpus, review_title se control_dimension= title

# TO DO: aggiungere review_date e mettere in un formato utile per il calcolo della FRESHNESS   
    new_data = {}
    dimension='control_'+str(indice)
    index=0
    
    for key, value in input_data.items():
        # Verifica se control ha un valore valido
        
        if value.get(dimension) is None:
            continue  # Salta il dizionario ha control None

        # Determina il valore di 'D' in base a control_indice, in modo da avere l'input desiderato per LLM
        if value[dimension] == 'title':  
            D = value['review_title']
        elif value[dimension] == 'corpus':
            D = value['review_corpus']
        elif value[dimension] == 'both':  
            D = value['review_title'] + ". " + value['review_corpus']
        else:
            continue
        
        # Aggiungi il nuovo dizionario con le chiavi per identificare la review e il valore da dare in input all'LLM
        new_data[index] = {
            'main_object_ID': value['main_object_ID'],
            'review_ID': value['review_ID'],
            'review_date': value['review_date'],
            'input_LLM': D
        }
        index+=1
    return new_data

def split_json_by_dimension(lista):
    with open('./Data/reviews_dimensions.json', 'r') as file:
        input_data = json.load(file)

    for elemento in lista:
        new_data = {}
        print("Working on reviews about "+elemento)
        new_data = json_input_LLM(input_data, lista.index(elemento))
        with open('./Data/input_LLM_'+elemento+'.json', 'w') as file:
            json.dump(new_data, file, indent=4)
        print("New JSON file saved in Data/input_LLM_"+elemento+'.json')
    return




