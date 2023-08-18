# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:20:54 2023

@author: tomah
"""

from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

load_dotenv()

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def read_documents_from_directory(directory):
    combined_text = ""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            combined_text += read_pdf(file_path)
        
    return combined_text

train_directory = 'Handbook/'
text = read_documents_from_directory(train_directory)


def process_pdf_query(query):
    

    # split into chunks
    char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, 
                                          chunk_overlap=200, length_function=len)

    text_chunks = char_text_splitter.split_text(text)
    
    # create embeddings
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(text_chunks, embeddings)
    
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")


    # process user query
    docs = docsearch.similarity_search(query)
    
    response = chain.run(input_documents=docs, question=query)
    return response
 

