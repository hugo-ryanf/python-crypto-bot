import requests
import pandas as pd
from datetime import datetime
import time
import schedule

def fetch_crypto_data():
    print("Buscando dados atualizados na CoinGecko...")
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []

def generate_report(data):
    if not data:
        return

    df = pd.DataFrame(data)
    cols = ['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']
    df_clean = df[cols].copy()
    df_clean.columns = ['Nome', 'Símbolo', 'Preço (USD)', 'Valor de Mercado', 'Variação 24h (%)']
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"relatorio_crypto_{timestamp}.xlsx"
    
    try:
        df_clean.to_excel(filename, index=False)
        print(f"Relatório salvo: {filename}")
    except Exception as e:
        print(f"Erro ao salvar Excel: {e}")

def job():
    print(f"\nExecução iniciada em: {datetime.now().strftime('%H:%M:%S')}")
    data = fetch_crypto_data()
    generate_report(data)
    print("Aguardando o próximo intervalo...")

if __name__ == "__main__":
    print("-Definindo intevalo de tempo-")
    
    # Pergunta ao usuário o intervalo
    user_input = input("Digite o intervalo em MINUTOS para gerar novos relatórios: ")
    
    try:
        minutos = int(user_input)
    except ValueError:
        print("Valor inválido inserido. Usando padrão de 5 minutos.")
        minutos = 5

    print(f"\n Bot iniciado! Um relatório será gerado a cada {minutos} minutos.")
    print("Pressione CTRL + C para parar o programa.\n")

    job()

    schedule.every(minutos).minutes.do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n Bot finalizado pelo usuário.")
            break