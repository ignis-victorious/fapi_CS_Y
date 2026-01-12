#
#  Import FILES
from fastapi import FastAPI

#  Import LIBRARIES
#
#  _______________________

app = FastAPI()


@app.get("/")
def main():
    return {"message": "Hello World"}
