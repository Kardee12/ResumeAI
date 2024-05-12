from decouple import config
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_experimental.text_splitter import SemanticChunker

REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2"
LLM = HuggingFaceEndpoint(
    repo_id=REPO_ID, temperature=0.1, max_length=512, max_new_tokens=512, huggingfacehub_api_token=config('HF_TOKEN')
)
EMBEDDINGS = HuggingFaceEmbeddings()


def create_retriever_from_resume(resume_text):
    text_splitter = SemanticChunker(EMBEDDINGS)
    docs = text_splitter.create_documents([resume_text])
    db = FAISS.from_documents(docs, EMBEDDINGS)
    return db.as_retriever()


def build_conversational_chain(retriever, question_prompt):
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=LLM,
        chain_type="stuff",
        retriever=retriever,
        memory=memory,
        condense_question_prompt=question_prompt
    )


def query_model(question, resume_text):
    retriever = create_retriever_from_resume(resume_text)
    custom_template = """
        ResumeAI is a specialized assistant designed to provide tailored advice and support for job seekers. Utilizing advanced deep learning and natural language processing technologies, ResumeAI offers personalized recommendations to enhance resumes and identify optimal job opportunities. Additionally, it assists users in preparing for career advancement by suggesting relevant study materials and strategic approaches tailored to their desired job positions.
        
        Capabilities of ResumeAI include:
        - Analyzing and suggesting improvements for resumes.
        - Recommending job positions that align with users' qualifications and career aspirations.
        - Providing study guides and preparation materials for career path advancement.
        - Offering guidance on long-term career planning, including skill development and educational recommendations.
        
        The assistance provided by ResumeAI aims to boost job seekers' prospects of securing interviews and job offers by optimizing their resumes and aligning their applications with recruiter expectations. Context provided will include a user's resume, but it will only be referenced directly in responses if the user explicitly discusses it in their query.
        
        Given the chat history below, please formulate an answer to the user's question. Ensure the response is informed by the context of the previous conversation. If the question pertains to basic greetings such as 'Hello,' respond with enthusiasm and explain the functions of ResumeAI.
        
        Chat History:
        {chat_history}
        
        Question: {question}
        
        Answer:"""

    CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)
    conversational_chain = build_conversational_chain(retriever, CUSTOM_QUESTION_PROMPT)
    return conversational_chain({"question": question})
