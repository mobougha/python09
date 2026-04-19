# Python 09: Cosmic Data Concepts (Pydantic v2)

This module focuses on data validation using **Pydantic v2**. Pydantic is a data validation and settings management library that uses Python type annotations to enforce data schemas.

## 1. BaseModel
The `BaseModel` is the primary class for creating validated data structures. When you inherit from it, Pydantic automatically handles the parsing and validation of input data.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "Anonymous"
```

## 2. Field
The `Field` function allows you to add specific constraints, metadata, and default values to your model's attributes.

- **Constraints**: `gt`, `ge`, `lt`, `le` (for numbers), `min_length`, `max_length` (for strings/lists).
- **Metadata**: `description`, `title`.
- **Default**: `default`, `default_factory`.

```python
from pydantic import BaseModel, Field

class Station(BaseModel):
    crew_size: int = Field(ge=1, le=20, description="Number of crew members")
```

## 3. Enums
Using Python's `Enum` class ensures that a field only accepts a specific set of values. Pydantic validates that the input matches one of the enum members.

```python
from enum import Enum

class Rank(Enum):
    CADET = "cadet"
    COMMANDER = "commander"
```

## 4. model_validator
In Pydantic v2, `@model_validator` replaces the old `@validator` and `@root_validator`.
- **mode='after'**: The validator runs after Pydantic has validated the individual fields. This is usually where you put cross-field validation logic.
- **Important**: You must return `self` at the end.

```python
from pydantic import BaseModel, model_validator

class Contact(BaseModel):
    type: str
    is_verified: bool

    @model_validator(mode='after')
    def check_physical_contact(self) -> 'Contact':
        if self.type == "physical" and not self.is_verified:
            raise ValueError("Physical contact must be verified")
        return self
```

## 5. Type Annotations & Type Hints
- **Strong Typing**: Python 3.10+ features like `|` for unions (e.g., `str | None`) are preferred over `Optional[str]`.
- **Mypy**: Used to perform static type checking. All functions should have return type hints (e.g., `def main() -> None:`).

## 6. Datetime Handling
Pydantic automatically converts ISO-formatted strings (e.g., `"2024-04-19T10:00:00"`) into Python `datetime` objects.

## 7. Nested Models
Models can be used as types within other models. This allows for complex, hierarchical data structures.

```python
class Mission(BaseModel):
    crew: list[CrewMember]
```

## 8. Error Handling
Pydantic raises a `ValidationError` when data fails to meet the schema. This error object contains detailed information about which fields failed and why.
