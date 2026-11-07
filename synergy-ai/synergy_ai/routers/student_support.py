from functools import lru_cache
from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains import RetrievalQA
from synergy_ai.config import settings
from synergy_ai.schemas import CourseQuestion, CourseAnswer

router = APIRouter(prefix="/support", tags=["2. Поддержка студентов"])

@lru_cache(maxsize=1)
def build_qa():
    docs = TextLoader(settings.course_materials_path, encoding="utf-8").load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(
        chunks,
        OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        ),
    )
    llm = ChatOpenAI(
        model=settings.llm_model,
        temperature=0,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    )

@router.post("/ask", response_model=CourseAnswer)
def ask_course(req: CourseQuestion):
    qa = build_qa()
    result = qa.invoke({"query": req.question})["result"]
    return CourseAnswer(answer=result)