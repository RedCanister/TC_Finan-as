import pandas as pd
import streamlit as st
import pickle
import numpy as np
import time
import psutil
from psutil import cpu_percent, virtual_memory
import torch
from sklearn.preprocessing import MinMaxScaler
from structure import Attention, LSTMModel


# Initialize Streamlit session state
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Open', 'High', 'Low', 'Prediction'])


@st.cache_resource
def load_model_and_scaler():
    """Loads the pretrained model and scaler."""
    try:
        with open('LSTM_treinado_modelo.pkl', 'rb') as file:
            model = pickle.load(file)
        with open('LSTM_scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        model.eval()  # Ensure the model is in evaluation mode
        return model, scaler
    except FileNotFoundError as e:
        st.error(f"Error loading model or scaler: {e}")
        return None, None


def get_user_data():
    """Collects user inputs via the sidebar."""
    open_price = st.sidebar.number_input('Open', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    high_price = st.sidebar.number_input('High', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    low_price = st.sidebar.number_input('Low', min_value=0.0, max_value=10000.0, value=0.0, step=0.1)
    return pd.DataFrame({'Open': [open_price], 'High': [high_price], 'Low': [low_price]})


def prepare_data(user_input, scaler):
    """Prepares and scales the input data."""
    raw_input = [[user_input['Open'][0], user_input['High'][0], user_input['Low'][0], 0]]
    scaled_input = scaler.transform(raw_input)
    sequence_input = torch.tensor(scaled_input).repeat(20, 1).unsqueeze(0).float()
    scaled_high = sequence_input[:, :, 1:2]
    scaled_low = sequence_input[:, :, 2:3]
    return sequence_input, scaled_high, scaled_low


def predict_price(model, sequence_input, scaled_high, scaled_low, scaler):
    """Generates price prediction using the trained model."""
    with torch.no_grad():
        prediction, _ = model(sequence_input, scaled_high, scaled_low)
    predictions_numpy = prediction.squeeze(-1).detach().numpy().reshape(-1, 1)
    predictions_extended = np.repeat(predictions_numpy, 4, axis=1)
    predicted_prices = scaler.inverse_transform(predictions_extended)
    return predicted_prices[:, -1].tolist()


def monitor_system():
    """Monitors system metrics."""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent, memory_percent


# Main Streamlit UI
st.title("📈 NVIDIA Stock Price Prediction")
st.sidebar.title("Enter Data")

# Load model and scaler
model, scaler = load_model_and_scaler()
if model is None or scaler is None:
    st.stop()

# Get user input
user_input_variables = get_user_data()
if st.sidebar.button('Predict'):
    st.subheader("User Input Data:")
    st.write(user_input_variables)

    # Measure runtime
    start_time = time.time()

    # Prepare data and predict
    try:
        sequence_input, scaled_high, scaled_low = prepare_data(user_input_variables, scaler)
        predictions = predict_price(model, sequence_input, scaled_high, scaled_low, scaler)
        prediction_value = predictions[0]
        user_input_variables['Prediction'] = prediction_value

        # Update session history
        st.session_state.history = pd.concat([st.session_state.history, user_input_variables], ignore_index=True)

        st.subheader("📊 Prediction:")
        st.write(prediction_value)

        st.subheader("Updated Data Table:")
        st.write(st.session_state.history)

        # Runtime and monitoring
        runtime = time.time() - start_time
        cpu_usage, memory_usage = monitor_system()
        st.sidebar.subheader("⚙️ System Monitoring")
        st.sidebar.write(f"Runtime: {runtime:.2f} seconds")
        st.sidebar.write(f"CPU Usage: {cpu_usage}%")
        st.sidebar.write(f"Memory Usage: {memory_usage}%")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
