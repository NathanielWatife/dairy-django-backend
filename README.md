# Dairy Django Backend

![GitHub top language](https://img.shields.io/github/languages/top/AgriCodeHub/dairy-django-backend)
![GitHub last commit](https://img.shields.io/github/last-commit/AgriCodeHub/dairy-django-backend)
![GitHub repo size](https://img.shields.io/github/repo-size/AgriCodeHub/dairy-django-backend)
![GitHub Stars](https://img.shields.io/github/stars/AgriCodeHub/dairy-django-backend)
![Pytest](https://img.shields.io/badge/tests-pytest-green)

## Overview

Welcome to the Dairy Django Backend repository! This project aims to develop a robust backend system for managing a dairy farm. The system includes modules for user authentication, role-based access control, core dairy logic, health monitoring, production records, inventory management, sales, and feeds.

## Features

### 1. User Authentication

Implementing a secure user authentication system to manage access to the farm's backend. Users can create accounts, log in securely, and maintain the confidentiality of their data.

### 2. Role-Based Access Control

Introducing role-based access control to assign specific roles to users based on their responsibilities on the farm. This ensures different team members have appropriate access levels, enhancing security and streamlining operations.

### 3. Core Models for Dairy Logic

#### Core App (core):
- **Cow Model:** Captures essential information about each cow.
- **CowBreed Model:** Represents different breeds of cows.

#### Health App (health):
- **Disease Model:** Manages information related to diseases affecting cows.
- **Treatment Model:** Records details about treatments administered to cows.
- **Quarantine Model:** Tracks cows in quarantine.
- **Symptom Model:** Stores information about symptoms associated with diseases.
- **Pathogen Model:** Represents pathogens causing diseases.
- **DiseaseCategory Model:** Categorizes different diseases.
- **WeightRecord Model:** Records weight information of cows.
- **CullingRecord Model:** Manages records of culling instances.
- **Recovery Model:** Tracks recovery status of cows from specific diseases.

#### Production App (production):
- **Milk Model:** Records information related to milk production.
- **Lactation Model:** Manages lactation details of cows.

#### Reproduction App (reproduction):
- **Pregnancy Model:** Tracks pregnancy details of cows.
- **Heat Model:** Records information about the heat cycles of cows.
- **Insemination Model:** Manages details about cow insemination.

#### Inventory App (inventory):
- **CowInventory Model:** Manages information about cows in the inventory.
- **MilkInventory Model:** Tracks details related to milk inventory.

### 4. Sales Logic

Under development - planning to introduce models and logic for tracking milk sales, integrating with the Daraja API from Safaricom for payment processing.

### 5. Feeds

Under development - planning to introduce models and logic for managing feeds.



## Getting Started

To get started with the Dairy Django Backend, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/AgriCodeHub/dairy-django-backend.git

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Set up and configure the database:
    ```bash
    python manage.py migrate

4. Run the development server:
    ```bash
    python manage.py runserver

5. Access the application at http://localhost:8000 in your web  browser.


## Running tests
We use pytest for testing. To run tests, use the following command:

```bash
  pytest
```

## License
This project is licensed under the [Apache License 2.0](./LICENSE). Please review the [license file](./LICENSE) for more details.


## Contribution
We welcome contributions from the community! If you're interested in contributing to the Dairy Django Backend project, please follow our Contribution Guidelines.

## Contact
For any inquiries or feedback, feel free to contact us at agricodehub@gmail.com.

