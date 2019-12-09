from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key ='gizli bişey'

client =MongoClient("mongodb+srv://egitim:egitim48@cluster0-y2eor.mongodb.net/test?retryWrites=true&w=majority")
#tododb veritabanı adı todos kolleksiyon adı
db = client.tododb.todos




@app.route('/')
def index():
    # veri tananından kayıtları çek listeye al
    yapilacaklar = []
    for yap in db.find():
        yapilacaklar.append({"_id":str(yap.get("_id")),
        "isim":yap.get("isim"),"durum":yap.get("durum")})
    # index.html ye bu listeyi gönder
@app.route('/guncelle/<id>')
def guncelle(id):
    # kaydı bulup true ise false false ise true yapcaz
    yap = db.find({'_id':ObjectId(id)})
    durum = not yap.get('durum')
    #kaydı güncelle
    db.find_one_and_update({'_id':ObjectId(id)},{'$set':{'durum':durum}})
   #ana sayfaya yönlendir
    return redirect('/')
@app.route('/sil/<id>')
def sil(id):
    #id si gelen kaydı sil
    db.find_and_delete({'_id':ObjectId(id)})
    #anasayfaya gönder
    return redirect('/')
@app.route('/ekle', methods = ['POST'])
def ekle():
    #kullanıcıdan isim aldık durumu default olarak false yaptık
    isim = request.form.get('isim')
    db.insert_one({'isim':isim, 'durum':'False'})
    #anasayfaya gönder
    return redirect('/')
#hatalı ya da olmayan url isteği gelirse hata vermesin anasayfaya gönder
@app.errorhandler(404)
def hatalı_url():
    return redirect('/')
   
    return render_template('index.html', yapilacaklar = yapilacaklar)
@app.route('/kimiz')
def kimiz():
    return render_template('kimiz.html')
@app.route('/user/<isim>')
def user(isim):
    return render_template('user.html', isim = isim)
if __name__ == '__main__':
  app.run( debug=True)
 