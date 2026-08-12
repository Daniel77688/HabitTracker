from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models.database import init_db
from src.controllers import habit_controller, habit_log_controller, users_controller, streak_controller, auth_controller

init_db()

app = FastAPI(title="Habit Tracker API", version="1.0.0", description="API REST for managing habits and streaks")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(habit_controller.router)
app.include_router(habit_log_controller.router)
app.include_router(users_controller.router)
app.include_router(streak_controller.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Habit Tracker. Go to /docs to view the interactive documentation."}