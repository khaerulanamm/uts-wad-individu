from pydantic import BaseModel, Field

class ShuttleSessionBase(BaseModel):
    passenger_name: str = Field(..., min_length=2)
    route: str = Field(...)
    departure_time: str = Field(...)
    seat_number: int = Field(..., gt=0)
    status: str = Field(default="Booked")

class ShuttleSessionCreate(ShuttleSessionBase):
    pass

class ShuttleSessionResponse(ShuttleSessionBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedShuttleResponse(BaseModel):
    data: list[ShuttleSessionResponse]
    total: int
    page: int
    limit: int