from flask import Flask, render_template, request, send_file
import socket
import os
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)

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

REPORT_DIR = "reports"
STATIC_DIR = "static"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def scan_ports(ip):
    results = []

    for port, service in PORT_SERVICES.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        status = sock.connect_ex((ip, port))

        results.append({
            "port": port,
            "service": service,
            "status": "OPEN" if status == 0 else "CLOSED"
        })

        sock.close()

    return results

def generate_graph(results):
    open_ports = len([r for r in results if r["status"] == "OPEN"])
    closed_ports = len(results) - open_ports

    plt.figure(figsize=(4, 3))
    plt.bar(["OPEN", "CLOSED"], [open_ports, closed_ports], color=["green", "red"])
    plt.title("Port Scan Result")

    path = os.path.join(STATIC_DIR, "graph.png")
    plt.savefig(path)
    plt.close()

    return path

def generate_report(ip, results):
    filename = f"report_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(REPORT_DIR, filename)

    open_ports = [r for r in results if r["status"] == "OPEN"]
    closed_ports = [r for r in results if r["status"] == "CLOSED"]

    with open(path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("           CYBER PORT SCANNER REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Target IP / Host : {ip}\n")
        f.write(f"Scan Time        : {datetime.now()}\n")
        f.write(f"Total Ports      : {len(results)}\n")
        f.write(f"Open Ports       : {len(open_ports)}\n")
        f.write(f"Closed Ports     : {len(closed_ports)}\n")

        f.write("\n" + "-" * 60 + "\n")
        f.write("OPEN PORTS\n")
        f.write("-" * 60 + "\n")

        if open_ports:
            for r in open_ports:
                f.write(f"[OPEN]   Port {str(r['port']).ljust(5)} | {r['service']}\n")
        else:
            f.write("No open ports found.\n")

        f.write("\n" + "-" * 60 + "\n")
        f.write("CLOSED PORTS\n")
        f.write("-" * 60 + "\n")

        for r in closed_ports:
            f.write(f"[CLOSED] Port {str(r['port']).ljust(5)} | {r['service']}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 60 + "\n")

    return path

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    ip = None
    graph = None
    report = None
    error = None

    if request.method == "POST":
        target = request.form["target"]

        try:
            ip = socket.gethostbyname(target)
        except:
            error = "Invalid IP or Hostname"
            return render_template("index.html", error=error)

        results = scan_ports(ip)
        graph = generate_graph(results)
        report = generate_report(ip, results)

    return render_template(
        "index.html",
        results=results,
        ip=ip,
        graph=graph,
        report=report
    )

@app.route("/download")
def download():
    files = sorted([f for f in os.listdir(REPORT_DIR) if f.endswith(".txt")])

    if not files:
        return "No reports found"

    latest = os.path.join(REPORT_DIR, files[-1])
    return send_file(latest, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)