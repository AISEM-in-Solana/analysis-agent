from fastapi import FastAPI


app = FastAPI()

@app.get('/report-today/')
def report_today():
    return