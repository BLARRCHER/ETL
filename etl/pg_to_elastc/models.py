from typing import Optional, List
from pydantic import BaseModel, validator
from pydantic.fields import Field


class Genre(BaseModel):
    id: str
    name: str


class FullPerson(BaseModel):
    id: str
    full_name: str
    roles: list = []
    film_ids: list = []


class ShortPerson(BaseModel):
    id: str
    name: str = Field(alias='full_name')


class Movies(BaseModel):
    id: str
    rating: Optional[float] = 0
    genre: Optional[List[Genre]] = []
    title: str
    description: Optional[str] = None
    director: Optional[List[str]]
    actors: Optional[List[ShortPerson]] = Field(default_factory=list)
    actors_names: Optional[List[str]] = Field(default_factory=list)
    writers: Optional[List[ShortPerson]] = Field(default_factory=list)
    writers_names: Optional[List[str]] = Field(default_factory=list)

    class Config:
        validate_assignment = True

    @validator('rating')
    def set_rating(cls, rating):
        return rating or 0

    @validator('director')
    def set_name(cls, director):
        return director or []

