from Function.Check.check_json import valida_formato
import json

def load_json(input_json):
    try:
        with open(input_json, 'r') as file:
            dati_json = json.load(file)
    except json.JSONDecodeError:
        print("Error during the JSON reading. The file could be damaged.")
        dati_json = {}

    # Validazione del formato
    if not valida_formato(dati_json):
        print("Error: JSON format not valid. The execution has been interrupted.")
    else:
        print("Valid JSON format. The execution proceeds")
    return  dati_json

def update_json_with_control(data, lista):
    for elemento in lista:
        nuova_chiave= 'control_'+ str(lista.index(elemento))
        for key, value in data.items():
            # Verifica se la stringa è presente nei valori delle chiavi title e corpus
            found_in_title = elemento in value['review_title'].lower()
            found_in_corpus = elemento in value['review_corpus'].lower()
            
            # Determina il valore di 'control'
            if found_in_title and found_in_corpus:
                value[nuova_chiave] = 'both'
            elif found_in_title:
                value[nuova_chiave] = 'title'
            elif found_in_corpus:
                value[nuova_chiave] = 'corpus'
            else:
                value[nuova_chiave] = None
    return 