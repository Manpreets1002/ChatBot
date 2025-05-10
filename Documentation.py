import streamlit as st

st.title("Documentation")
st.subheader("""1. User Interface (Frontend Layer)""")
st.write("""\tTool Used: Streamlit

\tPurpose: Acts as the front-facing UI for users to interact with the chatbot.

\tFunctions:

\t\tDisplay chat history and input field for user queries.

\t\tProvide a file uploader for PDF files.

\t\tDisplay real-time responses from the chatbot.""")

st.subheader("2. Language Model Processing")
st.write("""\tTools Used: Langchain + Groq (for LLM execution)

\tPurpose: To handle prompts, memory, and manage model responses.

\tSteps:

\t\tLangchain manages chains and prompts for handling chat flow and summarization.

\t\tGroq serves as the high-performance backend for open-source LLMs.

\t\tEach user message is passed through Langchain's prompt templates to format input appropriately.

\t\tGroq executes the prompt with the selected open-source LLM and returns a response.""")

st.subheader("3. File Upload and Document Processing")
st.write("""\tTools Used: Streamlit (UI), PyPDFLoader (Loader), Hugging Face Embeddings, FAISS:

\tTo allow users to upload PDFs, retrieve content, and answer questions from the file.

\tSteps:

\t\tPDF Upload: Streamlit’s file uploader accepts the user’s PDF document.

\t\tDocument Loading: PyPDFLoader reads and splits the PDF content.

\t\tEmbedding Generation: Hugging Face Embeddings converts document chunks into vector format.

\t\tVector Store: FAISS stores these vectors and allows fast similarity search during question-answering.

\tQuery Processing:

\t\tUser asks a question based on the PDF.

\t\tThe question is vectorized and compared with stored chunks using FAISS.

\t\tTop-matching chunks are retrieved and passed to the LLM via Langchain for context-aware response generation.""")

st.subheader("4. Response Management")
st.write("""\tTool Used: Langchain

\tPurpose: To format and summarize model responses, handle session memory, and maintain history.

\tFeatures:

\t\tStores interaction context (memory).

\t\tHandles summarization of uploaded documents.

\t\tEnsures consistent interaction with the model.""")