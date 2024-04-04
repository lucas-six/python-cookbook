# Web Frameworks: FastAPI

## Installation

```bash
# MQ: RabbitMQ/MongoDB/Redis
pipenv install pika
pipenv install types-pika

# Task Queue: Celery
pipenv install celery[librabbitmq, mongodb, redis]
```

## MongoDB

```python
import os

from motor.motor_asyncio import AsyncIOMotorClient

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'name': 'Lee',
            }
        }


class UpdateStudentModel(BaseModel):
    name: str | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'name': 'Lee',
            }
        }


@router.post('/', response_description='Add new student', response_model=StudentModel)
async def create_student(request: Request, student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    coll = request.app.mongodb_db['students']
    new_student = await coll.insert_one(student)
    created_student = await coll.find_one({'_id': new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@router.get(
    '/', response_description='List all students', response_model=list[StudentModel]
)
async def list_students(request: Request):
    coll = request.app.mongodb_db['students']
    return await coll.find().to_list(1000)


@router.get(
    '/{student_id}', response_description='Get a single student', response_model=StudentModel
)
async def show_student(request: Request, student_id: str):
    coll = request.app.mongodb_db['students']
    if (student := await coll.find_one({'_id': student_id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f'Student {student_id} not found')



@router.put('/{student_id}', response_description='Update a student', response_model=StudentModel)
async def update_student(
    request: Request,
    student_id: str,
    student: UpdateStudentModel = Body(...)
):
    student = {k: v for k, v in student.dict().items() if v is not None}
    coll = request.app.mongodb_db['students']

    if len(student) >= 1:
        update_result = await coll.update_one({
            '_id': student_id},
            {'$set': student})

        if update_result.modified_count == 1:
            if (
                updated_student := await coll.find_one({'_id': student_id})
            ) is not None:
                return updated_student

    if (existing_student := await coll.find_one({'_id': student_id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f'Student {student_id} not found')


@router.delete('/{student_id}', response_description='Delete a student')
async def delete_student(request: Request, student_id: str):
    delete_result = await request.app.mongodb_db['students'].delete_one({'_id': student_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Student {student_id} not found')
```
