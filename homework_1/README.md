# 📝 Django TODO Application

This is a simple TODO application built with Django. It supports:

- ✔️ Creating TODO items  
- ✏️ Editing existing items  
- ❌ Deleting items  
- 📅 Assigning due dates  
- ✅ Marking tasks as completed  

The project was created as part of an AI-assisted development exercise.

---

## 🚀 Installation (using uv)

### 1. Create a virtual environment
```bash
uv venv
```

Activate it:

```bash
source .venv/bin/activate         # Linux/macOS
.venv\Scripts\Activate.ps1        # Windows
```

### 2. Install Django
```bash
uv pip install django
```

---

## 📦 Project Setup

```bash
django-admin startproject todo_project
cd todo_project
python manage.py startapp todos
```

Enable the app by adding it to  
`todo_project/settings.py` → `INSTALLED_APPS`:

```python
'todos',
```

---

## 🗂️ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ▶️ Run the Application

```bash
python manage.py runserver
```

Default URL:  
**http://127.0.0.1:8000/**

---

## 🧪 Run Tests

```bash
python manage.py test
```

---

## 📁 Main Components

- `models.py` – TODO model  
- `views.py` – Application logic (CRUD)  
- `urls.py` – Routing  
- `templates/` – HTML templates (`base.html`, `home.html`, `todo_form.html`)  
- `forms.py` – Django ModelForm for handling form fields  

---

## 📅 Date Format

The due date field expects the following format:

```
YYYY-MM-DD
```

Example: `2025-12-01`

---

## ✔️ Features Summary

- Create new TODO items  
- Edit existing items  
- Delete items  
- Assign due dates  
- Mark items as resolved  

---

