### README.md

# Flask Blog Web Application

A feature-rich blog website built with Flask, providing functionalities for secure user authentication, profile management, blog post creation, and email verification. The project demonstrates best practices in Flask development, secure authentication, and user experience design.

## Overview

This project was developed as part of my Student Industrial Work Experience Scheme (SIWES) at CodesPro Solutions. It is a Flask-based web application that allows users to register, log in, verify their email, and create blog posts. Users can also manage their profiles and explore posts by other users. The site is designed with a responsive UI and uses Bootstrap for enhanced styling.

## Key Features

- **User Authentication**: Secure login and registration system for users.
- **Email Verification**: Confirmation email sent to users upon registration.
- **Profile Management**: Users can update their profile details and upload a profile picture.
- **Post Management**: Users can create, update, delete, and view blog posts.
- **Pagination**: Blog posts are paginated for efficient viewing.
- **Notifications**: Flash messages for user actions and feedback.
- **Google OAuth 2.0**: Planned feature for secure user login through Google.

## Technical Details

- **Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, Bootstrap
- **Email Service**: Flask-Mail for email functionalities
- **Deployment**: Suitable for Heroku or AWS

## Project Structure

BLOG/
│
├── blog/
│   ├── __init__.py
│   ├── routes.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   └── static/
│
├── config.py
├── run.py
├── README.md
└── LICENSE


## Installation and Setup

1. **Clone the Repository**:

   git clone https://github.com/joshdammy22/BLOG.git
   cd BLOG


2. **Set Up Virtual Environment**:

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. **Install Dependencies**:
   pip install -r requirements.txt

4. **Set Up Environment Variables**:
   Configure environment variables in a `.env` file (refer to `.env.example` for required variables).

5. **Initialize Database**:
  
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade


6. **Run the Application**:

   flask run


## Usage

1. Register a new account and verify it through the email link.
2. Log in to access the dashboard, manage your profile, and start posting content.
3. (Future feature) Use Google Login for streamlined access.

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.


