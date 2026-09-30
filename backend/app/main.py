from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from app.data import SHUTTLE_SESSIONS
from app.schemas import ShuttleSessionCreate, ShuttleSessionResponse, PaginatedShuttleResponse

app = FastAPI(title="Campus Shuttle Session API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

next_id = len(SHUTTLE_SESSIONS) + 1


@app.get("/sessions", response_model=PaginatedShuttleResponse)
def get_sessions(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: str = Query("")
):
    filtered_data = SHUTTLE_SESSIONS

    if search:
        search_lower = search.lower()
        filtered_data = [
            item for item in SHUTTLE_SESSIONS
            if search_lower in item["passenger_name"].lower() or search_lower in item["route"].lower()
        ]

    total = len(filtered_data)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = filtered_data[start_idx:end_idx]

    return {
        "data": paginated_data,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/sessions/{session_id}", response_model=ShuttleSessionResponse)
def get_session_by_id(session_id: int):
    session = next((s for s in SHUTTLE_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.post("/sessions", response_model=ShuttleSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_data: ShuttleSessionCreate):
    global next_id
    new_session = session_data.model_dump()
    new_session["id"] = next_id
    next_id += 1
    
    SHUTTLE_SESSIONS.append(new_session)
    return new_session


@app.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int):
    index = next((i for i, s in enumerate(SHUTTLE_SESSIONS) if s["id"] == session_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    SHUTTLE_SESSIONS.pop(index)
    return None