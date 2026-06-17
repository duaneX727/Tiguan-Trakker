---
Project: Tiguan Trakker
Objective: Automate fuel/maintenance logging and homelab server management
Server: Nucbox K10
Last Updated: 2026-05-26
---

# Tiguan Trakker Knowledge Base

lab-server/                             <-- Main Root (Target of your VS Code Tunnel)
├── lab-backend-api/                    <-- Your Active Express Server Environment
│   ├── node_modules/                   <-- Localized Node Dependencies (Ignored by Git)
│   ├── .gitignore                      <-- Prevents node_modules from pushing
│   ├── package.json                    <-- Set to entry point: "server.js"
│   └── server.js                       <-- The live API processing your POST/GET routes
│
└── K10-Lab/                            <-- Your Project Parent Folder
    └── Tiguan-Project/                 <-- Your Python Automation Workspace
        ├── .gitignore                  <-- Now ignoring 'service_key.json'
        ├── service_key.json            <-- Safe & untouched locally on the K10 hardware
        ├── clean_logs.csv              <-- Data files processed by Python
        └── clean_logs.py               <-- Script handling data logic

Last Updated: 2026-06-12
lab-server/
│
├── trakker-ingest-webhook/      <-- Node.js microservice (Port 3000)
│   ├── server.js                 <-- Listens for incoming payloads / appends to CSV
│   └── raw_logs.csv              <-- Real-time lander buffer file
│
├── trakker-analytics-api/       <-- Python Flask service (Port 5000)
│   ├── server.py                 <-- Serves cleaned telemetry layer out to api sub-domain
│   └── clean_logs_v3.py          <-- Implements the 33 MPG rules & filter algorithms
│
└── K10-Lab/
    └── Tiguan-Project/           <-- Git target tree / central source control repo