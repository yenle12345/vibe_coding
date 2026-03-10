from pydantic import BaseModel

class StudentCreate(BaseModel):
    student_id: str
    name: str
    birth_year: int
    major: str
    gpa: float
    class_id: str
class ClassBase(BaseModel):
    class_id: str
    class_name: str
    advisor: str