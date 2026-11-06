# Zoo Visitor Statistics API

This is an independent FastAPI project based on the real CSV resource for January, fiscal year 2569. It reads `zoo_visitors_january_2569.csv` from the same folder and returns its rows as JSON.

## Start on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` and run `GET /api/zoo-visitors`. The JSON includes source and dataset details, fiscal year, record count, and the 63 CSV rows. Keep the CSV beside `main.py` when deploying.

## Postman

Import `postman_collection.json` into Postman. The collection sends `GET {{baseUrl}}/api/zoo-visitors` to the local server at `http://127.0.0.1:8000`.

Dataset: https://data.go.th/dataset/zoo-visitors2569
