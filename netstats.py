import socket
import psutil
import requests
import subprocess
import speedtest
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unavailable"

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=3).text
    except:
        return "Unavailable (offline?)"

def get_network_usage():
    counters = psutil.net_io_counters()
    sent_mb = counters.bytes_sent / (1024 ** 2)
    recv_mb = counters.bytes_recv / (1024 ** 2)
    return f"{sent_mb:.2f} MB", f"{recv_mb:.2f} MB"

def check_connection():
    try:
        subprocess.check_output(["ping", "-c", "1", "8.8.8.8"], stderr=subprocess.DEVNULL)
        return "Online"
    except subprocess.CalledProcessError:
        return "Offline"

def get_speedtest_results():
    try:
        console.print("\n[bold yellow]Running speed test... (this may take a few seconds)[/bold yellow]")
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps
        return f"{download:.2f} Mbps", f"{upload:.2f} Mbps"
    except:
        return "N/A", "N/A"

def show_dashboard():
    connection_status = check_connection()
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    sent, received = get_network_usage()
    download, upload = get_speedtest_results()

    table = Table(title="🌐 NetPeek — Offline Network Dashboard", box=box.SIMPLE_HEAVY)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Connection", connection_status)
    table.add_row("Local IP", local_ip)
    table.add_row("Public IP", public_ip)
    table.add_row("Data Sent", sent)
    table.add_row("Data Received", received)
    table.add_row("Download Speed", download)
    table.add_row("Upload Speed", upload)

    console.clear()
    console.print(Panel.fit(table, padding=(1, 2), border_style="blue"))

if __name__ == "__main__":
    show_dashboard()
