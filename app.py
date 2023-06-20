from flask import Flask, render_template, request, url_for, jsonify
import numpy as np

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/set_titik", methods=["POST"])
def set_titik():
    #* Ambil data jumlah titik dari request ajax
    titik = request.get_data("titik")
    try:
        #* Ubah data jumlah titik menjadi integer, lalu buat matrix n*n dengan numpy
        titik = int(titik)
        matrix = np.zeros((titik, titik))

        #* Isi nilai dari matrix pada lokasi (i, i) dimana i = n dengan numpy.infinity
        for i in range(0, titik):
            matrix[i][i] = np.inf

        #* Buat tabel html dengan class tailwindcss
        html_table = '<table class="w-full text-sm text-left text-gray-500">'
        html_table += '<p class="block mr-2 text-sm font-medium text-gray-900 dark:text-white mb-4">Masukkan jarak antar titik:</p>'

        #* Tambahkan nama kolom (1, 2, dst)
        html_table += '<tr>'
        html_table += "<th></th>"
        for i in range(1, titik+1):
            html_table += f'<th class="border px-4 py-2 text-center">{i}</th>'
        html_table += '</tr>'
        
        #* Tambahkan nama index atau baris ()
        for i, row in enumerate(matrix):
            html_table += '<tr>'
            html_table += f'<th class="border px-4 py-2">{i + 1}</th>'
            columns = 0
            for value in row:
                if i == columns:
                    html_table += f'<td class="border px-4 py-2 text-center"><input type="text" name="titik_{i+1, columns+1}" id="titik_{i+1, columns+1}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-20 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mx-auto text-center disabled" value="&infin;" disabled /></td>'
                else:
                    html_table += f'<td class="border px-4 py-2 text-center"><input type="text" name="titik_{i+1, columns+1}" id="titik_{i+1, columns+1}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-20 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mx-auto text-center" value="{value}" oninput="setNilaiPalindrom({i+1}, {columns+1})" /></td>'
                columns += 1
            html_table += '</tr>'
        html_table += '</table>'
        html_table += '<button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 mt-4 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onclick="setNilaiSimpul()">Hitung Nilai Simpul Akar</button>'

        return html_table
    except Exception as e:
        return f"error occurred: {str(e)}"


@app.route("/hitung_simpul", methods=["POST"])
def hitung_simpul():
    loc_data = request.get_json("data_val")
    data_length = len(loc_data)
    try:
        #* Buat ulang matrix n*n dengan numpy
        matrix = np.zeros((data_length, data_length))

        #* Isi nilai dari matrix pada lokasi (i, i) dimana i = n dengan numpy.infinity
        for i in range(0, data_length):
            matrix[i][i] = np.inf

        #* Isi nilai dari matrix pada lokasi (i, j) dengan data dari ajax
        for i in range(0, data_length):
            for j in range(0, data_length):
                if i == j:
                    pass
                else:
                    matrix[i][j] = loc_data[str(i+1)][str(j+1)]

        simpul_akar = []

        def hitung_simpul_akar():
            min_row = 0
            min_col = 0

            for i in range(0, data_length):
                min_row = min(matrix[i, :])
                if min_row != float(0):
                    simpul_akar.append(min_row)
                    for j in range(0, data_length):
                        if i == j:
                            pass
                        else:
                            matrix[i][j] -= min_row
            
            for i in range(0, data_length):
                min_col = min(matrix[:, i])
                if min_col != float(0):
                    simpul_akar.append(min_col)
                    for j in range(0, data_length):
                        if i == j:
                            pass
                        else:
                            matrix[j][i] -= min_col
        
        hitung_simpul_akar()                

        #* Buat tabel html dengan class tailwindcss
        html_table = '<table class="w-full text-sm text-left text-gray-500">'
        html_table += '<p class="block mr-2 text-sm font-medium text-gray-900 dark:text-white mb-4">C(R) = ' + str(round(sum(simpul_akar), 2)) + '</p>'

        #* Tambahkan nama kolom (1, 2, dst)
        html_table += '<tr>'
        html_table += "<th></th>"
        for i in range(1, data_length+1):
            html_table += f'<th class="border px-4 py-2 text-center">{i}</th>'
        html_table += '</tr>'
        
        #* Tambahkan nama index atau baris ()
        for i, row in enumerate(matrix):
            html_table += '<tr>'
            html_table += f'<th class="border px-4 py-2">{i + 1}</th>'
            columns = 0
            for value in row:
                value = round(value, 2)
                if i == columns:
                    html_table += f'<td class="border px-4 py-2 text-center"><input type="text" name="titik_{i+1, columns+1}" id="titik_{i+1, columns+1}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-20 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mx-auto text-center disabled" value="&infin;" disabled /></td>'
                else:
                    html_table += f'<td class="border px-4 py-2 text-center"><input type="text" name="titik_{i+1, columns+1}" id="titik_{i+1, columns+1}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-20 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mx-auto text-center" value="{value}" oninput="setNilaiPalindrom({i+1}, {columns+1})" /></td>'
                columns += 1
            html_table += '</tr>'
        html_table += '</table>'
        
        return html_table
    except Exception as e:
        return f"error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
