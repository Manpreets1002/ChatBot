import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from prompts import *


load_dotenv()

st.set_page_config("ChatBot🤖")
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    if "store" not in st.session_state:
        st.session_state.store = {}

    #History
    def get_session_history(session_id)->BaseChatMessageHistory:
        if session_id not in st.session_state.store:
            st.session_state.store[session_id] = ChatMessageHistory()
        
        return st.session_state.store[session_id]


    def file_upload(file_uploader):
        temppdf = f'pdfs/{file_uploader.name}'
        with open(temppdf,'wb') as file:
            file.write(file_uploader.getvalue())
        
        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        final_docs = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200).split_documents(docs)
        retriever = FAISS.from_documents(final_docs,HuggingFaceEmbeddings()).as_retriever()

        history_prompt = ChatPromptTemplate.from_messages([
            ("system",history_sys_prompt),
            MessagesPlaceholder("chat_history"),
            ("human","{input}")
        ])

        history_retriever = create_history_aware_retriever(llm,retriever,history_prompt)

        file_prompt = ChatPromptTemplate.from_messages([
            ("system",sys_prompt_file),
            MessagesPlaceholder("chat_history"),
            ("human","{input}")
        ])

        combine_doc = create_stuff_documents_chain(llm,file_prompt)
        rag_chain = create_retrieval_chain(history_retriever,combine_doc)

        chain = RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )

        return chain
    

    llm = ChatGroq(model="Llama3-8b-8192",groq_api_key=api_key)

    #Session ID
    if "name_ss" not in st.session_state:
        st.session_state.name_ss = ["New Chat"]

    ss_id = st.sidebar.selectbox("Chat History",options=st.session_state.name_ss)
    session_id = st.text_input("Session ID",value=ss_id)

    if session_id not in st.session_state.name_ss:
        st.session_state.name_ss.append(session_id)
    
    #File Uploader
    file_uploader = st.sidebar.file_uploader("Upload Your File",type='pdf',accept_multiple_files=False)

    if file_uploader:
        chain = file_upload(file_uploader)
        flag = 1
    else:
        prompt = ChatPromptTemplate.from_messages([
            ("system",sys_prompt),
            MessagesPlaceholder("chat_history"),
            ("human","{input}")
        ])

        conv_chain = prompt | llm

        chain = RunnableWithMessageHistory(
            conv_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )
        flag = 0
    
    if "messages" not in st.session_state:
        st.session_state['messages'] = [
            {"role":"assistant","context":"How can I help you Today!"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["context"])


    #Query
    user_prompt = st.chat_input(placeholder="Ask your Query")

    if user_prompt:
        if session_id == "New Chat":
            name_prompt = ChatPromptTemplate([
                ("system",name_sys_prompt),
                ("human","{input}")
            ])

            name_chain = name_prompt | llm
            session_id = name_chain.invoke(user_prompt).content
            st.session_state.name_ss.append(session_id)
        
        response = chain.invoke({"input":user_prompt},config={"configurable":{"session_id":session_id}})

        if flag == 1:
            st.session_state.messages.append({"role":"user","context":user_prompt})
            st.chat_message('user').write(user_prompt)
            st.session_state.messages.append({"role":"assistant","context":response["answer"]})
            st.chat_message('assistant').write(response["answer"])
        else:
            st.session_state.messages.append({"role":"user","context":user_prompt})
            st.chat_message('user').write(user_prompt)
            st.session_state.messages.append({"role":"assistant","context":response.content})
            st.chat_message('assistant').write(response.content)