from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.rag.loader import load_txt_document

def split_documents(
        documents : list[Document],
        chunk_size :int = 300,
        chunk_overlap :int = 50#相邻chunks保留约50个字符重叠，确保关键语义不容易被切断
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_overlap = chunk_overlap,
        chunk_size = chunk_size
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ =="__main__":

    path  = "/Users/sunflower_zlf/AI_Data_Analyst_Agent_System/data/knowledge/business_rules.txt"

    documents = load_txt_document(path)

    chunks = split_documents(documents,100,20)

    print("原始文档数量：",len(documents))
    print("chunk数量：",len(chunks))

    for i,context in enumerate(chunks):#枚举，分别提取位置信息和内容
        print(f"\n=====Chunk{i+1}=====")
        print(context.page_content)
        print(context.metadata)

