import psycopg
from psycopg.rows import dict_row
from pwdlib import PasswordHash
from getpass import getpass
from backend.config import settings



password_hasher = PasswordHash.recommended()
DUMMY_HASH = password_hasher.hash("dummy-password")


#create user functions:
def hash_password(password):
    saved_hash = password_hasher.hash(password)
    return saved_hash


def create_user(connection, username, password):
    password_hash = hash_password(password)

    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username;",
                       (username, password_hash)
                       )

        new_user = cursor.fetchone()
        return new_user


#check user functions:
def check_password(entered_password, saved_hash) -> bool:
    is_valid = password_hasher.verify(entered_password, saved_hash)
    return is_valid


def get_user_by_username(connection, username):
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s;",
                       (username,),
                       )

        user = cursor.fetchone()
        return user


def get_user_by_id(connection, user_id: int) -> dict | None:
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT id, username FROM users WHERE id = %s;",
                       (user_id,),
                       )
        user = cursor.fetchone()
        return user


def auth_user(connection, username, password):
    """auth user and return id and username if success or return None if false"""
    full_user_info = get_user_by_username(connection, username)
    if full_user_info is None:
        check_password(password, DUMMY_HASH)
        return None

    password_check = check_password(password, full_user_info["password_hash"])
    if password_check:
        return {
            "id": full_user_info["id"],
            "username": full_user_info["username"],
        }
    
    return None


#tasks proccess functions
def get_task(connection, user_id, task_id):
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT id, task, status FROM tasks WHERE user_id = %s AND id = %s;",
                        (user_id, task_id,),
                        )

        task = cursor.fetchone()
        return task 


def get_tasks(connection, user_id, status=None):
    with connection.cursor(row_factory=dict_row) as cursor:
        if status is not None:
            cursor.execute("SELECT id, task, status FROM tasks WHERE status = %s AND user_id = %s ORDER by id;",
                           (status, user_id,),
                           )
        else:
            cursor.execute("SELECT id, task, status FROM tasks WHERE user_id = %s ORDER by id;",
                           (user_id,),
                           )

        tasks = cursor.fetchall()
        return tasks


def create_task(connection, user_id, task):
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("""INSERT INTO tasks (task, status, user_id) VALUES (%s, 'active', %s)
                        RETURNING id, task, status;""",
                        (task, user_id,),
                        )
        
        result = cursor.fetchone()
        return result


def complete_task(connection, user_id, task_id):
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute("""UPDATE tasks SET status = 'completed'
                        WHERE id = %s AND user_id = %s RETURNING id, task, status;""",
                       (task_id, user_id,),
                       )

        result = cursor.fetchone()
        return result


#connection to data base:
def create_connection():
    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password.get_secret_value(),
        connect_timeout=5,
    )


