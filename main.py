import os
import json
import glob
import nest_asyncio
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from llama_index.core import Settings
import uvicorn

from utils.chromadb import StoreVector, LoadData, QuerySearch
from utils.openai_embed import OpenAIEmbed
from prompt_definition import active_prompt_definition

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load environment variables from .env file
env_config = dotenv_values(".env")
os.environ["LLAMA_CLOUD_API_KEY"] = env_config["LLAMA_CLOUD_API_KEY"]
os.environ["OPENAI_API_KEY"] = env_config["OPENAI_API_KEY"]

# Load configuration from config.json
config = json.load(open("config.json"))

if not config:
    raise Exception("Config file not found")

# Extract configuration parameters
storage_path = config.get("storage_path")
collection_name = config.get("collection_name")
result_type = config.get("result_type")

if not all([storage_path, collection_name, result_type]):
    raise Exception("Config file is missing required fields")

def read_data_folder(data_folder):
    """
    Read the data folder and return the documents path.

    Parameters:
        data_folder (str): The path to the data folder.

    Returns:
        list: The list of document paths.
    """
    documents = glob.glob(os.path.join(data_folder, "*"))
    return documents

# Read documents from the data folder
documents_path = read_data_folder("./data")
print(documents_path)

# Initialize OpenAI embedding and language models
openai_embed = OpenAIEmbed(
    embedding_model=config.get("embedding_model"),
    generator_model=config.get("generator_model"),
)

llm, embed_model = openai_embed.init_embedding()
Settings.llm = llm
Settings.embed_model = embed_model

# Initialize storage, loading, and search functionalities
storevector = StoreVector(
    storage_path=storage_path,
    collection_name=collection_name,
    result_type=result_type,
    documents_path=documents_path,
)

loaddata = LoadData(
    storage_path=storage_path,
    collection_name=collection_name,
    result_type=result_type,
    documents_path=documents_path,
)

searchdata = QuerySearch(storage_path=storage_path, collection_name=collection_name)

app = FastAPI()

# Load the database if it does not exist and initialize the search index
try:
    if not os.path.exists(storage_path):
        loaddata.load_db()
    index = searchdata.load_index()
except Exception as e:
    raise Exception(str(e))

@app.get("/")
def read_root():
    """
    Check if the API is running.
    """
    return {"message": "API is running"}

@app.post("/db/reload")
def reload_db():
    """
    Reload the database with the latest data.
    """
    try:
        loaddata.load_db()
        return {"message": "Database reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def search_query(query: str):
    """
    Search the query in the database and return the response.
    """
    try:
        template = active_prompt_definition
        formatted_query = template.format(query)
        query_engine = index.as_query_engine()
        bot_response = query_engine.query(formatted_query)
        response_json = json.loads(bot_response.response)

        return Response(
            content=json.dumps(response_json), media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)