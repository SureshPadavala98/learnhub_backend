# StepUpMark LearnHub — Backend

Backend API powering **StepUpMark LearnHub**, an EdTech platform for course discovery, mentor-led learning, student enrollments, certification, and placements.

Built with **Django REST Framework**, backed by **PostgreSQL**, and secured with **JWT authentication**.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Authentication](#authentication)
- [API Overview](#api-overview)
- [Logging](#logging)
- [Media & Static Files](#media--static-files)

---

## Tech Stack

| Layer          | Technology                                              |
|----------------|----------------------------------------------------------|
| Framework      | Django 5.2, Django REST Framework                        |
| Database       | PostgreSQL (via `psycopg2`)                               |
| Auth           | `djangorestframework-simplejwt` (JWT, with token blacklist & rotation) |
| API Schema     | `drf-spectacular` (OpenAPI schema generation)             |
| CORS           | `django-cors-headers`                                     |
| Config         | `django-environ` / `python-decouple` (`.env` based settings) |
| Async / Queue  | `celery`, `redis` (included as dependencies for future background-task support) |
| Images / QR    | `Pillow`, `qrcode` (certificate generation)                |
| Prod Server    | `gunicorn`, `whitenoise`                                   |

---

## Project Structure

```
stepupmark_learnhub_backend/
├── learnhub/                # Project config (settings, root urls, wsgi/asgi)
├── accounts/                # Users, auth, OTP, student profile
│   ├── models/               # User, Profile, PendingRegistration, VerificationOTP
│   ├── services/              # AuthService, OTPService, EmailService
│   └── versioned/v1/          # Versioned serializers, views, urls
├── mentor/                  # Mentor, Course, CourseCategory, CourseInquiry models
├── super_admin/             # Admin-facing platform management
│   ├── models/                # Placement, Certificate(Template), Blog, SiteConfiguration, Enrollment
│   ├── services/               # Certificate generation, QR service, dashboard aggregation
│   └── versioned/v1/           # Admin / mentor / student / blog endpoints
├── common/                  # Shared app (currently scaffolding)
├── core/
│   ├── helpers/                # CustomResponse, CustomPageNumberPagination, role permissions
│   └── utils/                  # Choice fields (enums), abstract CommonModel, BaseAPIView
├── logs/                    # Runtime logs (django.log, error.log, security.log)
├── media/                   # User-uploaded files (profile pics, thumbnails, certificates…)
└── manage.py
```

Every domain app follows the same layered convention:

```
views  →  serializers (validation)  →  services (business logic)  →  models
```

- **`core.helpers.custom_response_hander.CustomResponse`** — standard `{success, message, data}` / `{success, message, errors}` envelope used by every endpoint.
- **`core.utils.common_models.CommonModel`** — abstract base giving every model a UUID primary key, `is_active`, `created_at`, `updated_at`.
- **`core.helpers.permissions`** — role-based permission classes: `IsAdmin`, `IsStudent`, `IsMentor`, `IsAdminOrMentor`, `IsAdminOrStudent`, `IsVerifiedUser`.

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally (or accessible remotely)
- An SMTP account (used for OTP / verification / password-reset emails)

### 1. Clone the repository

```bash
git clone <repo-url>
cd stepupmark_learnhub_backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Fill in `.env` with your local database, email, and CORS settings — see [Environment Variables](#environment-variables) below.

### 5. Create the database

Create a PostgreSQL database matching `DB_NAME` in your `.env`:

```bash
createdb stepupmark_learnhub
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (for Django admin access)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

---

## Environment Variables

All configuration is read from a `.env` file at the project root (see `.env.example`).

| Variable                 | Description                                              | Required |
|---------------------------|------------------------------------------------------------|----------|
| `DEBUG`                   | Django debug mode (`True`/`False`)                          | Yes |
| `SECRET_KEY`               | Django cryptographic secret key                             | Yes |
| `DB_NAME`                  | PostgreSQL database name                                     | Yes |
| `DB_USER`                  | PostgreSQL user                                               | Yes |
| `DB_PASSWORD`               | PostgreSQL password                                           | Yes |
| `DB_HOST`                   | PostgreSQL host                                                | Yes |
| `DB_PORT`                   | PostgreSQL port                                                | Yes |
| `CORS_ALLOWED_ORIGINS`       | Comma-separated list of allowed frontend origins                | Yes |
| `CSRF_TRUSTED_ORIGINS`       | Comma-separated list of trusted origins for CSRF                | Yes |
| `ALLOWED_HOSTS`              | Comma-separated list of allowed hosts                            | Yes |
| `EMAIL_HOST`                 | SMTP host                                                        | Yes |
| `EMAIL_PORT`                 | SMTP port                                                        | Yes |
| `EMAIL_HOST_USER`            | SMTP username                                                    | Yes |
| `EMAIL_HOST_PASSWORD`        | SMTP password                                                    | Yes |
| `EMAIL_USE_TLS`              | Use STARTTLS (`True`/`False`)                                     | Yes |
| `EMAIL_USE_SSL`              | Use SSL (`True`/`False`)                                          | Yes |
| `DEFAULT_FROM_EMAIL`         | Default "From" address for outgoing email                         | Yes |
| `SERVER_EMAIL`               | Address Django uses for error emails                               | Yes |
| `SUPPORT_EMAIL`              | Support contact shown in OTP emails                                 | No (falls back to `DEFAULT_FROM_EMAIL`) |

> **Note:** `.env` is git-ignored. Never commit real credentials — only `.env.example` (with placeholder values) should be tracked.

---

## Authentication

Authentication is JWT-based (`djangorestframework-simplejwt`), with refresh-token **rotation** and **blacklisting** enabled.

- Send the access token as `Authorization: Bearer <access_token>` on protected endpoints.
- Access tokens are short-lived (60 min); refresh tokens last 7 days.
- Every call to `/auth/refresh-token/` blacklists the used refresh token and issues a new access/refresh pair.

**Registration & email verification flow:**

1. `POST /auth/register/` — creates a `PendingRegistration` (no `User` row yet) and returns the user's details.
2. `POST /auth/send_otp/` (`otp_type=EMAIL_VERIFICATION`) — emails a one-time password.
3. `POST /auth/verify_otp/` — verifying the OTP promotes the pending registration into a real, verified `User` and returns JWT tokens.

**Forgot / reset password flow:**

1. `POST /auth/send_otp/` (`otp_type=PASSWORD_RESET`) — emails a one-time password to an existing user.
2. `POST /auth/verify_otp/` (`otp_type=PASSWORD_RESET`) — verifies the OTP.
3. `POST /auth/reset-password/` — sets a new password (`email`, `new_password`, `confirm_password`).

Role-based access is enforced via `role` on the `User` model (`ADMIN`, `MENTOR`, `STUDENT`) combined with the permission classes in `core.helpers.permissions`.

---

## API Overview

All endpoints are prefixed with the host, e.g. `http://127.0.0.1:8000`.

### `/auth/` — Accounts & Authentication

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/auth/register/` | Start registration (creates pending registration) |
| POST | `/auth/login/` | Login with email, password & role |
| POST | `/auth/logout/` | Blacklist a refresh token |
| POST | `/auth/refresh-token/` | Exchange a refresh token for a new access/refresh pair |
| POST | `/auth/reset-password/` | Set a new password after OTP verification |
| POST | `/auth/send_otp/` | Send an OTP (`EMAIL_VERIFICATION`, `PASSWORD_RESET`, `LOGIN_OTP`) |
| POST | `/auth/verify_otp/` | Verify an OTP |
| POST | `/auth/mentor/register/` | Complete mentor profile (authenticated) |
| GET/PUT/PATCH | `/auth/student/profile/` | Get or update the logged-in student's profile |

### `/auth/student/` — Public Student-Facing Content

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/auth/student/testimonials-list/` | List testimonials |
| GET | `/auth/student/courses-list/` | List published courses |
| GET | `/auth/student/course-detail/<course_id>/` | Course detail |
| GET | `/auth/student/student-placements/` | List placements |
| GET | `/auth/student/student-placement-detail/<id>/` | Placement detail |
| GET | `/auth/student/student-certificates/` | List certificates |
| GET | `/auth/student/student-certificate-detail/<id>/` | Certificate detail |

### `/super_admin/` — Blog

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET/POST | `/super_admin/blog-category-createlist/` | List / create blog categories |
| GET/PUT/DELETE | `/super_admin/blog-category-detail/<id>/` | Blog category detail |
| GET/POST | `/super_admin/blog-create-list/` | List / create blog posts |
| GET/PUT/DELETE | `/super_admin/blog-detail/<blog_id>/` | Blog post detail |

### `/super_admin/mentor/` — Mentors & Courses

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/super_admin/mentor/list/` | List mentors |
| GET/PUT | `/super_admin/mentor/detail/<mentor_id>/` | Mentor status / detail |
| GET/POST | `/super_admin/mentor/course-category/` | List / create course categories |
| GET/PUT/DELETE | `/super_admin/mentor/course-category-detail/<category_id>/` | Course category detail |
| GET/POST | `/super_admin/mentor/courses/` | List / create courses |
| GET/PUT/DELETE | `/super_admin/mentor/course-detail/<course_id>/` | Course detail |
| GET | `/super_admin/mentor/category-courses/<category_id>/` | Courses within a category |
| GET/POST | `/super_admin/mentor/course-enquiries/` | List / create course inquiries |
| GET/PUT | `/super_admin/mentor/course-enquiry-detail/<enquiry_id>/` | Course inquiry detail |

### `/super_admin/admin/` — Platform Administration

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/super_admin/admin/dashboard/` | Aggregated dashboard metrics |
| GET/POST/PUT | `/super_admin/admin/site-configuration/` | Get / create / update global site configuration |
| GET/POST | `/super_admin/admin/why-choose-us/` | List / create "why choose us" items |
| GET/PUT/DELETE | `/super_admin/admin/why-choose-us/<id>/` | "Why choose us" item detail |

### `/super_admin/student/` — Students, Placements & Certificates

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET/POST | `/super_admin/student/testimonials/` | List / create testimonials |
| GET/PUT/DELETE | `/super_admin/student/testimonial-detail/<id>/` | Testimonial detail |
| GET/POST | `/super_admin/student/placements/` | List / create placements |
| GET/PUT/DELETE | `/super_admin/student/placement-detail/<id>/` | Placement detail |
| GET/POST | `/super_admin/student/certificate-templates/` | List / create certificate templates |
| GET/PUT/DELETE | `/super_admin/student/certificate-template-detail/<template_id>/` | Certificate template detail |
| GET/POST | `/super_admin/student/certificates/` | List / issue certificates |
| GET/PUT/DELETE | `/super_admin/student/certificate-detail/<id>/` | Certificate detail |
| GET | `/super_admin/student/certificate/verify/<certificate_id>/` | Public certificate verification |
| GET | `/super_admin/student/courses-list-dropdown/` | Active courses (dropdown) |
| GET | `/super_admin/student/mentors-list-dropdown/` | Active mentors (dropdown) |
| GET/POST | `/super_admin/student/course_enrollements/` | List / create course enrollments |
| GET/PUT/DELETE | `/super_admin/student/course-enrollement-detail/<enrolled_id>/` | Enrollment detail |

### Django Admin

| Endpoint | Description |
|-----------|--------------|
| `/admin/` | Django admin panel |

---

## Logging

Application logs are written to `logs/`:

| File | Level | Purpose |
|------|-------|----------|
| `django.log` | INFO+ | General application logs |
| `error.log` | ERROR+ | Unhandled request errors (`django.request`) |
| `security.log` | WARNING+ | Security-related warnings (`django.security`) |

---

## Media & Static Files

- **Media** (user uploads — profile pictures, course thumbnails, certificates, QR codes): `MEDIA_ROOT = media/`, served at `/media/` in `DEBUG` mode.
- **Static**: `STATIC_ROOT = staticfiles/`, served at `/static/` in `DEBUG` mode; use `whitenoise` / a reverse proxy in production.

Run `python manage.py collectstatic` before deploying to production.
