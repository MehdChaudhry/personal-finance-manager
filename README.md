# Team-1 Financial App
The app allows users to register, log in, and manage their personal accounts, with a focus on tracking financial transactions like deposits and expenses. Users can view their total balance, manage their profile, and filter or review their recent transactions over various periods. It also enables users to add or subtract funds, label transactions, and view their financial history in detail.

This application was developed collaboratively as part of a seven-member academic team. I contributed to development and served as the **Requirements Manager**, helping define the project's scope, functionality, and functional requirements.

## Table of Contents
- [Members](#members)
- [Background](#background)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [My Role and Contributions](#my-role-and-contributions)
- [Requirements](#requirements)
- [Running with Docker](#running-with-docker)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Members
- Rafal Jasielec - Project Manager
- Mehd Chaudhry - Requirements Manager / Development
- Aahd Abubakar - Design Manager
- Kris Sakmuawong - Testing Manager
- Hubab Ali - Documentation Manager
- Jorge Chavez - Documentation Manager
- Tanbina Nabi - Documentation Manager

## Background
The primary objective is to provide users with a platform where they can not only track their current financial standing but also have access to detailed information about their past transactions. By enabling users to filter and review transactions over specific periods, the app helps individuals gain insight into their spending habits and financial patterns, thus promoting better financial management. Users can add or subtract funds with ease through dedicated buttons, ensuring that their financial data is always accurate and up-to-date.

This project is an excellent tool for anyone looking to organize their finances more effectively, and it serves as a practical solution for individuals seeking better control and visibility over their financial activities.

## Features
- User registration, login, and logout
- User profile management
- Multiple financial accounts
- Checking, savings, and other account types
- Deposit and expense tracking
- Transaction history
- Transaction filtering
- Transaction categorization
- Account deletion
- Monthly budget creation and management
- Budget item categorization
- Budget comparison
- Spending visualization by expense category
- Budget spending visualization

## Technologies Used

### Backend
- Python
- Django

### Database
- PostgreSQL

### Frontend
- HTML
- CSS

### Development Tools
- Docker
- Docker Compose
- Git
- GitHub

## My Role and Contributions
I served as the **Requirements Manager** while also contributing to development throughout the project.

My responsibilities included:

- Helping define the overall scope of the application
- Identifying and documenting functional requirements
- Helping determine which features and functionality would be included
- Defining expected behavior and acceptance criteria for application features
- Collaborating with team members throughout development
- Contributing to application development and troubleshooting
- Helping ensure implemented functionality aligned with the project's requirements

The requirements below document the functionality that was planned for the application throughout development.

## Functional Requirements

### FR-001: User Registration
**Rationale:** Enables users to create a secure, personalized account, ensuring their transactions and financial data are stored and accessed safely.

### FR-002: User Login
**Rationale:** Allows registered users to securely access their accounts and personal financial data.

### FR-003: User Logout
**Rationale:** Ensures users can safely exit the application, protecting their account and data.

### FR-004: User Profile Management
**Rationale:** Enables users to update personal information and credentials for a secure, customized experience.

### FR-005: Filter Transactions
**Rationale:** Allows users to quickly view transactions over specific time frames for easier tracking and analysis.

### FR-006: Total Amount
**Rationale:** Shows users their overall financial status by displaying the total balance from their transactions.

### FR-007: Deposit and Expense Button
**Rationale:** Provides an easy way for users to add or subtract funds while keeping their financial information up to date.

### FR-008: Data Visualization of Expense Categories
**Rationale:** Provides a chart showing expense categories and how much the user has spent in each category.

### FR-009: See All Button
**Rationale:** Allows users to display all transactions they have made.

### FR-010: Accounts for User
**Rationale:** Allows users to create different financial accounts, such as checking, savings, or other account types.

### FR-011: See All Transactions
**Rationale:** Allows users to view transactions across their accounts.

### FR-012: View Different Totals by Category
**Rationale:** Allows users to view their total balance and transactions organized by category.

### FR-013: View All Transactions for Current Account
**Rationale:** Allows users to view all transactions associated with a specific account rather than transactions from every account they own.

### FR-014: Delete an Account
**Rationale:** Allows users to delete an existing financial account.

### FR-015: Create a Monthly Budget
**Rationale:** Allows users to create a budget that is valid between a specified range of dates.

### FR-016: Add Items to a Budget
**Rationale:** Allows users to add items to a budget by specifying the item, its value, and its category, such as bills or leisure.

### FR-017: Store and Compare Budgets
**Rationale:** Allows users to store budgets and compare current and previous budgets to determine whether spending increased or decreased.

### FR-018: Budget Bar Graph
**Rationale:** Provides a bar graph that visually represents how much the user has spent relative to their budget.

### FR-019: Budget Management
**Rationale:** Allows users to create, edit, delete, and view budgets.

## Running with Docker
The application can be run locally using Docker Compose. The Docker environment consists of the Django web application and PostgreSQL database running in separate containers.

### Prerequisites
Before running the application, install:
- Docker Desktop
- Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/MehdChaudhry/personal-finance-manager.git
```

Navigate to the project directory:

```bash
cd personal-finance-manager/finance_project
```

### 2. Create the Environment File
Create a file named `.env` inside the `finance_project` directory.

Add:

```env
POSTGRES_DB=financeDB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_local_password
```

Replace `your_local_password` with a password for your local development environment.

The `.env` file is excluded from version control and should not be committed to GitHub.

### 3. Build and Start the Containers
```bash
docker compose up --build -d
```

Docker Compose starts two services:

- `web` - Django application
- `db` - PostgreSQL 16 database

### 4. Apply Database Migrations
```bash
docker compose exec web python manage.py migrate
```

### 5. Open the Application
After the containers are running, open the following address in your browser:

```text
http://localhost:8000
```

## Usage
After starting the application, users can create a new account or log into an existing account.

Once authenticated, users can manage their financial information by creating accounts, recording deposits and expenses, reviewing transactions, creating budgets, and viewing financial visualizations.

Transactions are entered manually and can be organized into categories to help users better understand their financial activity.

### Useful Docker Commands
Check the running containers:

```bash
docker compose ps
```

View container logs:

```bash
docker compose logs
```

Follow container logs in real time:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

Stop the application and remove the PostgreSQL development volume:

```bash
docker compose down -v
```

> **Note:** Removing the PostgreSQL volume deletes the database data stored locally in that Docker volume.

## Project Structure
```text
personal-finance-manager/
│
├── finance_project/
│   ├── finance_app/
│   ├── finance_project/
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```
