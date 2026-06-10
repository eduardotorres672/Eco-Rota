from flask import Flask, request
import sqlite3
from datetime import datetime
def init_db():
    conn = sqlite3.connect('ecorota.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modal TEXT,
            distancia REAL,
            co2 REAL,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

EMISSOES = {
    'carro':  155,
    'onibus': 80,
    'metro':  40,
    'bike':   0,
    'ape':    0
}

def calcular_co2(modal, distancia_km):
    gramas = EMISSOES[modal] * distancia_km
    return gramas

@app.route('/')
def index():
    media = calcular_media()
    return f'''
    <h1>EcoRota 🌱</h1>
    <p>Média de CO2 emitido: {media} kg</p>
    <form method="POST" action="/calcular">
        <label>Modal:</label>
        <select name="modal">
            <option value="carro">Carro</option>
            <option value="onibus">Onibus</option>
            <option value="metro">Metro</option>
            <option value="bike">Bike</option>
            <option value="ape">A pe</option>
        </select>
        <br><br>
        <label>Distancia (km):</label>
        <input type="number" name="distancia" value="10">
        <br><br>
        <button type="submit">Calcular</button>
    </form>
    '''
def calcular_media():
    conn = sqlite3.connect('ecorota.db')
    resultado = conn.execute('SELECT AVG(co2) FROM viagens')
    media = resultado.fetchone()[0]
    conn.close()
    return round(media, 2) if media else 0      

@app.route('/calcular', methods=['POST'])
def calcular():
    modal = request.form['modal']
    distancia = float(request.form['distancia'])
    co2 = calcular_co2(modal, distancia)
    
    conn = sqlite3.connect('ecorota.db')
    conn.execute(
        'INSERT INTO viagens (modal, distancia, co2, data) VALUES (?, ?, ?, ?)',
        (modal, distancia, co2, datetime.now().strftime('%d/%m/%Y %H:%M'))
    )
    conn.commit()
    conn.close()
    co2_kg = round(co2 /1000, 2) 
   
    return f'<h1>CO2 emitido: {co2_kg} kg</h1><a href="/">Voltar</a>'

if __name__ == '__main__':
    app.run(debug=True)

4595c28786f25d0e2388489f893f904f2932bbd6		branch 'main' of https://github.com/eduardotorres672/Quiz-de-perguntas

ref: refs/heads/main

2cda108ca12d0f28cc5f8120240717bcd4181519
