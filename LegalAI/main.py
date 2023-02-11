import openai
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re


openai.api_key = "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"

class Query(BaseModel):
    query: str


app = FastAPI()

#Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "API is running at 8080/legalaiEng"


@app.post("/legalaiEng")
def legalai(query: Query):
    prompt = "Please answer the above question according to Indian legal laws and regulation and constitution with proper article and Section if available."
    query = query.query + '\n' + prompt
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=query
                                        , max_tokens=3000,
                                        temperature=0.6, )
    advice = response.choices[0].text.strip("\n")
    advice = re.sub('\n', '', advice)
    advice = re.sub('[?]', '', advice)
    advice = re.sub('\xa0', ' ', advice)
    return {"Advice": advice}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
