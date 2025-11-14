# simple in-memory session store
session_store = {}

def create_session():
    import uuid
    session_id = str(uuid.uuid4())
    session_store[session_id] = []
    return session_id

def end_session(session_id):
    session_store.pop(session_id, None)

def add_message(session_id, role, content):
    if session_id not in session_store:
        session_store[session_id] = []
    session_store[session_id].append({"role": role, "content": content})

def get_session_history(session_id):
    return session_store.get(session_id, [])
