import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import validators
load_dotenv()
st.set_page_config("Summarize")

st.title("ChatBot🤖")

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="Llama3-8b-8192",groq_api_key=api_key)

user_url = st.text_input("URL",label_visibility="collapsed")

prompt_template="""Provide a summary of the following content in 300 words:
Content: {text}"""

prompt = PromptTemplate(template=prompt_template,input_variables=["text"])


if st.button("Summarize the Content"):
    if not user_url.strip():
        st.error("Please provide the URL to get started")
    elif not validators.url(user_url):
        st.error("Please provide a Valid URL")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in user_url:
                    loader = YoutubeLoader.from_youtube_url(user_url,add_video_info=False)   
                else:
                    loader = UnstructuredURLLoader([user_url],ssl_verify=False,headers={"Authorization": "Bearer YOUR_API_KEY","Content-Type": "application/json"})
                
                docs = loader.load()
                chain = load_summarize_chain(llm,chain_type="stuff",prompt=prompt)  
                response = chain.run(docs)

                st.success(response)
        except Exception as e:
            st.exception(e)
            