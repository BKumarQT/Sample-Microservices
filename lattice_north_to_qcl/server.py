import uvicorn

if '__main__' == __name__:
    uvicorn.run("app.main:app", host='0.0.0.0', port=8001 , reload=True)


