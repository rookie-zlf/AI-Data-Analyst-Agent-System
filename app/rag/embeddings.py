from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs = {
            "device":"cpu"
        },
        encode_kwargs = {
            "normalize_embeddings":True
        }
    )

    return embeddings



if __name__ == "__main__":

    embeddings = create_embeddings()

    text = "GMV的定义是什么？"

    vector = embeddings.embed_query(text)

    print("向量维度：",len(vector))

    print("前十个向量值:",vector[:10])

    


