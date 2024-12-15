import pandas as pd
import openai
import random

openai.api_key="" ##Mettere come parametro iniziale, non da codice!!!

def analyze_sentiment(text, dimension, topic):
# Funzione per richiamare API di openai e ottenere il sentiment relativo alle reviews 
# In questa versione il codice punta a gpt-4o
    
    response = openai.ChatCompletion.create(
        model = "gpt-4o",
        messages = [
            
            {"role": "system", 
             "content": "You are a helpful assistant."},
            
            {"role": "user", 
             "content": f"This is a review about {topic}. Return the sentiment value (1 to 5) for the {dimension}; \
                          you should also consider plurals and potential mispellings of {dimension}. \
                          ONLY RETURN the sentiment number, nothing else: {text}"}
            ])
    
    sentiment = response.choices[0].message['content'].strip()
    
    return sentiment

def LLM_sentiment(dataframe,dimension, topic):
#La funzione prende in input un dataframe di review, le dimension, il topic generico e restituisce il sentiment da LLM
# In una prima versione il sentiment tramite LLM non è attivo ma si applica un numero random da 1 a 5

    #df['sentiment']=[analyze_sentiment(x, dimension, topic) for x in df['input_LLM']]
    dataframe['sentiment']=[random.randint(1,5) for x in dataframe['input_LLM']]
    return 

def check(text):
    if text not in [1,2,3,4,5]:
        return -1
    else:
        return text

def check_sentiment(dataframe):
# Nel campo sentiment è richiesto un valore intero da 1 a 5, le review con valori diversi vengono messi a -1 per poi essere esclusi dal processing
    dataframe['sentiment']=[check(x) for x in dataframe['sentiment']]
    return

def Create_csv_sentiment(topic, dimensions):
    for dim in dimensions:
        df= pd.read_json('./Data/input_LLM_'+dim+'.json', orient='index')
        print("Analysing sentiment for reviews on which users talk about "+dim)
        LLM_sentiment(df, dim, topic)
        print("Checking sentiment values")
        check_sentiment(df) #laddove ci sono valori diversi da 1,2,3,4,5 cambiare e mettere ERRORE/-1
        # TO DO: eliminare le righe con sentiment=-1
        df.to_csv('./Data/sentiment_'+dim+'.csv', index=False)
        print('Sentiment output saved in ./Data/sentiment_'+dim+'.csv')
    return 
        
