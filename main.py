import uvicorn
from fastapi import FastAPI
from app.routers import authentication, blog, user, vote
from app.dependencies import models
from app.dependencies.database import engine
from fastapi.middleware.cors import CORSMiddleware
# from app.dependencies.path_metadata import tags_metadata

app = FastAPI(
    title="Simple CRUD App",
    description='A simple blog to demonstrate CRUD operation with FastAPI',
    summary="Create users, posts",
    version="0.0.1",
    terms_of_service="http://terms_of_service.com/terms/",
    contact={
        "name": "Nkereuwem Udoudo",
        "url": "http://www.nkereuwem.udoudo.com/contact/",
        "email": "nkereuwem.udoudo1@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # openapi_tags=tags_metadata
)

origins = [
    "*",
    "https://www.google.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(vote.router)

# models.Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Root'])
async def root():
    return {'detail': 'welcome to my API'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)