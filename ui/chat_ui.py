import streamlit as st
import requests

# Function to display the initial greeting message
def display_greeting():
    with st.chat_message("assistant"):
        st.write("¡Hola! Soy tu asistente para el Manual de Procedimientos de Enfermería 👩‍⚕️")
        st.write("Comencemos 👇")

# Function to make a request to the backend and process the response
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

# Function to display the response from the backend
def display_response(response_json):
    for key, value in response_json.items():
        st.write(f"### {key.replace('_', ' ').capitalize()}")
        if isinstance(value, list):
            for item in value:
                st.write(f"- {item}")
        else:
            st.write(f"{value}")

# Main function to run the Streamlit app
def main():
    # Display the initial greeting message
    display_greeting()

    # Streamlit UI components
    prompt = st.chat_input("Escribe aquí tu consulta")
    if prompt:
        st.write(f"Tu consulta: {prompt}")
        make_request_and_process_response(prompt)

if __name__ == "__main__":
    main()