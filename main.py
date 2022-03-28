import os

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from ck import CKServer

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8888",
    "http://developer-activity-console",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CK_HOST = os.environ.get('CK_HOST')
CK_PORT = os.environ.get('CK_PORT')
CK_USER = os.environ.get('CK_USER')
CK_PASS = os.environ.get('CK_PASS')
CK_DB = os.environ.get('CK_DB')

ck_server = CKServer(CK_HOST, CK_PORT, CK_USER, CK_PASS, CK_DB)


@app.post('/sql/transfer')
async def get_developer_activities(sql: str):
    if not sql:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    result = ck_server.execute_no_params(sql)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
