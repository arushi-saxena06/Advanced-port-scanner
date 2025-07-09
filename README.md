# Advanced Port Scanner 🔍

A fast, advanced port scanner written in Python that scans ports within a specified range on a target IP or hostname, identifies services on common ports, and grabs banners where possible. The scanner uses **multithreading** for speed and provides a clean, colored terminal output along with progress tracking.

---

## 🚀 Features:
- **Multithreaded Port Scanning** — Fast and efficient scanning with ThreadPoolExecutor.
- **Banner Grabbing** — Attempts to fetch banners from open ports.
- **Common Ports Detection** — Identifies services on well-known ports (e.g., HTTP, HTTPS, SSH).
- **Progress Bar** — Displays real-time progress during scans using `tqdm`.
- **Colored Output** — Uses `colorama` for better terminal readability.
- **Custom & Preset Port Ranges** — Supports both manual range selection and quick presets.
- **Result Saving** — Automatically saves the scan results to `scan_results.txt`.
- **Graceful Interrupt Handling** — Detects `Ctrl+C` to safely exit.

---

## 📋 How It Works:
1. Takes a target hostname or IP address from the user.
2. Lets user choose either:
   - Custom port range  
   - Preset port ranges:
     - Common Ports (20–1024)
     - Full Range (0–65535)
3. Scans each port using multithreading:
   - Checks whether the port is open.
   - Identifies service if it’s a common port.
   - Attempts to grab the service banner.
4. Displays open ports in a colorful, formatted output.
5. Saves all scan results into `scan_results.txt`.

---

## 🛠️ Technologies Used:
- `socket` — For low-level network connections.
- `tqdm` — For progress bars.
- `colorama` — For colored terminal output.
- `concurrent.futures` — For multithreading.

---

## 📦 Requirements:
```bash
pip install tqdm colorama

📄 Usage:

python port_test.py

💡 Example:

Enter target IP or hostname: scanme.nmap.org
Do you want a custom range? (y/n): n
Scan:
1. Common ports (20-1024)
2. Full range (0-65535)
Enter your choice (1 or 2): 1

⚠️ Disclaimer:

This tool is for educational and authorized testing purposes only.
Unauthorized port scanning may be illegal or against terms of service.
📁 Output Example:

Port 80 is open (HTTP) - Banner: HTTP/1.1 200 OK
Port 22 is open (SSH) - Banner: No banner or connection refused

📜 License:

This project is licensed under the MIT License.
✨ Author:

Arushi Saxena