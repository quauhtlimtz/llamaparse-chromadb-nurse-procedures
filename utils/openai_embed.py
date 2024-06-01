from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

class OpenAIEmbed:
    def __init__(self, embedding_model, generator_model):
        """
        Initialize the OpenAIEmbed class with the specified models.

        Parameters:
            embedding_model (str): The model used for creating text embeddings.
            generator_model (str): The model used for generating text.
        """
        self.embedding_model = embedding_model
        self.generator_model = generator_model

    def init_embedding(self):
        """
        Initialize the embedding and generator models.

        Returns:
            tuple: A tuple containing the language model (llm) and embedding model (embed_model).
        """
        llm = OpenAI(model=self.generator_model)
        embed_model = OpenAIEmbedding(model=self.embedding_model)
        return llm, embed_model