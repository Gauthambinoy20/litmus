from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware import (
    ErrorHandlingMiddleware,
    RateLimitMiddleware,
    RequestIDMiddleware,
    TimingMiddleware,
)
from app.api.routes import router
from app.config import get_settings
from app.utils.logger import get_logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    log = get_logger("startup")

    # Load spaCy model
    try:
        import spacy

        spacy.load("en_core_web_sm")
        log.info("spaCy model loaded")
    except Exception as e:
        log.warning("spaCy model not available", error=str(e))

    # Verify NLTK data
    try:
        import nltk

        nltk.data.find("tokenizers/punkt_tab")
        log.info("NLTK data verified")
    except Exception:
        try:
            import nltk

            nltk.download("punkt_tab", quiet=True)
            nltk.download("averaged_perceptron_tagger_eng", quiet=True)
            nltk.download("stopwords", quiet=True)
            log.info("NLTK data downloaded")
        except Exception as e:
            log.warning("NLTK data not available", error=str(e))

    log.info("Litmus API ready")
    yield
    log.info("Litmus API shutting down")


settings = get_settings()

app = FastAPI(
    title="Litmus API",
    description="Dual-axis resume scanner: ATS compatibility + AI detection scoring",
    version=settings.app_version,
    lifespan=lifespan,
)

# Middleware (order matters: outermost first)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"https://litmus.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Litmus API", "version": settings.app_version, "docs": "/docs"}
