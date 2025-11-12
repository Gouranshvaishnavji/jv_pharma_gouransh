from fastapi import FastAPI

# 1. Create the app instance (like 'const app = express()')
app = FastAPI()


# 2. Define a route (like 'app.get("/", ...)')
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# You can add more routes
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "Sample Item"}