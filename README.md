# Murang'a University Asset Management System

A comprehensive web-based asset management system designed for Murang'a University of Technology to efficiently track, manage, and monitor institutional assets across departments.

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

The Asset Management System provides a centralized platform for tracking university assets including computers, laboratory equipment, furniture, vehicles, and more. The system features real-time analytics, maintenance tracking, and comprehensive reporting capabilities.

## ✨ Key Features

- **Asset Management**: Add, update, and track all institutional assets
- **Department Management**: Organize assets by departments and locations
- **Asset Movements**: Track asset transfers between departments
- **Maintenance Records**: Log and monitor maintenance activities
- **Analytics Dashboard**: Real-time statistics and visualizations
- **User Management**: Role-based access control
- **Report Generation**: Export data and generate reports
- **Responsive Design**: Mobile-friendly interface

## 🚀 Technology Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5.3, Chart.js
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Icons**: Bootstrap Icons
- **Python**: 3.8+

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mut-asset-management.git
cd mut-asset-management
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Load sample data (optional)**
```bash
python manage.py seed_data
```

7. **Create a superuser**
```bash
python manage.py createsuperuser
```

8. **Run the development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Open your browser and navigate to `http://localhost:8000`
- Login with your superuser credentials

## 🗂️ Project Structure

```
mut-asset-management/
├── assets/                 # Main application
│   ├── management/        # Management commands
│   │   └── commands/
│   │       └── seed_data.py
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   │   └── assets/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       └── login.html
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   └── urls.py            # URL routing
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## 📊 Database Models

- **Department**: University departments and their details
- **AssetCategory**: Categories for organizing assets
- **Asset**: Main asset information and tracking
- **AssetMovement**: Asset transfer history
- **MaintenanceRecord**: Maintenance logs and records

## 🔐 Default Login Credentials

After running `seed_data` command:

- **Admin Account**
  - Username: `admin`
  - Password: `admin123`

- **Test Users**
  - Usernames: `jkamau`, `gwanjiru`, `pmwangi`, `mnjeri`, `dochieng`
  - Password (all): `password123`

**⚠️ Important**: Change these credentials in production!

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Asset Management
![Assets](screenshots/assets.png)

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Code Formatting
```bash
black .
flake8 .
```

### Database Backup
```bash
python manage.py dumpdata > backup.json
```

## 📝 Usage Guide

1. **Login**: Access the system using your credentials
2. **Dashboard**: View real-time analytics and statistics
3. **Add Assets**: Navigate to "Add Asset" to register new items
4. **Track Movement**: Record asset transfers between departments
5. **Maintenance**: Log maintenance activities and schedules
6. **Reports**: Generate and export asset reports

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Development Team

### Lead Developer
**Steve Ongera**
- Role: Lead Developer & System Architect
- Email: steve.ongera@mut.ac.ke
- GitHub: [@steveongera](https://github.com/steveongera)

### Junior Developer
**Linda Gatwiri**
- Role: Junior Developer
- Email: linda.gatwrir@mut.ac.ke
- GitHub: [@lindagatwrir](https://github.com/lindagatwrir)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Murang'a University of Technology for project support
- Django Framework community
- Bootstrap team for the UI framework
- Chart.js for data visualization

## 📞 Support

For support and queries:
- Email: support@mut.ac.ke
- Phone: +254 XXX XXX XXX
- Website: https://mut.ac.ke

## 🔄 Version History

- **v1.0.0** (2025-01-15)
  - Initial release
  - Core asset management features
  - Dashboard with analytics
  - User authentication and authorization

---

**© 2025 Murang'a University of Technology. All rights reserved.**