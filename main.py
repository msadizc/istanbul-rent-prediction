from flask import Flask, request, jsonify, render_template
import pandas as pd
import prediction


app = Flask("__name__", template_folder=".")

@app.route("/")
def loadPage():
   return render_template('home.html',query="")

@app.route("/save_property",methods=['POST'])
def save_property():
   if request.method == 'POST':
      fiyat = float(request.form['fiyat'])
      ilce = request.form['ilce']
      mahalle = request.form['mahalle']
      brutmetrekare = request.form['brutmetrekare']
      binayasi = request.form['yas']
      katsayisi = request.form['katsayisi']
      kullanimdurumu = request.form['kuldurumu']
      netmetrekare = request.form['netmetrekare']
      odasayisi = request.form['odasayisi']
      bulundugukat = request.form['bulundugukat']
      isitmatipi = request.form['isitmatipi']
      esyadurumu = request.form['esyadurumu']
      yapidurumu = request.form['yapidurumu']
      siteicerisinde = request.form['site']
      banyosayisi = request.form['banyosayisi']

   response_data = {
      'fiyat': fiyat,
      'ilce': ilce,
      'mahalle': mahalle,
      'brutmetrekare': brutmetrekare,
      'yas': binayasi,
      'katsayisi': katsayisi,
      'kuldurumu': kullanimdurumu,
      'netmetrekare': netmetrekare,
      'odasayisi': odasayisi,
      'bulundugukat': bulundugukat,
      'isitmatipi': isitmatipi,
      'esyadurumu': esyadurumu,
      'yapidurumu': yapidurumu,
      'site': siteicerisinde,
      'banyosayisi': banyosayisi,
   }

   df = pd.read_csv("output.csv")

   df['Fiyat'] = int(fiyat)
   df['İlçe'] = ilce
   df['Mahalle'] = mahalle
   df['Brüt Metrekare'] = brutmetrekare
   df['Net Metrekare'] = netmetrekare
   df['Oda Sayısı'] = odasayisi
   df['Binanın Yaşı'] = binayasi
   df['Binanın Kat Sayısı'] = katsayisi
   df['Bulunduğu Kat'] = bulundugukat
   df['Isıtma Tipi'] = isitmatipi
   df['Yapı Durumu'] = yapidurumu
   df['Eşya Durumu'] = esyadurumu
   df['Site İçerisinde'] = siteicerisinde

   df.to_csv("output.csv",index=False)

   return jsonify({'Success': 'Success'})

@app.route("/predict", methods=['GET'])
def predict():
    try:
        sonuc = ("")
        price, y_pred_int, mahalle_flag = prediction.get_prediction()
        if y_pred_int > price:
            x = (price * 100) / y_pred_int
            x = 100 - x

        else:
            x = (price * 100) / y_pred_int
            x -= 100

        if mahalle_flag == 1:
            sonuc = ("            NOT: Bu mahalleyle ilgili elimizde yeterli veri olmadığı için tahmin edilen fiyatta bir miktar sapma olabilir. ")

        y_pred_int = int(y_pred_int)
        price = int(price)
        return jsonify({'sonuc': sonuc,
                        'y_pred_int': y_pred_int,
                        'price': price,
                        'x': x})

    except Exception as e:
        return jsonify({'error': 'Error occurred: ' + str(e)})

@app.route("/savelink", methods=['POST'])
def savelink():
    global saved_link
    if request.method == 'POST':
        saved_link = request.form['link']

    return "Link saved and prediction retrieved."

@app.route("/linkpredict", methods=['GET'])
def linkpredict():
    global saved_link
    if saved_link is None:
        return jsonify({'error':'No link has been submitted.'})
    try:
        sonuc = ("")
        price, y_pred_int, mahalle_flag = prediction.linkprediction(saved_link)
        if y_pred_int > price:
            x = (price * 100) / y_pred_int
            x = 100 - x
        else:
            x = (price * 100) / y_pred_int
            x -= 100

        if mahalle_flag == 1:
            sonuc = ("            NOT: Bu mahalleyle ilgili elimizde yeterli veri olmadığı için tahmin edilen fiyatta bir miktar sapma olabilir. ")


        y_pred_int = int(y_pred_int)
        price = int(price)

        print(jsonify({'sonuc': sonuc,
                       'y_pred_int': y_pred_int,
                       'price':price,
                       'x': x}))
        return jsonify({'sonuc': sonuc,
                       'y_pred_int': y_pred_int,
                       'price':price,
                       'x': x})

    except Exception as e:
        return jsonify({'error': 'Error occurred: ' + str(e)})

if __name__ == "__main__":
    app.run()
