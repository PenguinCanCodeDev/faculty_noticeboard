# 🎓 Faculty Noticeboard

A modern, high-fidelity digital noticeboard system designed for educational institutions. This platform allows faculty staff to efficiently disseminate information, attachments, and exam results to students through a clean, intuitive interface.

## ✨ Features

- **Categorized Notices**: Organize information into Exams, Lectures, Events, Results, and General updates.
- **Secure Attachments**: Support for uploading and viewing PDFs, Excel spreadsheets, and more.
- **Password Protection**: Secure sensitive documents (like exam score sheets) with custom view passwords.
- **Timed Expiry**: Set expiry dates for notices to keep the board fresh and relevant.
- **Modern Dashboard**: Dedicated staff dashboard for notice management (CRUD operations).
- **Responsive Design**: Premium UI optimized for both desktop and mobile devices.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Static Assets**: WhiteNoise (for production-ready static file serving)
- **Environment**: Python-dotenv for secure configuration

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PenguinCanCodeDev/faculty_noticeboard.git
   cd faculty_noticeboard
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   *Note: On Windows, use `copy .env.example .env`.*

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser** (for administrative access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**:
   ```bash
   python manage.py run_server
   ```

The application will be accessible at `http://127.0.0.1:8000`.

## 🔒 Security

- Sensitive keys are managed via environment variables.
- Production-ready settings (`DEBUG=False`, `ALLOWED_HOSTS`, etc.) should be configured in `.env`.
- Password-protected notices add an extra layer of privacy for academic results.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.