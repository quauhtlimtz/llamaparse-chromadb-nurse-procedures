# chatbot-llamaparse

A LLM Chatbot that uses [LlamaIndex](https://www.llamaindex.ai/) and [OpenAI](https://openai.com/) with Custom PDF data to answer users query.

__Updated Repo Here:__ [**Click Me**](https://github.com/muralianand12345/llama-parse-embedding)

## Tech Used:
- Llama Index
- Llama Parse
- OpenAI API
- Llama Cloud
- ChromaDB
- FastAPI


## Installation:

- Delete storage folder in case it exists to initialize the vector db 
- Make sure you have python 3.10.* installed in your PC.
- Before we start, make sure you have ChatGPT OpenAI API and Llama Cloud API. You can get Llama Cloud API from [**here**](https://cloud.llamaindex.ai/).

```bash
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
or 
fastapi dev main.py
```

- Open up [**localhost:8000/docs**](http://localhost:8000/docs) to test the APIs.


## Improvements:

- Answer multiple questions at once.
- Add user DB.
- Parallel processing for loading database.

[Page Top](#chatbot-llamaparse)