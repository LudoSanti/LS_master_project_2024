

# Funzione per validare il formato dei dati JSON
def valida_formato(json_data):
    for key, valore in json_data.items():
        # Controlliamo la chiave 'main_object': deve essere una stringa
        if 'main_object_ID' in valore and not isinstance(valore['main_object_ID'], str):
            print(f"Errore: la chiave 'main_object_ID' in '{key}' deve contenere una stringa, ma è di tipo {type(valore['main_object_ID']).__name__}.")
            return False
         # Controlliamo la chiave 'description': deve essere una stringa
        if 'description' in valore and valore['description'] is not None and not isinstance(valore['description'], str):
            print(f"Errore: la chiave 'description' in '{key}' deve contenere una stringa o un valore nullo, ma è di tipo {type(valore['description']).__name__}.")
            return False
        # Controlliamo la chiave 'price_range': deve essere una stringa
        if 'price_range' in valore and valore['price_range'] is not None and not isinstance(valore['price_range'], str):
            print(f"Errore: la chiave 'price_range' in '{key}' deve contenere una stringa o un valore nullo, ma è di tipo {type(valore['price_range']).__name__}.")
            return False
        
        # Controlliamo la chiave 'N_reviews': deve essere un intero
        if 'N_reviews' in valore and not isinstance(valore['N_reviews'], int):
            print(f"Errore: la chiave 'N_reviews' in '{key}' deve contenere un intero, ma è di tipo {type(valore['N_reviews']).__name__}.")
            return False
         # Controlliamo la chiave 'stars': deve essere un float
        if 'stars' in valore and not isinstance(valore['stars'], float):
            print(f"Errore: la chiave 'stars' in '{key}' deve contenere un float, ma è di tipo {type(valore['stars']).__name__}.")
            return False
        
        
        # Controlliamo la chiave 'reviews': deve essere un dizionario
        if 'reviews' in valore and isinstance(valore['reviews'], dict):
            for sub_key, sub_valore in valore['reviews'].items():
                # Verifica che 'sub_valore' sia un dizionario con ulteriori chiavi
                if not isinstance(sub_valore, dict):
                    print(f"Errore: la sottochiave '{sub_key}' in 'reviews' di '{key}' deve essere un dizionario.")
                    return False
                
                # Verifica che 'review_title' sia una stringa
                if 'review_title' in valore and valore['review_title'] is not None and not isinstance(valore['review_title'], str):
                    print(f"Errore: la sottochiave 'review_title' in '{sub_key}' di 'reviews' in '{key}' deve essere una stringa o un valore nullo, ma è di tipo {type(sub_valore['review_title']).__name__}.")
                    return False
                # Verifica che 'review_title' sia una stringa
                if 'review_ID' in sub_valore and not isinstance(sub_valore['review_ID'], str):
                    print(f"Errore: la sottochiave 'review_ID' in '{sub_key}' di 'reviews' in '{key}' deve essere una stringa, ma è di tipo {type(sub_valore['review_ID']).__name__}.")
                    return False
                # Verifica che 'review_corpus' sia una stringa
                if 'review_corpus' in sub_valore and not isinstance(sub_valore['review_corpus'], str):
                    print(f"Errore: la sottochiave 'review_corpus' in '{sub_key}' di 'reviews' in '{key}' deve essere una stringa, ma è di tipo {type(sub_valore['review_corpus']).__name__}.")
                    return False
                
                # Verifica che 'E' sia un intero
                if 'review_stars' in sub_valore and not isinstance(sub_valore['review_stars'], int):
                    print(f"Errore: la sottochiave 'review_stars' in '{sub_key}' di 'reviews' in '{key}' deve essere un intero, ma è di tipo {type(sub_valore['review_stars']).__name__}.")
                    return False
        else:
            print(f"Errore: la chiave 'reviews' in '{key}' deve essere un dizionario.")
            return False
    return True


