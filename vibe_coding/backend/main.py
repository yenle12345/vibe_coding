from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from fastapi.staticfiles import StaticFiles

from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    db = SessionLocal()
    students = db.query(models.Student).options(
        joinedload(models.Student.classroom)
    ).all()
    classes = db.query(models.Class).all()
    db.close()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "students": students, "classes": classes}
    )


@app.get("/add")
def add_page(request: Request):
    db = SessionLocal()

    classes = db.query(models.Class).all()

    return templates.TemplateResponse(
        "add_student.html",
        {
            "request": request,
            "classes": classes
        }
    )


@app.post("/add")
def add_student(
        student_id: str = Form(...),
        name: str = Form(...),
        birth_year: int = Form(...),
        major: str = Form(...),
        gpa: float = Form(...),
        class_id: str = Form(...)
):
    db = SessionLocal()

    student = models.Student(
        student_id=student_id,
        name=name,
        birth_year=birth_year,
        major=major,
        gpa=gpa,
        class_id = class_id
    )

    db.add(student)
    db.commit()

    return RedirectResponse("/", status_code=303)

@app.get("/edit/{student_id}")
def edit_page(student_id: str, request: Request):
    db = SessionLocal()

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    return templates.TemplateResponse(
        "edit_student.html",
        {"request": request, "student": student}
    )

@app.post("/update/{student_id}")
def update_student(
    student_id: str,
    name: str = Form(...),
    birth_year: int = Form(...),
    major: str = Form(...),
    gpa: float = Form(...),
    class_id: str = Form(None)
):
    db = SessionLocal()

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if student:
        student.name = name
        student.birth_year = birth_year
        student.major = major
        student.gpa = gpa
        student.class_id = class_id

        db.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{student_id}")
def delete_student(student_id: str):
    db = SessionLocal()

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return RedirectResponse("/", status_code=303)
@app.get("/classes")
def class_list(request: Request):
    db = SessionLocal()
    classes = db.query(models.Class).all()
    db.close()

    return templates.TemplateResponse(
        "class_list.html",
        {"request": request, "classes": classes}
    )
@app.get("/add_class")
def add_class_page(request: Request):
    return templates.TemplateResponse(
        "add_class.html",
        {"request": request}
    )
@app.post("/add_class")
def add_class(
        class_id: str = Form(...),
        class_name: str = Form(...),
        advisor: str = Form(...)
):

    db = SessionLocal()

    new_class = models.Class(
        class_id=class_id,
        class_name=class_name,
        advisor=advisor
    )

    db.add(new_class)
    db.commit()

    return RedirectResponse("/classes", status_code=303)