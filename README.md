<div align="center">
<h1 align="center">
<br>argyle-upwork</h1>
<h3>◦ A Web Scanner for Upwork website.</h3>
<h4>Developed with following tools:</h4>
<p align="center">
<img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat-square&logo=Poetry&logoColor=white" alt="Poetry" />
<img src="https://img.shields.io/badge/Selenium-43B02A.svg?style=flat-square&logo=Selenium&logoColor=white" alt="Selenium" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker" />
<p>
<img src="https://camo.githubusercontent.com/d91ed7ac7abbd5a6102cbe988dd8e9ac21bde0a73d97be7603b891ad08ce3479/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667" alt="Code style: black" data-canonical-src="https://img.shields.io/badge/code%20style-black-000000.svg" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/59eab954a267c6e9ff1d80e8055de43a0ad771f5e1f3779aef99d111f20bee40/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667" alt="Type checked with mypy" data-canonical-src="http://www.mypy-lang.org/static/mypy_badge.svg" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/fe4a658dd745f746410f961ae45d44355db1cc0e4c09c7877d265c1380248943/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f253230696d706f7274732d69736f72742d2532333136373462313f7374796c653d666c6174266c6162656c436f6c6f723d656638333336" alt="Imports: isort" data-canonical-src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&amp;labelColor=ef8336" style="max-width: 100%;">
</div>

---

## 📍 Overview

The Argyle - Upwork project is a web scanning tool designed for extracting Job and Profile information from Upwork's website.

---

## 📦 Features

- **Login Management:** `login_manager` handles the login process on Upwork using inheritance from DriverManager, promoting code reuse and abstraction. This ensures a clean separation of concerns, with the login logic residing in a dedicated class.

- **Homepage Scanner:** The `homepage_scanner` module scans the Upwork homepage for job sections. It utilizes BeautifulSoup for HTML parsing and extracts relevant data from job sections.

- **Profile Scanner:** The `profile_scanner` module is responsible for scanning Upwork profile pages. It collects data from both the profile and contact info pages, including employment history.

- **Data Models:** The `argyle_upwork.models` package contains Pydantic models for representing job sections (`JobSection`) and profile information (`ProfilePage`, `AccountSection`, `LocationSection`, `Profile`). These models include validation and cleaning methods for data consistency.

- **Data storing locally:** Both `Jobs` and `Profile` data are stored locally in JSON format after its validation, in directory `data`. The names of the files saved are:
```
homepage-{date in format (%Y-%m-%d %H:%M:%S)}.json
profilepage-{date in format (%Y-%m-%d %H:%M:%S)}.json
```

---


## 📂 Repository Structure

```sh
└── argyle-upwork/
    ├── argyle_upwork/
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
python argyle_upwork/main.py
```

---


## 🎯 Next steps

1) Handle login with backup credentials if login process is not successful (Handle retry);
2) Scan other subpages in Home Page: Most Recent and Saved Jobs;
3) Get variable from a cloud environment (for production);
4) Store objects in a Database;
5) User-Agent rotation while scanning;
6) Using a pool of proxies to avoid IP ban;
7) Implement a mechanism to control the number of concurrent requests;
8) Use of asynchronous libs to improve scan time and concurrent scrape through different pages simultaneously.

---
