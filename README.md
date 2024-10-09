# Advanced Network Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A powerful and user-friendly network scanning tool that discovers active hosts on your network and provides detailed information about each host, including open ports, response times, and hostnames.

## Features

- Fast and accurate host discovery
- Detailed port scanning
- Hostname resolution
- Response time measurement
- Real-time progress updates
- Clean tabular output
- Multi-threading for improved performance
- Cross-platform compatibility (Windows, Linux, macOS)

## Requirements

- Python 3.6+
- Root/Administrator privileges
- Network access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/qhazeeem/network-scanner.git
cd network-scanner
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the scanner with administrator privileges:

```bash
# On Linux/Mac:
sudo python3 src/network_scanner.py

# On Windows (run as administrator):
python src/network_scanner.py
```

Follow the prompts to enter:
1. Network address (e.g., 192.168.1.0)
2. Subnet mask (e.g., 24 for /24)

## Sample Output

```
Network Scanner
====================
Scanning network... Found 5 active hosts

+----------------+----------------------+---------------+------------------+-----------+
| IP Address     | Hostname            | Response Time | Open Ports       | Last Seen |
+----------------+----------------------+---------------+------------------+-----------+
| 192.168.1.1    | router.local        | 2ms          | 80(HTTP),443(HTTPS) | 15:30:45 |
| 192.168.1.100  | desktop.local       | 5ms          | 445(SMB)        | 15:30:46 |
+----------------+----------------------+---------------+------------------+-----------+
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) before submitting a Pull Request.

## Future Improvements

- [ ] Export functionality (CSV, PDF, JSON)
- [ ] Continuous monitoring mode
- [ ] Device fingerprinting
- [ ] Vulnerability scanning
- [ ] Network mapping visualization
- [ ] Custom port range scanning
- [ ] Email notifications
- [ ] Historical data comparison

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Follow Us

- GitHub: [@qhazeeem](https://github.com/qhazeeem)
- Twitter: [@qhazeeem](https://twitter.com/qhazeeem)

## Acknowledgments

- Contributors and testers
- Open source community
