from pathlib import Path
import shutil

from fastapi import FastAPI,File,UploadFile

#创建后端应用
app = FastAPI(
    title = "AI Data Analyst Agent System"
              )

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(parents=True,exist_ok=True)


@app.get("/")
def root():
    return {
        "message":"AI Data Analyst Agent System is running"
    }

@app.post("/upload")

#需要用户上传一个csv文件
def up_load_csv(
    file : UploadFile = File(...)
):
    #防止文件名里面携带路径
    filename = Path(file.filename).name

    if not filename.lower().endswith(".csv"):
        return {
            "success":False,
            "mesage":"目前只支持CSV文件"
        }
    
    save_path = UPLOAD_DIR / filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "success":True,
        "filename":filename,
        "file_path":str(save_path)
    }