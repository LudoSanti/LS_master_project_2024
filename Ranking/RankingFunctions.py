import pandas as pd
from Function.Ranking.DateTransformation import add_freshness_info




# A partire dal json iniziale costruire un dataframe più compatto che ha tante righe  quanti 
# sono i main_object_ID e tutte le informazioni per main_object aggregato creando delle metriche apposite
# e.g. sentiment medio, sentiment LLm medio, popolarità, freshness, etc

def Sentimen_medio_and_N_reviews(dimension):
        # Aggiungere le informazioni relative ai sentiment a partire dai csv calcolati
        df_1=pd.read_csv('./Data/sentiment_'+str(dimension)+'.csv')
        result_1= df_1.groupby('main_object_ID').agg(
                N_reviews=('review_ID', 'nunique'),  # Numero di recensioni per main object in cui si parla di CARBONARA
                sentiment_medio=('sentiment','mean')
            ).reset_index()
        result_1=result_1.rename(columns={'N_reviews':'N_reviews_'+str(dimension), 'sentiment_medio':'SentimentScore_'+str(dimension) })
        return result_1


def popularity_metrics(df,dim):       
    #Metrica popolarità dimensione: Numero di review analizzate per quello specifico main_object_ID che parlano della dimension/ numero di review analizzate in totale di quel Main Object ID
    df['Popularity_dim']=df['N_reviews_'+str(dim)]/df['N_reviews_input']
    #PopScore_dimensione1: popolarità della dimensione in main_object specifico diviso il totale della popolarità 1 su tutti i main object
    df['PopScore']=df['Popularity_dim']/df['Popularity_dim'].sum(axis=0)
    df=df.rename(columns={'Popularity_dim':'Popularity_'+str(dim), 'PopScore':'PopScore_'+str(dim)})
    return df


def add_dimension_info(df, dimensions):
    for dim in dimensions:
        df=df.merge(Sentimen_medio_and_N_reviews(dim), how='left')
    print('Dimensions information added')
    return df



def Pop(df,dimensions, N):
    #Metrica popolarità: Numero di review analizzate per quello specifico main_object_ID/ numero di review analizzate in totale
    df['Popularity']=df['N_reviews_input']/N
    
    for dim in dimensions:
        df=popularity_metrics(df,dim)
    print('Popolarity information added')
    return df


def ranking_dimension(df, dim):
    alpha = 1
    beta_1 = ( (df['FreshScore_'+str(dim)].max() - df['FreshScore_'+str(dim)].min()) / 
            (df['PopScore_'+str(dim)].max() - df['PopScore_'+str(dim)].min()) )
    
    beta_2 = 0.9

    gamma = 1 - beta_2
    df['Rank_'+str(dim)] = ( 
                    alpha * df['SentimentScore_'+str(dim)] *
                    (1 + beta_1 * beta_2 * df['PopScore_'+str(dim)] + gamma * df['FreshScore_'+str(dim)])
                    )
    return df

def add_ranking(df, dimensions):
     for dim in dimensions:
          df=ranking_dimension(df,dim)
     return df

def create_dataset(dimensions):
    df= pd.read_json('./Data/inputGenerico.json', orient='index')
    df=df[['main_object_ID','name','stars','price_range','N_reviews','description']]


    df_1= pd.read_json('./Data/reviews_dimensions.json', orient='index')
    result_1 = df_1.groupby('main_object_ID').agg(
        N_reviews_input=('review_ID', 'nunique')  # Numero di recensioni per main object
    ).reset_index()


    # Il merge permette di selezionare solo le reviews per cui sono presenti commenti sulle dimensioni (questa selezione avviene dopo),
    # Inoltre, aggiunge la colonna N_reviews in cui ci sono il numero di recensioni analizzate per main_object
    df=df.merge(result_1, how='left')

    N=sum(df['N_reviews_input'])

    # Aggiungere le informazioni relative ai sentiment a partire dai csv calcolati
    df=add_dimension_info(df,dimensions)

    
    #ELIMINARE RIGHE PER CUI NON SI PARLA DI NESSUNA DIMENSIONE
    # TO DO : parametrizzare questa cosa, non banale!
    #df=df[~((df['N_reviews_carbonara']).isnull()) | ~((df['N_reviews_supplì']).isnull())]

    # Aggiungere metriche relative alla popolarità
    df=Pop(df,dimensions,N)
    

    print("Computing freshness")
    df=add_freshness_info(df,dimensions)
    

    print("Computing ranking")
    df=add_ranking(df,dimensions)   
    df.to_csv('./Data/data_ranking.csv', index=False)
    print('Dataframe saved')

    return
     


