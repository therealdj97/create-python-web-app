import os
import pathlib
import subprocess
import argparse
import questionary

# Check if questionary is installed, if not, install it
try:
    import questionary
except ImportError:
    print("Installing 'questionary' library...")
    subprocess.run(["pip", "install", "questionary"])

    # Retry import after installation
    try:
        import questionary
    except ImportError:
        raise ImportError("Failed to install 'questionary'. Please install it manually using 'pip install questionary'.")

def create_folder_structure(project_name, framework):
    base_path = pathlib.Path(project_name)

    # Common folder structure
    os.makedirs(base_path / "app" / "api" / "endpoints")
    os.makedirs(base_path / "app" / "core")
    os.makedirs(base_path / "app" / "db" / "models")
    os.makedirs(base_path / "app" / "schemas")
    os.makedirs(base_path / "app" / "utils")

    # Create tests folder
    os.makedirs(base_path / "tests" / "test_api")

    # Create necessary files
    for directory in ["app", "app/api", "app/core", "app/db", "app/schemas", "app/utils", "tests"]:
        open(base_path / f"{directory}" / "__init__.py", "w").close()

    # Additional structure based on the framework
    if framework == "django":
        os.makedirs(base_path / project_name / "static")
        os.makedirs(base_path / project_name / "media")
        os.makedirs(base_path / "templates")
        open(base_path / "manage.py", "w").close()

    # Create main script
    main_script_content = """# Your main script content here
"""
    with open(base_path / "app" / "main.py", "w") as main_script:
        main_script.write(main_script_content)

    print(f"Folder structure for {project_name} created successfully.")

def create_virtual_environment(project_name, verbose=False):
    venv_path = pathlib.Path(project_name) / "venv"
    subprocess.run(["python", "-m", "venv", str(venv_path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if verbose:
        print("Virtual environment created successfully.")

def create_requirements_txt(project_name, selected_packages, framework, verbose=True):
    requirements_file_path = pathlib.Path(project_name) / "requirements.txt"

    with open(requirements_file_path, "w") as requirements_file:
        if framework:
            requirements_file.write(f"{framework}\n")
        if selected_packages:
            for package in selected_packages:
                requirements_file.write(f"{package}\n")

    if verbose:
        print("requirements.txt updated successfully.")



def initialize_git_repository(project_name, verbose=False):
    base_path = pathlib.Path(project_name)
    subprocess.run(["git", "init"], cwd=base_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "add", "."], cwd=base_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=base_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if verbose:
        print("Git repository initialized successfully.")

def create_dockerfile(project_name, framework, verbose=False):
    dockerfile_content = """# Dockerfile content based on chosen framework
"""
    if framework == "flask":
        dockerfile_content += """FROM python:3.8-slim

WORKDIR /app

COPY ./app /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
"""
    elif framework == "django":
        dockerfile_content += """FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
"""
    elif framework == "fastapi":
        dockerfile_content += """FROM python:3.8-slim

WORKDIR /app

COPY ./app /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    else:
        dockerfile_content += "# Unsupported framework"

    with open(pathlib.Path(project_name) / "Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    if verbose:
        print("Dockerfile created successfully.")

def create_gitignore(project_name, verbose=False):
    gitignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
venv/
"""
    with open(pathlib.Path(project_name) / ".gitignore", "w") as gitignore_file:
        gitignore_file.write(gitignore_content)

    if verbose:
        print(".gitignore created successfully.")

def create_start_script(project_name, framework, verbose=False):
    if framework == "flask":
        start_script_content = """#!/bin/bash

# Start your Flask application
export FLASK_APP=app.main
export FLASK_RUN_HOST=0.0.0

.0
export FLASK_RUN_PORT=8000
flask run
"""
    elif framework == "django":
        start_script_content = """#!/bin/bash

# Start your Django application
python manage.py runserver 0.0.0.0:8000
"""
    elif framework == "fastapi":
        start_script_content = """#!/bin/bash

# Start your FastAPI application with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
"""
    else:
        start_script_content = ""

    with open(pathlib.Path(project_name) / "start.sh", "w") as start_script:
        start_script.write(start_script_content)

    if verbose:
        print("start.sh script created successfully.")

def main():
    parser = argparse.ArgumentParser(description="Setup a web framework project.")
    parser.add_argument("project_name", type=str, help="The name of your project.")
    parser.add_argument("--framework", type=str, choices=["flask", "django", "fastapi"], default=None, help="The web framework to use.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output.")
    
    args = parser.parse_args()

    # Ask the user for the framework if not provided
    if args.framework is None:
        frameworks = ["flask", "django", "fastapi"]
        framework_choice = questionary.select("Choose a web framework:", choices=frameworks).ask()
        args.framework = framework_choice.lower()

    # Ask for additional packages with version numbers
    libraries_by_category = {
        "data_manipulation": [
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "sqlalchemy",
        ],
        "testing": [
            "pytest",
            "pytest-django",
            "pytest-cov",
            "pytest-flask",
            "pytest-fastapi",
        ],
        "nlp": [
            "nltk",
            "spacy",
        ],
        "computer_vision": [
            "opencv-python",
        ],
        "web_scraping": [
            "requests",
            "beautifulsoup4",
        ],
        "async_programming": [
            "celery",
            "redis",
            "aioredis",
            "asyncio",
        ],
        "machine_learning": [
            "scikit-learn",
            "tensorflow",
            "torch",
            "transformers",
        ],
    }

    selected_packages = []
    for category, library_choices in libraries_by_category.items():
        print("--------------->",category, library_choices)
        category_selection = questionary.checkbox(
            f"Select additional {category.replace('_', ' ')} packages:",
            choices=library_choices
        ).ask()
        selected_packages.extend(category_selection)
        print('category_selection: ', category_selection)    
    print("selected_packages",selected_packages)

    create_virtual_environment(args.project_name, args.verbose)
    create_folder_structure(args.project_name, args.framework)
    create_requirements_txt(args.project_name, selected_packages, args.framework, args.verbose)
    initialize_git_repository(args.project_name, args.verbose)
    create_dockerfile(args.project_name, args.framework, args.verbose)
    create_gitignore(args.project_name, args.verbose)
    create_start_script(args.project_name, args.framework, args.verbose)

if __name__ == "__main__":
    main()