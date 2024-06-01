# chatbot-nurse-procedures

An experimental LLM Chatbot designed to assist with nursing procedures by leveraging [LlamaIndex](https://www.llamaindex.ai/) and [OpenAI](https://openai.com/) with custom PDF data. This project uses Streamlit to provide a simple chat UI for user interaction.

## Tech Stack

- **Llama Index**
- **Llama Parse**
- **OpenAI API**
- **Llama Cloud**
- **ChromaDB**
- **FastAPI**
- **Streamlit**

## Knowledge Source

The knowledge for this chatbot was taken from the following document:

**Manual de Procedimientos de Enfermería**  
Código MT.GM.DDSS.ARSDT.ENF.311014 Versión 02  
Caja Costarricense de Seguro Social  
Gerencia Médica  
Dirección Desarrollo de Servicios de Salud  
Área de Regulación y Sistematización de Diagnóstico y Tratamiento  
Coordinación Nacional de Enfermería  
2014  

Downloaded on June 1st from: [https://www.binasss.sa.cr/protocolos/manualenfermeria.pdf](https://www.binasss.sa.cr/protocolos/manualenfermeria.pdf)

## Installation

1. **Prepare the Environment**
   - Ensure Python 3.10.* is installed on your system.
   - Obtain your ChatGPT OpenAI API key and Llama Cloud API key. Get the Llama Cloud API [here](https://cloud.llamaindex.ai/).

2. **Initialize the Project**
   - Delete the `./storage` folder if it exists to initialize the vector database and parse initial documents with llama-parse.

3. **Set Up the Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory with the following content:
     ```
     OPENAI_API_KEY=sk-*
     LLAMA_CLOUD_API_KEY=llx-*
     ```

5. **Run the Applications**
    ```bash
    uvicorn main:app --reload  # Start FastAPI
    streamlit run chat_ui.py   # Start Streamlit UI
    ```

6. **Access the Applications**
    - Open [**localhost:8000/docs**](http://localhost:8000/docs) to explore the FastAPI documentation.
    - Open [**localhost:8501**](http://localhost:8501/) to interact with the chatbot.

## Code Overview

### Architecture

1. **Streamlit UI**: Provides a user interface for interacting with the chatbot.
2. **FastAPI**: Handles API requests for querying the chatbot.
3. **OpenAIEmbed**: Initializes OpenAI embedding and generator models.
4. **ChromaDB Integration**: Manages storage and querying of vector data using ChromaDB.

### Key Components

- **Streamlit UI Initialization**: Handles user input and displays responses.
    ```python
    import streamlit as st
    import requests

    def display_greeting():
        with st.chat_message("assistant"):
            st.write("¡Hola! Soy tu asistente para el Manual de Procedimientos de Enfermería 👩‍⚕️")
            st.write("Comencemos 👇")

    def make_request_and_process_response(prompt):
        url = f'http://0.0.0.0:8000/query?query={prompt}'
        headers = {'accept': 'application/json'}
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            display_response(response_json)
        else:
            st.write(f"Request failed with status code: {response.status_code}")

    def display_response(response_json):
        for key, value in response_json.items():
            st.write(f"### {key.replace('_', ' ').capitalize()}")
            if isinstance(value, list):
                for item in value:
                    st.write(f"- {item}")
            else:
                st.write(f"{value}")

    def main():
        display_greeting()
        prompt = st.chat_input("Escribe aquí tu consulta")
        if prompt:
            st.write(f"Tu consulta: {prompt}")
            make_request_and_process_response(prompt)

    if __name__ == "__main__":
        main()
    ```

- **OpenAI Embedding Initialization**: Initializes the OpenAI embedding and generator models.
    ```python
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding

    class OpenAIEmbed:
        def __init__(self, embedding_model, generator_model):
            self.embedding_model = embedding_model
            self.generator_model = generator_model

        def init_embedding(self):
            llm = OpenAI(model=self.generator_model)
            embed_model = OpenAIEmbedding(model=self.embedding_model)
            return llm, embed_model
    ```

- **ChromaDB Integration**: Manages storage and querying of vector data.
    ```python
    import chromadb
    from llama_index.core import (
        SimpleDirectoryReader,
        StorageContext,
        VectorStoreIndex,
        load_index_from_storage,
    )
    from llama_parse import LlamaParse
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from llama_parse_parsing_instructions import parsing_instructions

    class StoreVector:
        def __init__(self, storage_path, collection_name, result_type, documents_path):
            self.storage_path = storage_path
            self.collection_name = collection_name
            self.result_type = result_type
            self.documents_path = documents_path

        def init_chroma_store(self):
            db = chromadb.PersistentClient(self.storage_path)
            chroma_collection = db.get_or_create_collection(self.collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            return storage_context

        def load_documents(self):
            parser = LlamaParse(result_type=self.result_type, parsing_instruction=parsing_instructions, verbose=True)
            file_extractor = {".pdf": parser}
            documents = SimpleDirectoryReader(
                input_files=self.documents_path,
                file_extractor=file_extractor,
            ).load_data()
            return documents

    class LoadData(StoreVector):
        def load_db(self):
            try:
                storage_context = self.init_chroma_store()
                documents = self.load_documents()
                index = VectorStoreIndex.from_documents(
                    documents, storage_context=storage_context
                )
                index.storage_context.persist()
                return index
            except Exception as e:
                if "No such file or directory" in str(e):
                    raise Exception("No data found in the data folder")
                raise Exception(str(e))

    class QuerySearch:
        def __init__(self, storage_path, collection_name):
            self.storage_path = storage_path
            self.collection_name = collection_name

        def load_index(self):
            db = chromadb.PersistentClient(path=self.storage_path)
            chroma_collection = db.get_or_create_collection(self.collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store, persist_dir=self.storage_path
            )
            index = load_index_from_storage(storage_context=storage_context)
            return index
    ```

## Author

Quauhtli Martínez  
[LinkedIn](https://www.linkedin.com/in/quauhtlimtz/)

---

[Page Top](#chatbot-nurse-procedures)