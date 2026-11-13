from pydantic import BaseModel,Field
from pydantic import field_validator
from typing import Literal


class AnalysisTaskRequest(BaseModel):
    """gt 是 greater than(大于) 的缩写。Field(gt=0) 表示这个字段的值必须大于 0,
    所以 dataset_id: int = Field(gt=0) 
    的意思是:dataset_id 必须是整数,而且是正整数。
    ge:大于等于(greater than or equal)
    lt:小于(less than)
    le:小于等于(less than or equal)"""
    dataset_id :int = Field(gt=0)  

    top_k:int = Field(default=5,ge=1,le=20)

    question :str = Field(min_length=1,max_length=200)#没有提供默认值，question 就是必填字段

    @field_validator("question",mode = "before")
    @classmethod
    def validate_question(cls,value):
        if isinstance(value,str):
            return value.strip()
        return value
     
    
  

class AnalysisTaskResponse(BaseModel):
    task_id : str
    dataset_id :int
    status :Literal['pending'] #status: str 允许任意字符串,status: Literal['pending'] 则只允许字符串 "pending"

    





