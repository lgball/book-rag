from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata


class ChapterChat:
    def __init__(self, text_splitter, vector_store, chat_model, document_loader, runnable, prompt):
        self.text_splitter = text_splitter
        self.vector_store = vector_store
        self.chat_model = chat_model
        self.document_loader = document_loader
        self.runnable = runnable
        self.prompt = prompt


    def run(self, input):

        chapters = self.vector_store.retrieve(input)

        chapters = filter_complex_metadata(chapters)

        for chapter in chapters:
            chapter = self.runnable.run(chapter)
            chapter = self.chat_model.run(chapter)

    def run_prompt(self, input):
        return self.prompt.run(input)