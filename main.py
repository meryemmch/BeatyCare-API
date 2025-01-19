from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from routers.search import search_router
from routers.user_management import user_management_router
from routers.report_submission import report_submission_router
from routers.recognized_products import recognized_products_router
from routers.verify_report import verify_report_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/favicon.ico", response_class=Response)
async def favicon():
    return Response(status_code=204)
    

# Include routers from different modules
app.include_router(search_router)
app.include_router(user_management_router)
app.include_router(report_submission_router)
app.include_router(recognized_products_router)
app.include_router(verify_report_router)
