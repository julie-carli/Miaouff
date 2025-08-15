# Miaouff

### Description
Miaouff is a Flask web application to manage animal shelters, animals, pets, products, and users with authentication and admin roles.

---

### Features
- User registration and login with role-based access control (user/admin)
- Admin dashboard to manage shelters, animals, pets, products, and users
- Email verification and password reset via Flask-Mail
- Pagination and search functionalities for user management
- Responsive UI with consistent styling
- Route protection based on user roles

---

### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)
- SMTP server (e.g., Gmail) for sending emails

---

### Installation

```bash
# Clone the repository
git clone https://github.com/julie-carli/miaouff.git
cd miaouff

# Create a virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Configuration
Create a .env file at the project root with the following variables (example for Gmail):

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_super_secure_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///miaouff.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

Database Initialization

# Create database and tables
python setup_db.py

# If using Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Running the Application
flask run
Access the app at http://127.0.0.1:5000/

Usage
Homepage: general presentation
/login: registration and login page 
Admin dashboard (admin role only):

License
This project is licensed under the MIT License. See LICENSE file for details.

Contact
Julie Carli - julie.carli@example.com
GitHub: https://github.com/julie-carli