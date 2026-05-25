# Tiguan Trakker Master Documentation

## Project Overview
- **Purpose:** Automate fuel tracking and maintenance scheduling for the VW Tiguan.
- **Environment:** Nucbox K10 Lab running VS Code Remote Tunnels.

## Master Log: April – May 2026
| Date | Odometer (mi) | Trip (mi) | Fuel (gal) | Price/Gal | MPG | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 04-03 | 109,474 | 410.9 | 4.287 | $3.499 | 95.85 | Partial Fill (Excl.) |
| 04-03 | 109,497 | 433.6 | 10.569 | $3.739 | 41.03 | Partial Fill (Excl.) |
| 04-07 | 110,188 | 358.4 | 12.155 | $3.499 | 29.49 | Verified |
| 04-11 | 110,616 | 427.8 | 13.793 | $3.469 | 31.02 | Verified |
| 04-13 | 111,460 | 358.3 | 12.396 | $3.359 | 28.90 | Verified Baseline |
| 04-18 | 111,562 | 209.6 | 11.967 | $3.499 | 17.51 | |
| 04-21 | 112,197 | 377.5 | 13.306 | $3.359 | 28.37 | Verified |
| 05-23 | 117,665 | 177.3 | 12.387 | $3.639 | 24.78 | Full Refill |

## Maintenance History
- **2025-12-05:** New Continental Tires & Alignment.
- **2026-04-22:** Oil Change & Tire Rotation (Odometer: 112,213).
- **Next Service Due:** 122,101 miles.

## Technical Architecture
- **API Backend:** `server.js` (Express/Node) listens on port 3000.
- **Auth:** `auth.py` handles Google Sheets API via `service_key.json` (stored locally, ignored by Git).
- **Data Logic:** `clean_logs.py` filters MPG > 33 as "Partial Fill".
- **Auth:** Service Account via .env

## Known Troubleshooting
- **VS Code Tunnel:** If offline, use `Enter-PSSession` on the K10 to clear stale processes.
- **Git:** Credentials (`service_key.json`) are blocked by `.gitignore`.
- **GitHub Auth:** Clear cache via Accounts icon > Sign Out > Reload Window.
- **Data Anomaly:** If MPG > 33, flag as "Partial Fill".