from langchain_chroma import Chroma

from app.rag.loader import load_txt_document
from app.rag.splitter import split_documents
from app.rag.embeddings import create_embeddings

if __name__ == "__main__":

    documents = load_txt_document("/Users/sunflower_zlf/AI_Data_Analyst_Agent_System/data/knowledge/business_rules.txt")

    chunks = split_documents(documents,100,20)

    embeddings = create_embeddings()

    vector_store = Chroma(
        collection_name= "business_rules",
        embedding_function = embeddings,
        persist_directory = "data/chroma_db"
    )
    ids = [
        f"business_rules_chunk_{i}" for i in range(len(chunks))
    ]

    vector_store.add_documents(
        documents=chunks,
        ids = ids
    )
    print("成功存储chunks数量：",len(chunks))

    query = "什么样的客户属于VIP？"
    result = vector_store.similarity_search(
        query = query,
        k=1
    )

    for doc in result:
        print("\n检索到内容：",doc.page_content)
        print("\n来源：",doc.metadata)







