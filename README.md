# MAD2 Hospital Management App

A full-stack **Hospital Management System** designed to streamline the management of patients, doctors, appointments, prescriptions, and treatment records through a centralized web application.

The system helps reduce manual record-keeping, prevent appointment scheduling conflicts, and provide patients and doctors with organized access to essential healthcare information.

---

##  Problem Statement

Hospitals often rely on manual registers or disconnected software systems to manage patients, doctors, appointments, and treatment records.

This can lead to:

- Difficulty maintaining patient records
- Appointment scheduling conflicts
- Time-consuming manual processes
- Limited access to patient history
- Difficulty tracking prescriptions and treatments
- Lack of centralized information

The **MAD2 Hospital Management App** addresses these challenges by providing a centralized platform for managing hospital operations.

---

##  Key Features

###  Doctor Management
- Doctor registration and authentication
- Manage doctor profiles
- Specify medical specialization
- Manage availability and appointment schedules
- View assigned appointments
- Maintain patient treatment information

###  Patient Management
- Patient registration and login
- View available doctors
- Search doctors based on specialization
- View doctor availability
- Book appointments
- Cancel appointments
- View appointment history
- Access prescriptions and treatment reports

###  Appointment Management
- Schedule appointments based on doctor availability
- Prevent conflicting appointments
- Appointment status tracking
- Appointment cancellation
- Appointment-day reminders

###  Prescription & Treatment Management
- Doctors can create prescriptions
- Record treatment details
- Maintain patient treatment history
- Patients can view their prescriptions and reports

###  Reports
- Generate monthly appointment reports
- Export appointment data in **CSV format**
- View relevant patient and appointment information

###  Authentication & Authorization
- Secure user authentication
- Role-based access for different users
- Separate dashboards for patients and doctors
- Protected application routes

---

##  Tech Stack

### Frontend
- **Vue.js**
- HTML5
- CSS3
- JavaScript

### Backend
- **Python**
- **Flask**
- Flask extensions and REST APIs

### Database
- **MySQL**

### Background Tasks
- **Celery**
- **Redis**
- Celery Beat

### Development Tools
- Git
- GitHub
- VS Code
- Postman

---

##  System Architecture

```text
                    ┌──────────────────────┐
                    │       Frontend       │
                    │       Vue.js         │
                    └──────────┬───────────┘
                               │
                               │ HTTP / API
                               ▼
                    ┌──────────────────────┐
                    │       Backend        │
                    │       Flask          │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │     MySQL       │       │ Celery + Redis  │
        │    Database     │       │ Background Jobs │
        └─────────────────┘       └─────────────────┘
```

---

##  Project Structure

```text
Mad2-Hospital-management-App/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── controllers/
│   ├── tasks/
│   ├── config/
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── views/
│   ├── router/
│   └── ...
│
├── requirements.txt
├── README.md
└── ...
```

> The exact structure may vary depending on the current project implementation.

---

##  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pratikranjan6/Mad2-Hospital-management-App.git
```

```bash
cd Mad2-Hospital-management-App
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

---

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure the Database

Create a MySQL database and configure the database credentials in the application's configuration/environment file.

Example:

```env
DATABASE_URL=mysql://username:password@localhost/hospital_management
```

> Keep sensitive credentials such as database passwords and API keys in environment variables. Do not commit them to GitHub.

---

### 5. Start Redis

Make sure Redis is running locally.

```bash
redis-server
```

---

### 6. Start Celery

Run the Celery worker:

```bash
celery -A <your_celery_app> worker --loglevel=info
```

For scheduled/background tasks, start Celery Beat:

```bash
celery -A <your_celery_app> beat --loglevel=info
```

> Replace `<your_celery_app>` with the Celery application used in your project.

---

### 7. Run the Flask Backend

```bash
python app.py
```

depending on the project configuration.

---

### 8. Run the Vue Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

---

##  Application Workflow

```text
Patient
   │
   ├── Register / Login
   │
   ├── Search Doctor
   │
   ├── Check Availability
   │
   ├── Book Appointment
   │
   ├── Receive Reminder
   │
   └── View Prescription & Treatment History


Doctor
   │
   ├── Login
   │
   ├── Manage Availability
   │
   ├── View Appointments
   │
   ├── Manage Patient Treatment
   │
   └── Create Prescription
```

---

##  Appointment System

The appointment module allows patients to:

1. Select a medical specialization
2. View available doctors
3. Check doctor availability
4. Select an available appointment slot
5. Book the appointment
6. Cancel the appointment when required
7. View appointment history

The system is designed to reduce scheduling conflicts by considering doctor availability and existing appointments.

---

##  Automated Notifications

The application uses **Celery and Redis** to handle background tasks such as scheduled email notifications.

For example:

```text
Celery Beat
     │
     ▼
Scheduled Task
     │
     ▼
Check Upcoming Appointments
     │
     ▼
Send Reminder Email
```

This allows time-consuming or scheduled operations to run independently from the main web application.

---

##  Future Improvements

Potential improvements include:

-  Real-time notifications
-  Responsive mobile-first interface
-  Online payment integration
-  Electronic health record enhancements
-  Advanced hospital analytics
-  AI-assisted medical data analysis
-  More advanced notification workflows
-  Cloud deployment
-  Enhanced security and audit logging

---

##  Security Considerations

The application should follow standard security practices including:

- Password hashing
- Secure authentication
- Role-based authorization
- Environment variables for secrets
- Input validation
- SQL injection prevention
- Secure API endpoints
- Protection of sensitive patient information

---

##  Learning Outcomes

This project provided practical experience in:

- Full-stack web development
- Flask backend development
- REST API design
- Vue.js frontend development
- Database design and management
- Authentication and authorization
- Appointment scheduling logic
- Background task processing
- Celery and Redis
- Email automation
- Git and GitHub collaboration

---

##  Contributors

Developed as part of the **Modern Application Development – II (MAD2)** project.

**Pratik Ranjan Bishwal**  
Computer Science & Data Science Student

---

##  License

This project is developed for **educational purposes**.

---

##  Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
