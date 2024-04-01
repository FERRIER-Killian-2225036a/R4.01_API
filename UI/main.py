from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
app = FastAPI()
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)
# Endpoint pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

# Fonction main
def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)

if __name__ == "__main__":
    main()
