### Step 1: Clone the Repository

First, clone the project repository from the command line:

```
git clone <repo url>
```

### Step 2: Navigate to the Project Directory

Change into the project directory that you just cloned:

```
cd path_to_your_project
```

### Step 3: Create a Virtual Environment

Create a virtual environment named `venv` within the project directory to manage dependencies:

```
python -m venv venv
```

This is very important!

### Step 4: Activate the Virtual Environment

Activate the virtual environment using the correct command for your operating system:

* **Windows:**

```
.\venv\Scripts\activate
```

* **Linux/macOS:**

```
source venv/bin/activate
```

### Step 5: Install Dependencies

Install all the required dependencies from the `requirements.txt` file:

```
pip install -r requirements.txt
```

### Step 6: Start Working on the Project

You're now ready to start working on the project! Remember to activate the virtual environment whenever you begin a new development session. All your dependency paths/versions will be maintained through this virtual envrionment.

### Step 7: Deactivate the Virtual Environment

When you're finished working for the session, deactivate the virtual environment:

```
deactivate
```

## **Notes:**

* Always ensure the virtual environment is activated before running the project or installing new packages to keep your project's dependencies isolated. Please let the team know that you are installing new packages!
* After installing any new packages during development, update `requirements.txt` using `pip freeze > requirements.txt` (within the virtual envrionment) so that other team members can install the same versions.
* You should only be programming with the virtual envrionment activated!
* To run the development server, execute:

```
python manage.py runserver
```

You will need to be in the `CTET` directory to do this.

* To stop the development server, you can simply just do `CTRL+C` in the terminal.

**Always remember to activate the virtual envrionment before running any Django management command or installing new packages with `pip`.**
