from fastapi import FastAPI


app = FastAPI(title='Init')

@app.get('/')
def home():
    return {'message': 'Hello world'}
