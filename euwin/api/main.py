from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="EUWINNER API",
    description="Lottery Wheeling System",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers from your controllers
from euwin.api.routes import data_controller, analysis_controller, random_numbers_controller, system_controller

app.include_router(data_controller.router, prefix="/api/data", tags=["Data"])
app.include_router(analysis_controller.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(random_numbers_controller.router, prefix="/api/random", tags=["Random Numbers"])
app.include_router(system_controller.router, prefix="/api/system", tags=["System"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "EUWINNER Lottery Wheeling API"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}