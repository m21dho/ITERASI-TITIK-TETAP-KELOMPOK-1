from flask import Flask, request, render_template
import webbrowser
import math

class IterasiTitikTetap:
    def __init__(self, gx, batas_error=0.000001, nilai_awal=0, titik_desimal=7, pembulatan=True):
        self.gx = gx.replace("^", "**")
        self.batas_error = batas_error
        self.nilai_awal = nilai_awal
        self.titik_desimal = titik_desimal
        self.pembulatan = pembulatan
        self.maks_iterasi = 1000  

    def evaluasi(self, ekspresi, x):
    
        try:
            return eval(ekspresi, {"math": math, "x": x})
        except Exception as e:
            print(f"Kesalahan evaluasi: {e}")
            return None

    def hitung(self):
        x = self.nilai_awal
        hasil = []

        for iterasi in range(1, self.maks_iterasi + 1):
            gx = self.evaluasi(self.gx, x)
            if gx is None:
                return []  

            error = abs(gx - x)
            hasil.append((iterasi, round(x, self.titik_desimal), round(gx, self.titik_desimal), round(error, self.titik_desimal)))

            if error < self.batas_error:
                break  

            x = gx

        return hasil  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        gx = request.form['gx']  # Ambil ekspresi g(x) dari form
        batas_error = float(request.form['batas_error'])  # Ambil batas error dari form
        nilai_awal = float(request.form['nilai_awal'])  # Ambil nilai awal dari form

        # Gunakan nilai default untuk titik desimal dan pembulatan
        titik_desimal = 7  # Default jumlah angka desimal
        pembulatan = True  # Default pembulatan aktif

        kalkulator = IterasiTitikTetap(gx, batas_error, nilai_awal, titik_desimal, pembulatan)
        hasil = kalkulator.hitung()

        if hasil:
            return render_template('index.html', hasil=hasil)
        return '''
                <div style="color: red; font-weight: bold;">
                    Perhitungan gagal atau tidak konvergen.
                </div>
                <a href='/'>Coba lagi</a>.
            '''
    return render_template('index.html')


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"  # URL untuk aplikasi Flask

    webbrowser.open(url)  # Buka aplikasi di browser otomatis
    app.run(debug=True, use_reloader=False)
