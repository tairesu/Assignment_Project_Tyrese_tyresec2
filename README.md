# Digital Card Management System

A Django web application for managing digital business cards. Users can activate cards, update card details, analyze card usage, and export reports.

## Project Overview

This system enables customers to manage their digital cards from home. It provides authentication, card editing, QR code generation, analytics with PlotlyJS, and CSV/JSON export capabilities.

## Foundational 

- Github
- UI/UX Planning
- Models + ORM Basics
- Views + Templates + URLS
- User Authentication 
- Deployment 

## Functional Add-ons (Table 2)

- ORM Queries Data Summaries
- Static Files (Tailwind,  Vanilla JS & Jquery)
- Charts / Visuals (PlotlyJS)
- Forms + Basic Input (CRUD)
- Simple JSON Endpoints / ApIs
- Integrate QrCode API
- Data Presentation & Export
- User Auth for External Users

## Bonus Features

- Custom form validation
- Media Files 

### Authentication & User Management

* Signup, login, logout
* Profile creation and updates
* Dashboard with protected content
* Role‑restricted views

## ER Diagram

![ER Diagram](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/notes/erDiagram.png)

## Tech Stack

| Area         | Technology     |
| ------------ | -------------- |
| Backend      | Django         |
| Frontend     | TailwindCSS    |
| Charts       | PlotlyJS       |
| Database     | SQLite         |
| External API | goQR.me QR API |

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/tairesu/Assignment_Project_Tyrese_tyresec2.git
cd Assignment_Project_Tyrese_tyresec2
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
```

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

## Usage Guide

* Access dashboard after login
* Edit card details via update form
* View usage analytics on reports page
* Download CSV/JSON exports
* Scan or activate cards using public endpoints


## Development Notes (Condensed)

### A5

* TailwindCSS added to base template
* Form customization
* LoginView context improvements
* Dashboard FBV migrated to CBV
* Conditional login anchors

### A6

* Removed unused or out‑of‑scope systems
* Added two aggregations and one filtering feature

### A7

* Added PlotlyJS visualizations
* Backend JSON feeding into frontend JS
* Created a JS Plot wrapper class

### A8

* Implemented both FBV and CBV card update flows
* Added CardForm with validation and field restrictions

### A9

* Added daily usage JSON endpoint
* Added matplotlib chart PNG endpoint

### A10

* Integrated external QR API
* Added JS blob download flow for SVG QR codes

### A11 (Exports)

* CSV and JSON usage export functionality
* Added /reports/, /export/usage.csv, /export/usage.json

### A11 (Authentication)

* Implemented signup process
* Protected routes: dashboard, profile create, card update, reports, exports
* Public routes: signup, card activation, card scan, profile detail

## Credentials for Grading

* Username: mohitg2
* Password: graingerlibrary

* Username: infoadmins
* Password: uiucinfo