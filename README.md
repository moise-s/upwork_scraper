<div align="center">
<h1 align="center">
<br>Upwork Scraper</h1>
<h3>◦ A Web Scraper for Upwork website.</h3>
<h4>Developed with following tools:</h4>
<p align="center">
<img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat-square&logo=Poetry&logoColor=white" alt="Poetry" />
<img src="https://img.shields.io/badge/Selenium-43B02A.svg?style=flat-square&logo=Selenium&logoColor=white" alt="Selenium" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker" />
<p>
</div>

---

## 📍 Overview

The Upwork Scraper project is a web scanning tool designed for extracting Job and Profile information from Upwork's website.

---

## 📦 Features

### 1. Login Management (`login_manager`)

The `login_manager` module handles the login process on Upwork, utilizing inheritance from `DriverManager`. This promotes code reuse and abstraction, ensuring a clean separation of concerns. The login logic resides in a dedicated class for easy maintenance.

### 2. Homepage Scanner (`homepage_scanner`)

The `homepage_scanner` module scans the Upwork homepage for job sections. It employs BeautifulSoup for HTML parsing and extracts relevant data from job sections.

### 3. Profile Scanner (`profile_scanner`)

The `profile_scanner` module is responsible for scanning Upwork profile pages. It collects comprehensive data from both the profile and contact info pages, including employment history.

### 4. Data Models (`upwork_scraper.models`)

The `upwork_scraper.models` package contains Pydantic models for representing job sections (`JobSection`) and profile information (`ProfilePage`, `AccountSection`, `LocationSection`, `Profile`). These models include validation and cleaning methods for data consistency.

### 5. Data Storage Locally

Both job and profile data are stored locally in JSON format after validation. The data is saved in the `data` directory with filenames following the format:

- `homepage-{date in format (%Y-%m-%d %H:%M:%S)}.json`
- `profilepage-{date in format (%Y-%m-%d %H:%M:%S)}.json`

### 6. Tests

The `upwork_scraper.tests` package includes tests designed to assert the functionality of crucial driver and model components. These tests ensure the proper evaluation of key functions, covering areas such as driver behavior, model validation, and overall project integrity.

---


## 📂 Repository Structure

```sh
└── argyle-upwork/
    ├── upwork_scraper/
    │   ├── driver.py
    │   ├── homepage_scanner.py
    │   ├── logger.py
    │   ├── login_manager.py
    │   ├── main.py
    │   ├── models/
    │   │   ├── job.py
    │   │   └── profile.py
    │   └── profile_scanner.py
    ├── dockerfile
    ├── poetry.lock
    ├── pyproject.toml
    └── requirements.txt

```

---

## 🏛️ Architecture

The project adopts an object-oriented architecture to enhance modularity, maintainability, and extensibility. It was designed to have an entry point in `main.py` to start the scan process.

OOP principles such as encapsulation and inheritance are applied. It follows a modular architecture with separate modules for login management, homepage scanning, and profile scanning. 

The use of Pydantic models ensures structured data representation, and the separation of concerns is maintained through different classes for managing the ChromeDriver (`ChromeDriver`, `DriverManager`) using inheritance.

---

## 🛠️ Design Choices

- **Use of Selenium and BeautifulSoup:** Selenium for browser automation, and BeautifulSoup for HTML parsing. This combination allows for effective interaction with dynamic web pages and data extraction.

---

## 📚 Good Practices

- **Code Structuring:** The codebase is organized into modules, classes, and functions, promoting clarity and maintainability and trying to reach good practices of software engineering. Modularization and clear separation of responsibilities contribute to code readability and ease of maintenance.

- **Documentation:** Inline comments and docstrings are used to explain the purpose and functionality of functions and classes.

- **Linting and Code Quality** It was applied the use of following linters: `black`, `isort`, `flake8`, `pydocstyle`, `refurb` and `mypy`.

-- **Environment Management** The use of `Poetry` dependency management emphasizes a modern and standardized approach. This ensures a consistent environment across development and deployment, mitigating potential compatibility issues.

-- **Semantic Commits** During project development, it was employed the use of semantic commits with emojis, so it is easier to debug when needed.

---

## 🚀 Getting Started

### 🔧 Installation

1. Clone the argyle-upwork repository:
```sh
git clone https://github.com/moise-s/argyle-upwork
```

2. Change to the project directory:
```sh
cd argyle-upwork
```

3. Install the dependencies using Poetry:
```sh
poetry install
```

4. Use virtual env created with Poetry:
```sh
poetry shell
```

### 🔧 Environment Setup

Create a `.env` file with the necessary environment variables (`ARGYLE_USERNAME`, `ARGYLE_PASSWORD`, `ARGYLE_SECRET_ANSWER`).


### 🤖 Running argyle-upwork

```sh
python upwork_scraper/main.py
```

## 🧪 Running Tests

To run the tests, execute the following command in the project directory:

```sh
pytest upwork_scraper/tests
```

---


## 🎯 Next steps

1) Handle login with backup credentials if login process is not successful (Handle retry);
2) Scan other subpages in Home Page: Most Recent and Saved Jobs;
4) Getting more information from Profile page (hours per week, languages, education etc...)
5) Get variable from a cloud environment (for production);
6) Store objects in a Database;
7) User-Agent rotation while scanning;
8) Using a pool of proxies to avoid IP ban;
9) Implement a mechanism to control the number of concurrent requests;
10) Use of asynchronous libs to improve scan time and concurrent scrape through different pages simultaneously.

---
