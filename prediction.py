import pandas as pd
import numpy as np
import data_processing
import web_scraping
def get_prediction():
    mahalle_flag = 0

    with open("theta.txt", "r") as file1:
        data = file1.readlines()

    theta = np.array([float(x.strip()) for x in data])

    default_values = {
        "Fiyat": None,
        "İlçe": None,
        "Mahalle": None,
        "Brüt Metrekare": None,
        "Binanın Yaşı": None,
        "Binanın Kat Sayısı": None,
        "Kullanım Durumu": 'Boş',
        "Net Metrekare": None,
        "Oda Sayısı": None,
        "Bulunduğu Kat": None,
        "Isıtma Tipi": 'Kombi Doğalgaz',
        "Eşya Durumu": 'Boş',
        "Yapı Durumu": 'İkinci El',
        "Site İçerisinde": 'Hayır',
        "Banyo Sayısı": 1
    }

    #link = input("Enter a link: ")
    #if link != None:
    #    web_scraping.scraping(link)

    df = pd.read_csv("output.csv", dtype={"Fiyat": str})
    df = data_processing.database_setup(df)
    for i in df.columns:
        if df[i].isnull().any():
            df[i].fillna(default_values.get(i), inplace=True)
    df = data_processing.one_hot(df)
    df2 = pd.read_csv("database_default.csv")
    df3 = pd.read_csv("database.csv")

    for i in df.columns:
        if i in df2.columns:
            df2[i] = df[i]
        else:
            if i.startswith('Mahalle'):
                print(f"i eşittir {i}")
                mahalle_flag = 1

    norm_array = data_processing.minmax(df3)
    df = df2['Fiyat']
    df2 = df2.drop(columns=['Fiyat'])
    for i in df2:
        try:
            min_tmp = norm_array[i][0]
            max_tmp = norm_array[i][1]
        except Exception as e:
            min_tmp = 0
            max_tmp = 1
        df2[i] = (df2[i] - min_tmp) / (max_tmp - min_tmp)
    X = df2.values
    ones_column = np.ones((X.shape[0], 1))
    X = np.hstack((ones_column, X))
    y_pred = np.dot(X, theta)

    y_pred = data_processing.reverse_normalization(y_pred, norm_array['Fiyat'][0], norm_array['Fiyat'][1])

    y_pred_int = abs(int(y_pred))

    if mahalle_flag == 1:
        print(
            "NOTE: We currently have limited information available for this neighborhood. As a result, the predicted value may have a slight degree of uncertainty.")
    print("Predicted average value for this flat is:", y_pred_int, "\nReal price is : ", df[0])
    if y_pred_int > df[0]:
        x = (df[0] * 100) / y_pred_int
        x = 100 - x
        print(f"This house is {x}% cheaper than its equivalents.")
    else:
        x = (df[0] * 100) / y_pred_int
        x -= 100
        print(f"This house is {x}% more expensive than its equivalents.")

    return df[0], y_pred_int, mahalle_flag

def linkprediction(link):
    mahalle_flag = 0

    with open("theta.txt", "r") as file1:
        data = file1.readlines()

    theta = np.array([float(x.strip()) for x in data])

    default_values = {
        "Fiyat": None,
        "İlçe": None,
        "Mahalle": None,
        "Brüt Metrekare": None,
        "Binanın Yaşı": None,
        "Binanın Kat Sayısı": None,
        "Kullanım Durumu": 'Boş',
        "Net Metrekare": None,
        "Oda Sayısı": None,
        "Bulunduğu Kat": None,
        "Isıtma Tipi": 'Kombi Doğalgaz',
        "Eşya Durumu": 'Boş',
        "Yapı Durumu": 'İkinci El',
        "Site İçerisinde": 'Hayır',
        "Banyo Sayısı": 1
    }

    web_scraping.scraping(link)

    df = pd.read_csv("output.csv", dtype={"Fiyat": str})
    df = data_processing.database_setup(df)
    for i in df.columns:
        if df[i].isnull().any():
            df[i].fillna(default_values.get(i), inplace=True)
    df = data_processing.one_hot(df)
    df2 = pd.read_csv("database_default.csv")
    df3 = pd.read_csv("database.csv")

    for i in df.columns:
        if i in df2.columns:
            df2[i] = df[i]
        else:
            if i.startswith('Mahalle'):
                mahalle_flag = 1

    norm_array = data_processing.minmax(df3)
    df = df2['Fiyat']
    df2 = df2.drop(columns=['Fiyat'])
    for i in df2:
        try:
            min_tmp = norm_array[i][0]
            max_tmp = norm_array[i][1]
        except Exception as e:
            min_tmp = 0
            max_tmp = 1
        df2[i] = (df2[i] - min_tmp) / (max_tmp - min_tmp)

    X = df2.values
    ones_column = np.ones((X.shape[0], 1))
    X = np.hstack((ones_column, X))
    y_pred = np.dot(X, theta)

    y_pred = data_processing.reverse_normalization(y_pred, norm_array['Fiyat'][0], norm_array['Fiyat'][1])

    y_pred_int = abs(int(y_pred))

    if mahalle_flag == 1:
        print(
            "NOTE: We currently have limited information available for this neighborhood. As a result, the predicted value may have a slight degree of uncertainty.")
    print("Predicted average value for this flat is:", y_pred_int, "\nReal price is : ", df[0])
    if y_pred_int > df[0]:
        x = (df[0] * 100) / y_pred_int
        x = 100 - x
        print(f"This house is {x}% cheaper than its equivalents.")
    else:
        x = (df[0] * 100) / y_pred_int
        x -= 100
        print(f"This house is {x}% more expensive than its equivalents.")

    return df[0], y_pred_int, mahalle_flag
