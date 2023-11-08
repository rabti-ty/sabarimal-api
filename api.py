from fastapi import FastAPI, Request, Depends
from fastapi_health import health
import json
from configparser import ConfigParser
from models import ClsQR
import segno
import boto3
from botocore.exceptions import NoCredentialsError
from utils import upload_to_aws

app = FastAPI(
    title="Provider Event Receiver"
)

configur = ConfigParser()
configur.read('config.ini')

async def is_application_reachable():
    return True

@app.get("/health")
async def health():
    return {"status":"Ok"}

@app.post("/sabarimala/genqr")
async def sabrimalagenqr(item: ClsQR.ClsSabarimalaQr):
    try:
        qr_data = item.__repr__()
        qrcode = segno.make_qr(qr_data)
        qrcode.save(
                "testqr1.png",
                scale=3
            )
        upload_to_aws("testqr1.png")
        data = {"msg": item.__repr__()}
    except:
        data = {"status": "Failure", "msg": "Unexpected data received"}
    return data