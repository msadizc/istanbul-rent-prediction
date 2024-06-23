from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def scraping(str_x):
    browser = webdriver.Chrome()
    details = []
    prices = []
    districts = []
    neighborhoods = []
    print(str_x)
    try:
        existing_df = pd.read_csv('output.csv')
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    try:
        browser.get(str_x)
        features = browser.find_element(By.XPATH,
                                                    "/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[4]/div/div[2]/div/div[1]")
        district = browser.find_element(By.XPATH,
                                                    "/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/ul/li[4]")
        neighborhood = browser.find_element(By.XPATH,
                                                        "/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/ul/li[5]")
        price = browser.find_element(By.CLASS_NAME, "R-RKDB")

        details.append(features.text)
        prices.append(price.text[:-2])
        dist = str(district.text).split()[0]
        districts.append(dist)
        nbh = str(neighborhood.text).split()
        neigh = "".join(nbh[:-2])
        neighborhoods.append(neigh)
    except Exception as e:
        print(f"An error occurred for item {i}: {e}")

    # lines = []
    # for i in range(0,3):
    #   lines.append(details[i].splitlines())
    #    print(lines[i])
    data_list = list(zip(details, prices, districts, neighborhoods))
    dict = {}

    for data in data_list:
        details, price, district, neighborhood = data
        lines = details.splitlines()
        temp_dict = {}
        temp_dict['Fiyat'] = price
        temp_dict['İlçe'] = district
        temp_dict['Mahalle'] = neighborhood
        for j in range(0, len(lines), 2):
            key = lines[j]
            value = lines[j + 1]
            if key in temp_dict:
                temp_dict[key].append(value)
            else:
                temp_dict[key] = value
        list_number = temp_dict['İlan Numarası']
        dict[list_number] = temp_dict

    new_data_df = pd.DataFrame.from_dict(dict, orient='index')

    new_data_df.to_csv('output.csv', index=False)


