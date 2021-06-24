import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title='Spotify App API',
    description="Predicts songs",
    version="1.0",
    docs_url='/docs'
)


templates = Jinja2Templates(directory="app/templates")

@app.get('/', response_class=HTMLResponse)
def display_index(request: Request):
    """Displays index.html from templates when user loads root URL"""
    return templates.TemplateResponse('index.html', {"request": request})



app.mount("/assets",
          StaticFiles(directory="app/templates/assets"),
          name="assets"
          )


app.mount("/images",
          StaticFiles(directory="app/templates/images"),
          name="images"
          )

app.add_middleware(    CORSMiddleware,    allow_origins=['*'],    allow_credentials=True,    allow_methods=['*'],    allow_headers=['*'],)
if __name__ == '__main__':
    uvicorn.run(app)