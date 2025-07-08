import socket
from tqdm import tqdm
from colorama import Fore, Style

# Common ports dictionary
common_ports = {
    80: 'HTTP',
    443: 'HTTPS',
    22: 'SSH',
    21: 'FTP',
    53: 'DNS',
    25: 'SMTP'
}

# Get target IP or hostname
ip_or_host = input("Enter target IP or hostname: ")

try:
    ip = socket.gethostbyname(ip_or_host)
except socket.gaierror:
    print("Invalid hostname or IP.")
    exit()

open_ports = []

# User chooses port range
while True:
    choice = input("Do you want a custom range? (y/n): ").lower()

    if choice == 'y':
        try:
            st_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
        except ValueError:
            print("Please enter valid numeric ports.")
            continue  # go back and ask again

        # Range check
        if 0 <= st_port <= 65535 and 0 <= end_port <= 65535:
            break  # Valid input, break outer loop
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
                    st_port = 20
                    end_port = 1024
                    break  # valid inner choice, break inner loop
                elif ch == 2:
                    st_port = 0
                    end_port = 65535
                    break  # valid inner choice, break inner loop
                else:
                    print("Invalid input! Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
        break  # break outer loop after inner loop completes
    else:
        print("Invalid input! Please enter 'y' or 'n'.")

# Display scan info
print("-" * 40)
print(f"Scanning target: {ip}")
print(f"Port range: {st_port}-{end_port}")
print("-" * 40)

# Begin scanning
try:
    for port in tqdm(range(st_port, end_port + 1), desc="Scanning"):
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()

        if result == 0:
            open_ports.append(port)
            if port in common_ports:
                print(f"{Fore.GREEN}Port {port} is open ({common_ports[port]}){Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Port {port} is open{Style.RESET_ALL}")

    # If no ports were open
    if not open_ports:
        print(f"{Fore.RED}Whoops! All ports are closed.{Style.RESET_ALL}")

    print("\nScan complete...")

except KeyboardInterrupt:
    # handle keyboard interruptions
    print(f"\n{Fore.YELLOW}Scan interrupted by user. Exiting scan...{Fore.RESET}")

# Save to file
with open("scan_results.txt", "w") as f:
    f.write(f"Scanning {ip} from {st_port} to {end_port}\n")
    for port in open_ports:
        if port in common_ports:
            f.write(f"Port {port} is open ({common_ports[port]})\n")
        else:
            f.write(f"Port {port} is open\n")
