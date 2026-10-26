from langchain_chroma import Chroma
from app.rag.embeddings import create_embeddings
from functools import lru_cache



@lru_cache(maxsize=4)#
def create_retriever(k :int = 1):
    embeddings = create_embeddings()

    #使用相同的数据库目录和 Collection 名称，相当于重新打开已有的向量数据库
    vector_store = Chroma(
        collection_name="business_rules",
        embedding_function = embeddings,
        persist_directory="data/chroma_db"
    )

    retriever = vector_store.as_retriever(
        search_kwargs = {
            'k' : k
        }
    )

    return retriever


if __name__ == "__main__":
    
    retriever1 = create_retriever(k=2)
    retriever2 = create_retriever(k=2)

    print(retriever1 is retriever2)
    print(create_retriever.cache_info())