# EcoRota 

Calculadora de emissões de CO2 por modal de transporte urbano. Registra suas viagens e mostra a média de carbono emitido ao longo do tempo.

## Funcionalidades

- Calcula o CO2 emitido por viagem com base no modal e distância
- Salva o histórico de viagens em banco de dados local
- Exibe a média geral de emissões na tela inicial
- Suporta carro, ônibus, metrô, bike e a pé

## Tecnologias

- Python 3
- Flask
- SQLite

## Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/ecorota.git
cd ecorota
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Rode a aplicação**
```bash
python app.py
```

**4. Acesse no navegador**
```
http://localhost:5000
```

## Emissões por modal

| Modal   | CO2 (g/km) |
|---------|-----------|
| Carro   | 155       |
| Ônibus  | 80        |
| Metrô   | 40        |
| Bike    | 0         |
| A pé    | 0         |

## Estrutura do projeto

```
ecorota/
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
└── README.md
```
