# Tiguan Trakker 🚗📊

> **Status:** Active Development | **Target:** DevOps/Full-Stack Portfolio

A robust, multi-service Python and Bash automation platform designed to ingest, process, store, and analyze vehicle diagnostics and fuel metrics for a Volkswagen Tiguan.

---

## 🛠️ Project Overview
This platform serves as a core portfolio piece demonstrating end-to-end data engineering, systems orchestration, and DevOps best practices. Moving beyond simple scripts, the project architecture spans a local automated ingest engine, an orchestration layer, relational database migrations, and real-time backend analytics services running natively in a dedicated home lab environment.

## 🚀 Key Features
* **Unified Service Orchestration:** Employs a centralized management framework (`start_all.py`) to handle lifecycle initialization, process monitoring, and seamless coordination between back-end data services.
* **Relational Data Storage & Migration:** Structural migration from flat logs to a robust, indexed SQLite binary database layer for optimal query optimization and tracking integrity.
* **Advanced Analytics Engine:** Dedicated execution layers (`view_analytics.py`, `view_stats.py`) parsing raw vehicle log inputs to compute key metrics, runtime efficiencies, and fuel analytics.
* **Automated File & Ingest Management:** Shell script pipelines (`organize_files.sh`) to automate data ingestion hygiene, stage internal assets, and clear log dependencies cleanly.
* **Secure Hybrid Cloud Infrastructure:** Architected with remote development bridges, secure Cloudflare tunnel routing via `mdmcode.io`, and granular web access control policies.

## 💻 Tech Stack
| Category | Tools |
| :--- | :--- |
| **Languages** | Python `3.14+`, Bash Shell scripting |
| **Data & Storage** | SQLite Database Engine, Pandas, NumPy |
| **Services & APIs** | Webhook Ingest Receivers, Analytics API Routing Modules |
| **Infrastructure** | NucBox K10 Server Architecture, Cloudflare Edge Tunnels |
| **DevOps & Edge** | Git, GitHub, VS Code Remote SSH Development Bridge |

## 📂 Repository Structure
* `start_all.py` — Central orchestrator coordinating system execution and back-end services.
* `server.py` & `trakker-analytics-api/` — Microservice API layer routing system inquiries and data requests.
* `trakker-ingest-webhook/` — Real-time event receiver for raw vehicle log inputs.
* `migrate_db.py` — Database schema management and SQLite compilation routines.
* `view_analytics.py` & `view_stats.py` — Data extraction scripts processing tracking trends and metrics.
* `organize_files.sh` — High-efficiency shell utility automating local staging area maintenance.
* `TIGUAN_TRAKKER_KNOWLEDGE_BASE.md` — Centralized project documentation and system architecture runbook.

## 📝 Next Milestones
- [ ] Implement automated GitHub Actions CI/CD workflows for script test validation.
- [ ] Connect frontend components to the `trakker-analytics-api` interface.
- [ ] Build visual graph tracking widgets utilizing Matplotlib / Seaborn datasets.