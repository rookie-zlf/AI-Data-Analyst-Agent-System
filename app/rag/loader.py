from pathlib import Path
from langchain_core.documents import Document

def load_txt_document(file_path:str) -> list[Document]:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")

    document = Document(
        page_content=text,
        metadata = {
            "source":str(path),
            "filename":path.name
        }
    )

    return [document] #文本切分器通常处理的是：list[document]



if __name__ == '__main__':
    document = "/Users/sunflower_zlf/AI_Data_Analyst_Agent_System/data/knowledge/business_rules.txt"
    documents =  load_txt_document(document)
    print(documents)
    print(documents[0].page_content)
    print(documents[0].metadata)


