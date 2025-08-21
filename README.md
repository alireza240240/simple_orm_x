# Simple ORM with SQLite

This project is a simple ORM (Object Relational Mapper) written in Python, designed for learning and practicing database concepts and object-oriented programming.  
It allows you to define database tables using Python classes and fields, without writing raw SQL queries.

---

## ✨ Features
- Define models as Python classes (Table = Class)
- Supported field types:
  - `IntegerField`
  - `CharField`
- Data validation:
  - `primary_key`
  - `unique`
  - `not null`
  - length restriction (`max_length`)
- Basic CRUD operations:
  - Create table
  - Insert / Update data
  - Fetch data (Get)
  - Delete data
- **Singleton Pattern** for database connection management

---

## 🛠️ Requirements
- Python 3.8+ (tested on Python 3.10)
- SQLite (comes by default with Python)

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/alireza240240/simple_orm_x.git
cd myorm
```

---


## 🚀 Run unit tests

```python
python -m unittest tests/test_models.py
```

---

## 🚀 Example usage:

```python

from base_model import BaseModel
from fields import IntegerField, CharField

class User(BaseModel):
    table_name = "users"
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100, null=False)
    email = CharField(unique=True)

# Create table
User.create_table()

# Insert a user
u = User()
u.id = 1
u.name = "Ali"
u.email = "ali@example.com"
u.save()

# Fetch a user
fetched = User.get(id=1)
print(fetched.name)  # Ali

```

---

## 📊 Test Coverage

For detailed coverage report, see [COVERAGE.md](COVERAGE.md).


