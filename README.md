Tiguan Trakker 🚗📊
A Python-based automation tool designed to log, clean, and analyze vehicle fuel efficiency and maintenance data for a 2021 Volkswagen Tiguan.

🛠 Project Overview
This project was developed as part of a transition into Full-Stack Engineering and DevOps. It utilizes a central Nucbox K10 home lab server to automate data processing from raw fuel logs, ensuring data integrity through custom cleaning logic.

🚀 Key Features
Automated Data Cleaning: Processes raw CSV fuel logs using the Pandas library.

Partial Fill Logic: Implements a strict rule to identify partial fuel fills.

Note: Any reading above 33 MPG is treated as a partial fill and automatically excluded from standard fuel economy calculations to prevent data skewing.

Lab-to-Cloud Integration: Developed on a remote development environment using VS Code Tunnels and GitHub CLI for version control.

📁 Repository Structure
clean_logs.py: The core Python engine for data transformation.

Tiguan-Logs/: Directory containing raw and processed mileage data.

.gitignore: Configured to protect sensitive environment variables and Google Cloud API keys.

🧰 Tech Stack
Language: Python 3.x

Libraries: Pandas, NumPy

Infrastructure: Nucbox K10 Server (Remote Lab)

DevOps Tools: Git, GitHub CLI, VS Code Remote Tunnels