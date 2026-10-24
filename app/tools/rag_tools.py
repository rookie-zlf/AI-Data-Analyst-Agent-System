from langchain_core.tools import tool
from app.rag.retriever import create_retriever

@tool 
def search_knowlege_base(query:str)->str:
    """检索公司业务知识库
    当用户询问GMV定义
    VIP客户标准、产品分类、地区含义或其他业务规划时使用。"""
    retriever = create_retriever(k=2)

    documents = retriever.invoke(query)

    if not documents:
        return f'知识库中没有找到相关的内容。'

    results = []

    for doc in documents:
        content = doc.page_content
        source = doc.metadata.get("filename","未知来源")
        results.append(
            f'来源：{source}\n内容：{content}'
        )

    return "\n\n".join(results)


if __name__ == "__main__":

    result = search_knowlege_base.invoke(
        {
            "query":"vip客户需要满足什么条件？"
        }
    )

    print(result)



