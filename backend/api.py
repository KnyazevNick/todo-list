from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pathlib import Path
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from backend import db, auth


app = FastAPI()
path = Path(__file__).parent /'todolist.json'
bearer_scheme = HTTPBearer(auto_error=False)



#user check:
class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=1)
    password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),

    ] = Field(min_length=1)


class UserRead(BaseModel):
    id: int
    username: str


class TokenRead(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


#task check:
class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    task: str = Field(min_length=1)


class TaskRead(BaseModel):
    id: int
    task: str
    status: Literal["active", "completed"]



#API:

#user proccess:
@app.post("/register", response_model=UserRead, status_code=201)
def register_user(new_user: User):
    with db.create_connection() as connection:
        return db.create_user(connection, new_user.username, new_user.password)


@app.post("/login", response_model=TokenRead)
def login_user(user: User):
    with db.create_connection() as connection:
        check_result = db.auth_user(connection, user.username, user.password)
        if check_result is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        else:
            token = auth.create_access_token(check_result["id"])
            return {
                "access_token": token,
                "token_type": "bearer",
            }


def get_current_user(
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer_scheme),
        ]
    ) -> dict:

    auth_error = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise auth_error
    
    else:

        payload = auth.decode_access_token(credentials.credentials)
    if payload is None:
        raise auth_error

    else:
        try:
            user_id = int(payload["sub"])
        except (ValueError, TypeError):
            raise auth_error
        else:
            with db.create_connection() as connection:
                user = db.get_user_by_id(connection, user_id)
                if user is None:
                    raise auth_error
                else:
                    return user


#task proccess:
@app.get('/tasks') 
def get_tasks(current_user: Annotated[dict, Depends(get_current_user)], status_filter: Literal["active", "completed"] | None = None):
    with db.create_connection() as connection:
        return db.get_tasks(connection, current_user["id"], status_filter)


@app.get('/tasks/{task_id}', response_model=TaskRead)
def get_task(current_user: Annotated[dict, Depends(get_current_user)], task_id: int):
    with db.create_connection() as connection:
        result = db.get_task(connection, current_user["id"], task_id)

        if result is None:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            return result


@app.post('/tasks', response_model=TaskRead)
def add_task(current_user: Annotated[dict, Depends(get_current_user)], new_task: TaskCreate):
    with db.create_connection() as connection:
        return db.create_task(connection, current_user["id"], new_task.task)


@app.patch('/tasks/{task_id}/complete', response_model= TaskRead)
def complete_task(current_user: Annotated[dict, Depends(get_current_user)], task_id: int):
    with db.create_connection() as connection:

        result = db.complete_task(connection, current_user["id"], task_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            return result
