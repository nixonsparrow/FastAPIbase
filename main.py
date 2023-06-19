from fastapi import FastAPI, HTTPException, Path
from typing import Optional

from pydantic import BaseModel


app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    year: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None


students = {
    1: Student(
        **{
            "name": "john",
            "age": 17,
            "year": 2023
        }
    )
}


@app.get("/")
def homepage():
    return students


@app.get("/get-student/{sid}")
def get_student(sid: int = Path(description="The ID of the student you want to view", gt=0)):
    if sid in students:
        return students[sid]
    raise HTTPException(status_code=404, detail="Data not found")


@app.get("/get-by-name/")
def get_student(*, name: Optional[str] = None):
    for student_id, student in students.items():
        if student.name.casefold() == name.casefold():
            return student
    raise HTTPException(status_code=404, detail="Data not found")


@app.post("/create-student")
def create_student(student: Student):
    students[max(students) + 1] = student
    return student


@app.put("/update-student/{sid}")
def update_student(sid: int, student: UpdateStudent):
    if sid not in students:
        raise HTTPException(status_code=404, detail="Student does not exist")

    if student.name is not None:
        students[sid].name = student.name
    if student.age is not None:
        students[sid].age = student.age
    if student.year is not None:
        students[sid].year = student.year

    return students[sid]


@app.delete("/delete-student/{sid}")
def delete_student(sid: int):
    if sid not in students:
        raise HTTPException(status_code=404, detail="Student does not exist")

    del students[sid]
    return {"Message": f"Student {sid} deleted successfully!"}
