from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- Configurações ---

DB_PATH = 'ecorota.db'

EMISSOES = {
    'carro':  155,
    'onibus': 80,
    'metro':  40,
    'bike':   0,
    'ape':    0
}

LABELS = {
    'carro':  '🚗 Carro',
    'onibus': '🚌 Ônibus',
    'metro':  '🚇 Metrô',
    'bike':   '🚲 Bike',
    'ape':    '🚶 A pé'
}

# --- Banco de dados ---

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS viagens (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                modal     TEXT,
                distancia REAL,
                co2       REAL,
                data      TEXT
            )
        ''')

def salvar_viagem(modal, distancia, co2):
    with get_conn() as conn:
        conn.execute(
            'INSERT INTO viagens (modal, distancia, co2, data) VALUES (?, ?, ?, ?)',
            (modal, distancia, co2, datetime.now().strftime('%d/%m/%Y %H:%M'))
        )

def buscar_media():
    with get_conn() as conn:
        resultado = conn.execute('SELECT AVG(co2) FROM viagens').fetchone()[0]
    return round(resultado / 1000, 2) if resultado else 0

def buscar_historico(limite=5):
    with get_conn() as conn:
        rows = conn.execute(
            'SELECT modal, distancia, co2, data FROM viagens ORDER BY id DESC LIMIT ?',
            (limite,)
        ).fetchall()
    return rows

# --- Lógica de negócio ---

def calcular_co2(modal, distancia_km):
    return EMISSOES[modal] * distancia_km

# --- Template HTML ---

TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EcoRota</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:       #0d1a0f;
      --surface:  #142018;
      --border:   #1f3325;
      --green:    #4ade80;
      --green-dim:#1a4a2a;
      --amber:    #fbbf24;
      --text:     #e2ead4;
      --muted:    #6b8a72;
      --radius:   12px;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Space Grotesk', sans-serif;
      min-height: 100vh;
      padding: 2rem 1rem;
    }

    .container {
      max-width: 560px;
      margin: 0 auto;
    }

    /* Header */
    header {
      display: flex;
      align-items: baseline;
      gap: .75rem;
      margin-bottom: 2.5rem;
      padding-bottom: 1.25rem;
      border-bottom: 1px solid var(--border);
    }
    header h1 {
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -.02em;
      color: var(--green);
    }
    header span {
      font-size: .8rem;
      color: var(--muted);
      font-family: 'Space Mono', monospace;
      letter-spacing: .06em;
      text-transform: uppercase;
    }

    /* Stat de média */
    .stat-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .stat-label {
      font-size: .75rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .08em;
      margin-bottom: .25rem;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      font-family: 'Space Mono', monospace;
      color: {% if media == 0 %}var(--green){% elif media < 1 %}var(--amber){% else %}#f87171{% endif %};
    }
    .stat-unit { font-size: .85rem; color: var(--muted); margin-left: .25rem; }
    .eco-badge {
      font-size: 1.8rem;
      opacity: .7;
    }

    /* Formulário */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    .card-title {
      font-size: .75rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      margin-bottom: 1.25rem;
    }

    label {
      display: block;
      font-size: .8rem;
      color: var(--muted);
      margin-bottom: .4rem;
      text-transform: uppercase;
      letter-spacing: .06em;
    }

    select, input[type="number"] {
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1rem;
      padding: .7rem 1rem;
      margin-bottom: 1rem;
      outline: none;
      transition: border-color .2s;
      appearance: none;
    }
    select:focus, input[type="number"]:focus {
      border-color: var(--green);
    }

    button {
      width: 100%;
      background: var(--green);
      color: #0d1a0f;
      border: none;
      border-radius: 8px;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1rem;
      font-weight: 700;
      padding: .8rem;
      cursor: pointer;
      letter-spacing: .02em;
      transition: opacity .2s;
    }
    button:hover { opacity: .85; }

    /* Resultado */
    .result-card {
      background: var(--green-dim);
      border: 1px solid var(--green);
      border-radius: var(--radius);
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      text-align: center;
    }
    .result-label { font-size: .75rem; color: var(--green); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .5rem; }
    .result-value { font-size: 2.8rem; font-weight: 700; font-family: 'Space Mono', monospace; color: var(--green); }
    .result-unit  { font-size: 1rem; color: var(--muted); }
    .result-modal { font-size: .85rem; color: var(--muted); margin-top: .5rem; }

    /* Histórico */
    .history-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: .65rem 0;
      border-bottom: 1px solid var(--border);
      font-size: .88rem;
    }
    .history-row:last-child { border-bottom: none; }
    .history-modal { color: var(--text); }
    .history-meta  { color: var(--muted); font-size: .75rem; margin-top: .1rem; }
    .history-co2   { font-family: 'Space Mono', monospace; font-size: .85rem; color: var(--amber); text-align: right; }

    /* Link voltar */
    .back {
      display: inline-block;
      margin-top: .5rem;
      color: var(--green);
      text-decoration: none;
      font-size: .9rem;
      border-bottom: 1px solid transparent;
      transition: border-color .2s;
    }
    .back:hover { border-color: var(--green); }
  </style>
</head>
<body>
<div class="container">

  <header>
    <h1>EcoRota</h1>
    <span>Calculadora de CO₂</span>
  </header>

  {% if resultado %}
  <!-- Tela de resultado -->
  <div class="result-card">
    <div class="result-label">CO₂ emitido nesta viagem</div>
    <div>
      <span class="result-value">{{ resultado.co2_kg }}</span>
      <span class="result-unit"> kg</span>
    </div>
    <div class="result-modal">{{ resultado.label }} · {{ resultado.distancia }} km</div>
  </div>
  <a class="back" href="/">← Calcular outra viagem</a>

  {% else %}
  <!-- Tela principal -->
  <div class="stat-card">
    <div>
      <div class="stat-label">Média de CO₂ por viagem</div>
      <div>
        <span class="stat-value">{{ media }}</span>
        <span class="stat-unit">kg</span>
      </div>
    </div>
    <div class="eco-badge">🌿</div>
  </div>

  <div class="card">
    <div class="card-title">Nova viagem</div>
    <form method="POST" action="/calcular">
      <label for="modal">Meio de transporte</label>
      <select name="modal" id="modal">
        <option value="carro">🚗 Carro</option>
        <option value="onibus">🚌 Ônibus</option>
        <option value="metro">🚇 Metrô</option>
        <option value="bike">🚲 Bike</option>
        <option value="ape">🚶 A pé</option>
      </select>

      <label for="distancia">Distância (km)</label>
      <input type="number" name="distancia" id="distancia" value="10" min="0.1" step="0.1">

      <button type="submit">Calcular emissão</button>
    </form>
  </div>

  {% if historico %}
  <div class="card">
    <div class="card-title">Últimas viagens</div>
    {% for v in historico %}
    <div class="history-row">
      <div>
        <div class="history-modal">{{ labels[v[0]] }}</div>
        <div class="history-meta">{{ v[3] }} · {{ v[1] }} km</div>
      </div>
      <div class="history-co2">{{ "%.2f"|format(v[2]/1000) }} kg</div>
    </div>
    {% endfor %}
  </div>
  {% endif %}

  {% endif %}

</div>
</body>
</html>
'''

# --- Rotas ---

@app.route('/')
def index():
    media = buscar_media()
    historico = buscar_historico()
    return render_template_string(TEMPLATE, media=media, historico=historico, labels=LABELS, resultado=None)

@app.route('/calcular', methods=['POST'])
def calcular():
    modal     = request.form['modal']
    distancia = float(request.form['distancia'])
    co2       = calcular_co2(modal, distancia)

    salvar_viagem(modal, distancia, co2)

    resultado = {
        'co2_kg':   round(co2 / 1000, 2),
        'label':    LABELS[modal],
        'distancia': distancia,
    }
    return render_template_string(TEMPLATE, resultado=resultado, media=None, historico=None, labels=LABELS)

# --- Inicialização ---

init_db()

if __name__ == '__main__':
    app.run(debug=True)