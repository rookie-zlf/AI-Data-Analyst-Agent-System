from langchain_chroma import Chroma
from app.rag.embeddings import create_embeddings


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

    retriever = create_retriever()

    query = "什么样的客户能成为vip？"

    documents = retriever.invoke(query)

    for doc in documents:
        print("检索到的内容：",doc.page_content)
        print("信息来源：",doc.metadata)
