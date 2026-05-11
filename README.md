# Tiguan Trakker 🚗📊

> **Status:** Active Development | **Target:** DevOps/Full-Stack Portfolio

A Python-based automation tool designed to log, clean, and analyze vehicle fuel efficiency for a **2021 Volkswagen Tiguan**.

---

## 🛠 Project Overview
This project was developed as part of a career transition into **Full-Stack Engineering and DevOps**. It utilizes a central **Nucbox K10** home lab server to automate data processing from raw fuel logs, ensuring data integrity through custom cleaning logic.

## 🚀 Key Features
* **Automated Data Cleaning:** Leverages the `Pandas` library to transform raw CSV data.
* **Partial Fill Logic:** * Any reading **above 33 MPG** is identified as a partial fill.
    * These entries are automatically excluded from standard fuel economy calculations to maintain accuracy.
* **Lab-to-Cloud Integration:** Developed using a remote development bridge (VS Code Tunnels) and GitHub CLI.

## 🧰 Tech Stack

| Category | Tools |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **Libraries** | Pandas, NumPy |
| **Infrastructure** | Nucbox K10 Server (Ubuntu/Win11) |
| **DevOps** | Git, GitHub CLI, VS Code Remote Tunnels |

## 📁 Repository Structure
* `clean_logs.py`: Core logic for data transformation.
* `Tiguan-Logs/`: Source directory for raw and processed mileage data.
* `.gitignore`: Prevents exposure of sensitive Google Cloud API keys.

---

## 📝 Future Housekeeping
- [ ] Implement automated GitHub Actions for data validation.
- [ ] Add visualization dashboard using Matplotlib.
- [ ] Integrate Google Sheets API for real-time mobile logging.