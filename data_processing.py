import pandas as pd
import numpy as np
from datetime import datetime

def min_max_normalization(x):
    normalization_array = {}
    for i in x.columns:
        min_tmp = x[i].min()
        max_tmp = x[i].max()
        x.loc[:, i] = (x[i] - min_tmp) / (max_tmp - min_tmp)
        normalization_array[i] = [max_tmp, min_tmp]
    return normalization_array

def minmax(x):
    array = {}
    for i in x.columns:
        min_x = x[i].min()
        max_x = x[i].max()
        array[i] = [min_x,max_x]
    return array

def reverse_normalization(x_normalized, min_val, max_val):
    reversed_x = (x_normalized * (max_val - min_val)) + min_val
    return reversed_x


def merge_districts(x):
    mapping = {
        'Kartal': 'KartalMaltpAtas','Maltepe': 'KartalMaltpAtas','Ataşehir': 'KartalMaltpAtas',
        'Beykoz': 'BeykSariyer','Sarıyer': 'BeykSariyer',
        'Sancaktepe': 'SancaktSultan','Sultanbeyli': 'SancaktSultan',
        'Çekmeköy': 'CekmekoySile','Şile': 'CekmekoySile',
        'Sultangazi': 'SulBayramGOPEyup','Bayrampaşa': 'SulBayramGOPEyup','Gaziosmanpaşa': 'SulBayramGOPEyup', 'Eyüpsultan':'SulBayramGOPEyup',
        'Silivri' : 'SilivriCatalca', 'Çatalca' : 'SilivriCatalca',
        'Esenyurt' : 'EsenBcekmece', 'Büyükçekmece' : 'EsenBcekmece',
        'Esenler' : 'EsenBagcGungoren', 'Bağcılar' : 'EsenBagcGungoren', 'Güngören' : 'EsenBagcGungoren',
        'Küçükçekmece' : 'KcekmeceAvcilar', 'Avcılar' : 'KcekmeceAvcilar',
        'Bakırköy' : 'BakirZeytinb', 'Zeytinburnu' : 'BakirZeytinb',
        'Arnavutköy' : 'ArnavtkBsksehir', 'Başakşehir' : 'ArnavtkBsksehir',
        'Pendik' : 'PendikTuzla', 'Tuzla' : 'PendikTuzla'
    }
    if x in mapping:
        return mapping[x]
    else:
        return x

def format_room_number(x):
    mapping = {
        '1 Oda' : 1,
        '9+ Oda' : 11,
        'Stüdyo' : 1
    }
    if x in mapping:
        return mapping[x]

    if '+' in x:
        parts = x.split('+')
        return float(parts[0])+float(parts[1])


def format_prices(x):
    x= str(x).rstrip("TLarrow_downward")
    x= str(x).rstrip("TLarrow_downward%")
    x= str(x).replace(".","")
    return int(x)

def format_squaremeter(x):
    x= str(x).replace("M2","")
    x= str(x).replace(".","")
    return int(x)

def format_deposit(x):
    if pd.isna(x):
        return
    x = str(x).replace("TL", "")
    return int(x)

def format_dates(x):
    months = {"Ocak": 1,"Şubat": 2,"Mart": 3,"Nisan": 4,"Mayıs": 5,"Haziran": 6,"Temmuz": 7,"Ağustos": 8,"Eylül": 9,"Ekim": 10,"Kasım": 11,"Aralık": 12,}
    day, month_name, year = x.strip().split()
    month_number = months[month_name]
    day = int(day)
    month = int(month_number)
    year = int(year)
    date_obj = datetime(year, month, day).date()
    date_def = datetime(2020, 1, 1).date()
    date_diff = date_obj - date_def
    day_diff = date_diff.days
    return int(day_diff)


def format_names(x):
    if pd.isna(x):
        return
    x = str(x).replace(" ","")
    return x

def site_ic(x):
    mapping = {
        'Evet': 1,
        'Hayır': 0
    }
    if x in mapping:
        return mapping[x]
    else:
        return 0

def kiral(x):
    x = str(x).replace("Kiralık", "").replace("Kiral", "").replace("Kir", "")
    return x


def fill_esya(x):
    for i in x:
        if pd.isna(i):
            i = "Boş"
    return


def esya_binary(x):
    if 'Eşyalı' in x:
        return 1
    elif 'Boş' in x:
        return 0
    else:
        return 0


def format_age(x):
    mapping = {
        '5-10': 8,
        '11-15': 13,
        '16-20': 18,
        '0 (Yeni)': 0,
        '21 Ve Üzeri': 25
    }

    if x in mapping:
        return mapping[x]

    else:
        return int(x)

def format_floor(dataset,x):
    x = str(x).replace(".Kat","")
    num_of_floors = 0
    try:
        x = int(x)
        return x
    except Exception as e:
        print(f"string is: {x}")
    mapping = {
        '10-20' : 15,
        '20-30' : 25,
        '30-40' : 35,
        'Bahçe Dublex' : 0.5,
        'Bahçe Katı' : 0,
        'Düz Giriş' : 0,
        'Düz Giriş (Zemin)': 0,
        'Kot 1 (-1)' : (-1),
        'Kot 2 (-2)' : (-2),
        'Kot 3 (-3)' : (-3),
        'Müstakil' : 0,
        'Tam Bodrum' : (-1),
        'Villa Tipi' : 0,
        'Yarı Bodrum' : (-0.5),
        'Yüksek Giriş' : (-0.5)
    }
    if x in mapping:
        return mapping[x]
    else:
        mask = (dataset['Bulunduğu Kat'] == 'Çatı Dubleks') | (dataset['Bulunduğu Kat'] == 'Çatı Katı')

        if mask.any():
            num_of_floors = dataset.loc[mask, 'Binanın Kat Sayısı'].iloc[0]
            if x=='Çatı Dubleks':
                num_of_floors -= 0.5
            return num_of_floors

        return int(x)


#df = pd.read_csv('data.csv')
#df['Fiyat'] = df['Fiyat'].map(format_prices)
#df['Fiyat Kategorisi'] = np.select([df['Fiyat'] < 10000, df['Fiyat'] > 30000],["Düşük", "Yüksek"], default="Orta")

def count(x,dict):
    for i in x:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1
    return dict
def entropy(x):
    result = 0
    dict = {}
    dict = count(x,dict)
    for i in dict:
        p = dict[i]/len(x)
        p = p * np.log2(p)
        result += p
    result *= (-1)
    return result
# z : dataset
def information_gain(z,feature1,feature2):
    ft1_list = z[feature1].values.tolist()
    ft2_list = z[feature2].values.tolist()
    ft2_values = list(set(ft2_list)) # only unique values from ft2
    total_entropy = entropy(z[feature1])
    dict = {}
    result = 0
    for pair in zip(ft1_list,ft2_list):
        if pair not in dict:
            dict[pair] = 1
        else:
            dict[pair] += 1
    num_of_ft1=0
    result = 0
    tmp = 0
    for ft1 in ft1_list:
        for ft2 in ft2_values:
            pair = (ft1,ft2)
            if(pair in dict):
                num_of_ft1 += dict[pair]
        for ft2 in ft2_values:
            pair = (ft1,ft2)
            if(pair in dict and (not pd.isna(dict[pair]))):
                prob = dict[pair] / num_of_ft1
                prob = prob * np.log2(prob)
                dict[pair] = prob

        for ft2 in ft2_values:
            pair = (ft1,ft2)
            if((pair in dict) and (not pd.isna(dict[pair]))):
               tmp += dict[pair]

        tmp *= (-1)
        if(not pd.isna(num_of_ft1)):
            prob = num_of_ft1 / len(ft1_list)
            prob *= tmp

        num_of_ft1 = 0
        tmp = 0
        result += prob
    info_gain = total_entropy - result
    print(f"Information Gain of {feature2} and {feature1} is {info_gain}")
    return info_gain

def database_setup(df):
    if 'Eşya Durumu' not in df.columns:
        df['Eşya Durumu'] = 'B'
    if 'Site İçerisinde' not in df.columns:
        df['Site İçerisinde'] = 'Hayır'
    if 'Yapı Durumu' not in df.columns:
        df['Yapı Durumu'] = 'İkinci El'
    df['Fiyat'] = df['Fiyat'].map(format_prices)
    df['İlan Oluşturma Tarihi'] = df['İlan Oluşturma Tarihi'].map(format_dates)
    df['İlan Güncelleme Tarihi'] = df['İlan Güncelleme Tarihi'].map(format_dates)
    df['Brüt Metrekare'] = df['Brüt Metrekare'].map(format_squaremeter)
    df['Net Metrekare'] = df['Net Metrekare'].map(format_squaremeter)
    df['Mahalle'] = df['Mahalle'].map(kiral)
    df['İlçe'] = df['İlçe'].map(kiral)
    df['Mahalle'] = df['Mahalle'].map(format_names)
    df['İlçe'] = df['İlçe'].map(format_names)
    df['Binanın Yaşı'] = df['Binanın Yaşı'].map(format_age)
    df['Oda Sayısı'] = df['Oda Sayısı'].map(format_room_number)
    try:
        df.drop('İlan Numarası', axis=1, inplace=True)
        df.drop('Kategorisi', axis=1, inplace=True)
        df.drop('Türü', axis=1, inplace=True)
        df.drop('Aidat', axis=1, inplace=True)
        #df.drop('İlan Oluşturma Tarihi', axis=1, inplace=True)
        #df.drop('İlan Güncelleme Tarihi', axis=1, inplace=True)
        df.drop('Depozito', axis=1, inplace=True)
        df.drop('Yapı Tipi', axis=1, inplace=True)
        df.drop('Takas', axis=1, inplace=True)
    except KeyError:
        pass
    df['Bulunduğu Kat'] = df['Bulunduğu Kat'].map(lambda x: format_floor(df, x))
    df['Eşya Durumu'].fillna('Boş', inplace=True)
    df['Eşya Durumu'] = df['Eşya Durumu'].apply(esya_binary)
    df['Mahalle'] = df['İlçe']+df['Mahalle']
    df['Site İçerisinde'] = df['Site İçerisinde'].map(site_ic)
    return df

def one_hot(df): #One-Hot encoding yapılacaktır.
    columns_to_encode = ['İlçe','Mahalle','Kullanım Durumu','Isıtma Tipi','Yapı Durumu']
    df_encoded = pd.get_dummies(df, columns=columns_to_encode)
    df_encoded = df_encoded.replace({True: 1, False: 0})
    return df_encoded