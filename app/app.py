import pandas as pd
import streamlit as st
import pickle
import numpy as np
import time
import psutil
import torch
import os

# Inicializa o estado de sessão do Streamlit
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Open', 'High', 'Low', 'Prediction'])

# Registrando o diretório atual do script
base_dir = os.path.dirname(__file__)

# Construa o caminho absoluto até o modelo e o scaler
model_path = os.path.join(base_dir, 'LSTM_treinado_modelo.pkl')

scaler_path = os.path.join(base_dir, 'LSTM_scaler.pkl')

#model_path = r"modelos/LSTM_treinado_modelo.pkl"
#scaler_path = r"modelos/LSTM_scaler.pkl"

@st.cache_resource
def load_model_and_scaler():
    """Carrega o modelo pré-treinado e o scaler."""
    
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        model.eval()  # Garante que o modelo está em modo de avaliação
        return model, scaler
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar o modelo ou scaler: {e}")
        return None, None


def get_user_data():
    """Coleta os dados de entrada do usuário pela barra lateral."""
    open_price = st.sidebar.number_input('Open', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    high_price = st.sidebar.number_input('High', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    low_price = st.sidebar.number_input('Low', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    return pd.DataFrame({'Open': [open_price], 'High': [high_price], 'Low': [low_price]})


def prepare_data(user_input, scaler):
    """Prepara e escala os dados de entrada."""
    raw_input = [[user_input['Open'][0], user_input['High'][0], user_input['Low'][0], 0]]
    scaled_input = scaler.transform(raw_input)
    sequence_input = torch.tensor(scaled_input).repeat(20, 1).unsqueeze(0).float()
    scaled_high = sequence_input[:, :, 1:2]  # Extrai a coluna "High" da sequência escalada
    scaled_low = sequence_input[:, :, 2:3]   # Extrai a coluna "Low" da sequência escalada
    return sequence_input, scaled_high, scaled_low


def predict_price(model, sequence_input, scaled_high, scaled_low, scaler):
    """Gera a previsão de preço usando o modelo treinado."""
    with torch.no_grad():
        prediction, _ = model(sequence_input, scaled_high, scaled_low)
    predictions_numpy = prediction.squeeze(-1).detach().numpy().reshape(-1, 1)
    predictions_extended = np.repeat(predictions_numpy, 4, axis=1)
    predicted_prices = scaler.inverse_transform(predictions_extended)
    return predicted_prices[:, -1].tolist()


def monitor_system():
    """Monitora métricas do sistema."""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent, memory_percent


# Interface principal do Streamlit
st.title("📈 Previsão do Preço das Ações da NVIDIA")
st.sidebar.title("Insira os Dados")

# Carrega o modelo e o scaler
model, scaler = load_model_and_scaler()
if model is None or scaler is None:
    st.stop()

# Obtém os dados do usuário
user_input_variables = get_user_data()
if st.sidebar.button('Prever'):
    st.subheader("Dados de Entrada do Usuário:")
    st.write(user_input_variables)

    # Mede o tempo de execução
    start_time = time.time()

    # Prepara os dados e faz a previsão
    try:
        sequence_input, scaled_high, scaled_low = prepare_data(user_input_variables, scaler)
        predictions = predict_price(model, sequence_input, scaled_high, scaled_low, scaler)
        prediction_value = predictions[0]
        user_input_variables['Prediction'] = prediction_value

        # Atualiza o histórico da sessão
        st.session_state.history = pd.concat([st.session_state.history, user_input_variables], ignore_index=True)

        st.subheader("📊 Previsão:")
        st.write(prediction_value)

        st.subheader("Tabela Atualizada:")
        st.write(st.session_state.history)

        # Tempo de execução e monitoramento
        runtime = time.time() - start_time
        cpu_usage, memory_usage = monitor_system()
        st.sidebar.subheader("⚙️ Monitoramento do Sistema")
        st.sidebar.write(f"Tempo de Execução: {runtime:.2f} segundos")
        st.sidebar.write(f"Uso de CPU: {cpu_usage}%")
        st.sidebar.write(f"Uso de Memória: {memory_usage}%")

    except Exception as e:
        st.error(f"Ocorreu um erro durante a previsão: {e}")
