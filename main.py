from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.exceptions import add_exception_handlers
from app.routes import auth_router, gym_router, miembro_router, actividad_router, membresia_router, promocion_router, pago_router

app = FastAPI(
    title="Gym API",
    description="API para administración de gimnasios y miembros",
    version="1.0.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)

app.include_router(auth_router.router)
app.include_router(gym_router.router)
app.include_router(miembro_router.router)
app.include_router(actividad_router.router)
app.include_router(membresia_router.router)
app.include_router(promocion_router.router)
app.include_router(pago_router.router)




@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "Gym API"}
