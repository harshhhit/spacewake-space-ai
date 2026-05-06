📂 Document Management System

This is a simple yet powerful Django-based document management application. It allows users to upload, categorize, and manage various files. The application provides a clean interface for adding new documents and viewing a history of all uploaded files.
✨ Features

    File Uploads: Easily upload any type of document.

    Categorization: Organize documents by predefined categories like Reports, Contracts, and Proposals.

    Dynamic Storage: Files are automatically saved into folders corresponding to their chosen category.

    Database Integration: Document metadata (title, description, category, etc.) is stored in a database.

    Responsive UI: A modern, dark-themed interface built with Tailwind CSS.

🛠️ Installation and Setup
Prerequisites

    Python 3.x

    Django (You can install this with pip install Django)

Steps

    Clone the repository:

    git clone https://github.com/your-username/your-project-name.git
    cd your-project-name

    (Note: Replace your-username and your-project-name with your actual details.)

    Create a virtual environment (recommended):

    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    Install dependencies:

    pip install Django

    Configure settings.py:
    Make sure your settings.py includes the following for media file handling:

    import os

    # ... other settings ...

    # Base directory of your project
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # URL prefix for media files
    MEDIA_URL = '/media/'

    # Directory where media files will be uploaded and stored
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    Run migrations:

    python manage.py makemigrations
    python manage.py migrate

    Create a superuser:

    python manage.py createsuperuser

    Run the development server:

    python manage.py runserver

    The application will be accessible at http://127.0.0.1:8000.

🚀 Usage
Adding a Document

    Navigate to the Add New Document page (usually /add-document/).

    Fill out the form with a title, description, and select a category and priority.

    Click the "Choose File" button and select the document you wish to upload.

    Click "Save Document."

The file will be uploaded and stored in the media/documents/<category_name>/ directory. The document's metadata will be saved in the database.
Viewing Documents

    On the homepage, you can see a list of all uploaded documents.

    The page provides filters and search functionality to help you find specific documents.

    You can click the View link to open the file in a new tab, Edit to modify its details, or Delete to remove it.