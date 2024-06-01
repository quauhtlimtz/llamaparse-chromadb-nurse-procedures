import streamlit as st
import requests

# Display a greeting message when the user first opens the Streamlit UI
with st.chat_message("assistant"):
    st.write("¡Hola! Soy tu asistente para el Manual de Procedimientos de Enfermería 👩‍⚕️")
    st.write("Comencemos 👇")

def make_request_and_process_response(prompt):
    url = f'http://0.0.0.0:8000/query?query={prompt}'
    headers = {
        'accept': 'application/json',
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        display_response(response_json)
    else:
        st.write(f"Request failed with status code: {response.status_code}")

def display_response(response_json):    
    for key, value in response_json.items():
        if isinstance(value, list):
            st.write(f"### {key.replace('_', ' ').capitalize()}")
            for item in value:
                st.write(f"- {item}")
        else:
            st.write(f"### {key.replace('_', ' ').capitalize()}")
            st.write(f"{value}")

# Streamlit UI components
prompt = st.chat_input("Escribe aquí tu consulta")
if prompt:
    st.write(f"Tu consulta: {prompt}")
    message = st.chat_message("assistant")
    make_request_and_process_response(prompt)