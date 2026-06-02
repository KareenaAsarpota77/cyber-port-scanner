import socket

PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt"
}

RISKY_PORTS = [21, 23, 3306]


def scan_ports(ip):
    results = []

    for port, service in PORT_SERVICES.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7)

        status = sock.connect_ex((ip, port))

        results.append({
            "port": port,
            "service": service,
            "status": "OPEN" if status == 0 else "CLOSED",
            "risk": port in RISKY_PORTS
        })

        sock.close()

    return results


def calculate_risk(results):
    open_ports = [r for r in results if r["status"] == "OPEN"]

    if not open_ports:
        return "LOW"
    if any(r["risk"] for r in open_ports) or len(open_ports) > 2:
        return "HIGH"
    return "MEDIUM"