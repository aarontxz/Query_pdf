from langchain.llms.base import LLM
from llama_index import SimpleDirectoryReader, LangchainEmbedding, ListIndex, TreeIndex, KeywordTableIndex
from llama_index import LLMPredictor, ServiceContext
from transformers import pipeline
from typing import Optional, List, Mapping, Any
from transformers import AutoModelForSeq2SeqLM
import transformers
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
# Load the BART model
llm = OpenAI()

# define our LLM
llm_predictor = LLMPredictor(llm=llm)

service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor
)

def create_tree_index_query_engine():
    # Load the your data
    documents = SimpleDirectoryReader('./data').load_data()
    index = TreeIndex.from_documents(documents, service_context=service_context)

    # Query and print response
    query_engine = index.as_query_engine()
    return query_engine

def create_list_index_query_engine():
    # Load the your data
    documents = SimpleDirectoryReader('./data').load_data()
    index = TreeIndex.from_documents(documents, service_context=service_context)

    # Query and print response
    query_engine = index.as_query_engine()
    return query_engine


def create_key_word_table_index_query_engine():
    # Load the your data
    documents = SimpleDirectoryReader('./data').load_data()
    index = KeywordTableIndex.from_documents(documents, service_context=service_context)

    # Query and print response
    query_engine = index.as_query_engine()
    return query_engine
