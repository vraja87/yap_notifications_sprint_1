from pydantic import BaseModel


class UGCSummary(BaseModel):
    new_likes: int


class Movie(BaseModel):
    id: int
    title: str
    description: str | None = None
    rating: float | None = None


class ContentSummary(BaseModel):
    movies: list[Movie]


class TemplateModel(BaseModel):
    template_name: str
    template_content: str
