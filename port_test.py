import sys
print("Python Executable Path:", sys.executable)
import socket
from tqdm import tqdm
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

# Common ports dictionary
common_ports = {
    80: 'HTTP',
    443: 'HTTPS',
    22: 'SSH',
    21: 'FTP',
    53: 'DNS',
    25: 'SMTP'
}

# Banner grabbing function
def get_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((ip, port))
            banner = s.recv(1024).decode().strip()
            return banner if banner else "No banner"
    except:
        return "No banner or connection refused"

# Single port scan function
def scan_port(ip, port, common_ports):
    try:
        with socket.socket() as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                banner = get_banner(ip, port)
                service = common_ports.get(port, "Unknown")
                return (port, service, banner)
    except:
        pass
    return None

# Multithreaded port scan
def port_scan(ip, start_port, end_port, common_ports):
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {
            executor.submit(scan_port, ip, port, common_ports): port
            for port in range(start_port, end_port + 1)
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
            result = future.result()
            if result:
                open_ports.append(result)

    return open_ports

# Main execution
if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid hostname or IP.")
        exit()

    while True:
        choice = input("Do you want a custom range? (y/n): ").lower()

        if choice == 'y':
            try:
                start_port = int(input("Enter start port: "))
                end_port = int(input("Enter end port: "))
            except ValueError:
                print("Please enter valid numeric ports.")
                continue

            if 0 <= start_port <= 65535 and 0 <= end_port <= 65535:
                break
            else:
                print("Ports must be between 0 and 65535.")

        elif choice == 'n':
            while True:
                print("Scan:")
                print("1. Common ports (20-1024)")
                print("2. Full range (0-65535)")
                try:
                    ch = int(input("Enter your choice (1 or 2): "))
                    if ch == 1:
                        start_port = 20
                        end_port = 1024
                        break
                    elif ch == 2:
                        start_port = 0
                        end_port = 65535
                        break
                    else:
                        print("Invalid input! Please enter 1 or 2.")
                except ValueError:
                    print("Please enter a valid number.")
            break
        else:
            print("Invalid input! Please enter 'y' or 'n'.")

    print("-" * 40)
    print(f"Scanning target: {ip}")
    print(f"Port range: {start_port}-{end_port}")
    print("-" * 40)

    try:
        results = port_scan(ip, start_port, end_port, common_ports)

        if not results:
            print(f"{Fore.RED}Whoops! All ports are closed.{Style.RESET_ALL}")
        else:
            for port, service, banner in results:
                print(f"{Fore.GREEN}Port {port} is open ({service}) - Banner: {banner}{Style.RESET_ALL}")

        with open("scan_results.txt", "w") as f:
            f.write(f"Scanning {ip} from {start_port} to {end_port}\n")
            for port, service, banner in results:
                f.write(f"Port {port} is open ({service}) - Banner: {banner}\n")

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Scan interrupted by user. Exiting scan...{Style.RESET_ALL}")
