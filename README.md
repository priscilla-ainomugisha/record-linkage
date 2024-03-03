# Artificial Intelligence Record Linkage

Welcome to the Artificial Intelligence Record Linkage project! This project aims to link records in HDSS communities within the inspire network present in two different datasets. It facilitates the allocation and linking of common data between the HDSS dataset and the facility dataset.

## Documentation

For detailed documentation on how to install, use, and contribute to this project, please refer to the [record-linkage.doc](record-linkage.doc) file.

## Requirements

- Python (>=3.6)
- Django (>=3.2)
- pandas (>=1.3)
- numpy (>=1.21)
- asgiref (>=3.4)
- background-task (>=1.2)

## Installation

1. Clone the repository from GitHub.
2. (Optional) Create and activate a virtual environment.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Apply migrations to set up the database with `python manage.py migrate`.

## Running the Application

Execute the following command in the terminal:

```
uvicorn record_project.asgi:application
```

The Django application will be accessible at `http://127.0.0.1:8000/`.

