import uuid
from pydantic import BaseModel, Field

class UserCreateTelegramDTO(BaseModel):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)