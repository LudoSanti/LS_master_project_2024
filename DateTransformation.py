import pandas as pd
import datetime


def calc_freshness(group, thresh_years = 2):
    mask = group['years'] <= thresh_years
    return len(group[mask]) / len(group)

def Freshness():
    df= pd.read_json('./Data/reviews_dimensions.json', orient='index')
    df_freshess = df[['main_object_ID', 'review_ID', 'review_date']]
    format="%d/%m/%Y"
    df_freshess['years'] = df_freshess['review_date'].apply(lambda x: datetime.datetime.now().year - datetime.datetime.strptime(x, format).date().year)
    
    FreshessDishSpec = ( 
                     df_freshess.groupby('main_object_ID').apply(calc_freshness, 2)
                     .to_frame()
                     .reset_index()
                     .rename(columns = {0: 'FreshScore'})
                   )
    

    return FreshessDishSpec


def Freshness_per_dimension(dimension):
        format="%d/%m/%Y"
        # Aggiungere le informazioni relative alle date a partire dai csv calcolati
        
        df_1=pd.read_csv('./Data/sentiment_'+str(dimension)+'.csv')
        df_1 = df_1[['main_object_ID', 'review_ID', 'review_date']]
        df_1['years'] = df_1['review_date'].apply(lambda x: datetime.datetime.now().year - datetime.datetime.strptime(x, format).date().year)
        FreshessDishSpec = ( 
                        df_1.groupby('main_object_ID').apply(calc_freshness, 2)
                        .to_frame()
                        .reset_index()
                        .rename(columns = {0: 'FreshScore_'+str(dimension)})
                    )
        return FreshessDishSpec

def add_freshness_info(df, dimensions):
    for dim in dimensions:
        df=df.merge(Freshness_per_dimension(dim), how='left')
    print('Freshness information added')
    return df

        



