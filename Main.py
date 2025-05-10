import streamlit as st

st.set_page_config(page_title="Smart AI Chatbot", layout="centered")


st.title("📚 Smart AI Chatbot: Your Personal Document & Knowledge Assistant")


st.markdown("""
Welcome to **Smart AI Chatbot**, an intelligent assistant that allows you to interact with your documents like never before.
Upload your PDF, ask questions, and receive accurate, real-time answers powered by cutting-edge open-source AI models.
""")


st.markdown("### 💡 Key Features:")
st.markdown("""
- **📄 Document Understanding via PDF Upload**  
  Upload your PDFs easily. We extract and analyze the content for intelligent querying.

- **🧠 Open Source Intelligence (Groq + LangChain)**  
  Experience the speed and accuracy of Groq’s LLMs combined with Langchain’s orchestration capabilities.

- **🔍 Semantic Search with Hugging Face Embeddings + FAISS**  
  Get semantically relevant answers using industry-standard embedding and vector storage techniques.

- **⚡ Real-Time Interaction**  
  Ask questions and get answers from your documents instantly using a clean and intuitive UI.

- **🔄 Multi-File Processing (Expandable)**  
  Built for scale — handle multiple documents effortlessly.
""")


st.markdown("### 🚀 Get Started Below:")
st.info("Go to chatbot section for the answering of your questions.")