from contextlib import asynccontextmanager

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.config import settings
from app.database import Base, engine
from app.graphql.schema import get_graphql_context, schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

graphql_app = GraphQLRouter(schema, context_getter=get_graphql_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {
        "message": settings.app_name,
        "graphql": "/graphql",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
