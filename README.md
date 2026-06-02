# Cyber Port Scanner 

## Overview
A Flask-based cybersecurity tool for performing TCP port scans and visualizing results through a web interface with automated report generation.

## Features
- TCP port scanning using Python sockets
- Web-based dashboard using Flask
- Open and closed port detection
- Scan result visualization using Matplotlib
- Automated timestamped report generation
- Support for IP address and domain scanning

## Requirements
- Python 3.8+
- Flask
- Matplotlib

Install dependencies:
pip install flask matplotlib

## Project Structure
```
cyber-port-scanner/
├── app.py
├── scanner.py
├── templates/
│   └── index.html
├── static/   (stores generated visualization files)
├── reports/  (stores generated scan reports)
└── README.md
```

Note: Ensure `static/` and `reports/` directories exist before execution.

## Usage

Run the application:
python app.py

Access the web interface:
http://localhost:5000/

## Screenshots
<img width="496" height="260" alt="1" src="https://github.com/user-attachments/assets/e42a51fe-dd91-4aed-8475-03b37393b050" />
<img width="496" height="236" alt="2" src="https://github.com/user-attachments/assets/f11fcaee-8a06-4008-8d0f-74c14e0a15f3" />

## Supported Targets
- IPv4 addresses
- Domain names

Example:
- 127.0.0.1
- scanme.nmap.org (authorized security testing environment)

## Output
- List of scanned ports (OPEN / CLOSED)
- Visual representation of scan results
- Generated scan report stored locally

## Disclaimer
This project is intended for educational purposes and authorized security testing only.

The author is not responsible for misuse or damage caused by this tool. Users are responsible for ensuring proper authorization before scanning any target systems.

Unauthorized scanning may violate applicable laws and regulations.

## License
MIT License
