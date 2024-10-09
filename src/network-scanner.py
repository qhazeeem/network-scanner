import ipaddress
import platform
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
from prettytable import PrettyTable
import sys
import os

class NetworkScanner:
    def __init__(self):
        self.active_hosts = []
        self.common_ports = [80, 443, 22, 445, 3389]
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')
        
    def verify_host(self, ip):
        """Verify host is truly active using multiple methods"""
        # Try TCP connection first (faster than ICMP)
        for port in [445, 80, 443]:  # Common ports that are usually responsive
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((str(ip), port))
                sock.close()
                if result == 0:
                    return True
            except:
                continue
                
        # If TCP fails, try ICMP ping
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', str(ip)]
        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
            return output.returncode == 0
        except:
            return False
            
        return False

    def get_open_ports(self, ip):
        """Check for open ports with improved accuracy"""
        open_ports = []
        for port in self.common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((str(ip), port))
                sock.close()
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append(f"{port}({service})")
            except:
                continue
        return open_ports

    def get_service_name(self, port):
        """Get service names for common ports"""
        services = {
            80: "HTTP",
            443: "HTTPS",
            22: "SSH",
            445: "SMB",
            3389: "RDP"
        }
        return services.get(port, "Unknown")

    def get_hostname(self, ip):
        """Get hostname with timeout"""
        try:
            socket.setdefaulttimeout(1)
            hostname = socket.gethostbyaddr(str(ip))[0]
            return hostname
        except:
            return "Unknown"

    def scan_host(self, ip):
        """Scan a single host with improved accuracy"""
        try:
            # First verify the host is truly active
            if self.verify_host(str(ip)):
                # Get hostname
                hostname = self.get_hostname(str(ip))
                
                # Get open ports
                open_ports = self.get_open_ports(str(ip))
                
                # Measure response time
                start_time = time.time()
                self.verify_host(str(ip))  # Second verification for timing
                response_time = int((time.time() - start_time) * 1000)  # Convert to ms
                
                host_info = {
                    'ip': str(ip),
                    'hostname': hostname,
                    'response_time': f"{response_time}ms",
                    'open_ports': ', '.join(open_ports) if open_ports else 'None',
                    'last_seen': datetime.now().strftime('%H:%M:%S')
                }
                
                self.active_hosts.append(host_info)
                self.display_progress()
                
        except Exception as e:
            pass

    def display_progress(self):
        """Display scanning progress"""
        self.clear_screen()
        print(f"\nScanning network... Found {len(self.active_hosts)} active hosts")
        self.display_results(intermediate=True)

    def display_results(self, intermediate=False):
        """Display results in a table format"""
        table = PrettyTable()
        table.field_names = ["IP Address", "Hostname", "Response Time", "Open Ports", "Last Seen"]
        table.align = "l"  # Left align text
        table.max_width = 40  # Limit column width
        
        # Sort hosts by IP address
        sorted_hosts = sorted(self.active_hosts, 
                            key=lambda x: [int(i) for i in x['ip'].split('.')])
        
        for host in sorted_hosts:
            table.add_row([
                host['ip'],
                host['hostname'][:30] + '...' if len(host['hostname']) > 30 else host['hostname'],
                host['response_time'],
                host['open_ports'][:30] + '...' if len(host['open_ports']) > 30 else host['open_ports'],
                host['last_seen']
            ])
        
        if intermediate:
            # For progress updates, only show the last few rows
            print(table.get_string(end=10))  # Show last 10 results
        else:
            print(table)

    def scan_network(self, network_address, subnet_mask):
        try:
            # Create network object
            network = ipaddress.ip_network(f'{network_address}/{subnet_mask}', strict=False)
            hosts = list(network.hosts())
            total_hosts = len(hosts)
            
            print(f"\nInitiating scan of network {network}")
            print(f"Total hosts to scan: {total_hosts}")
            
            start_time = time.time()
            
            # Use ThreadPoolExecutor for parallel scanning
            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(self.scan_host, hosts)
            
            scan_duration = time.time() - start_time
            
            # Final results display
            self.clear_screen()
            print("\n" + "="*80)
            print(f"Scan Results Summary")
            print(f"Network: {network}")
            print(f"Scan Duration: {scan_duration:.2f} seconds")
            print(f"Active Hosts: {len(self.active_hosts)}/{total_hosts}")
            print("="*80 + "\n")
            
            if self.active_hosts:
                self.display_results()
            else:
                print("\nNo active hosts found on the network.")
            
        except Exception as e:
            print(f"An error occurred during scanning: {str(e)}")

def print_banner():
    banner = """
    ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
    ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
    ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
    ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                    
    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗   
    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗  
    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝  
    ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗  
    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║  
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  
    """
    print(banner)
    print("="*80)
    print("Advanced Network Scanner v1.0")
    print("Created by: @qhazeeem")
    print("="*80)
    time.sleep(2)  # Give users time to read the banner

def main():
    try:
        # Check for root/admin privileges
        if hasattr(os, 'geteuid') and os.geteuid() != 0:  # Unix-like systems
            print("This script requires root/administrator privileges to run properly.")
            print("Please run with sudo or as administrator.")
            sys.exit(1)
        elif platform.system().lower() == 'windows':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("This script requires administrator privileges to run properly.")
                print("Please run as administrator.")
                sys.exit(1)
    except Exception:
        pass  # Skip privilege check if it fails
    
    scanner = NetworkScanner()
    
    while True:
        try:
            scanner.clear_screen()
            print("\nNetwork Scanner")
            print("="*20)
            network_address = input("Enter network address (e.g., 192.168.1.0): ").strip()
            if not network_address:
                continue
            
            subnet_mask = input("Enter subnet mask (e.g., 24 for /24): ").strip()
            if not subnet_mask:
                continue
            
            # Validate network inputs
            ipaddress.ip_network(f'{network_address}/{subnet_mask}', strict=False)
            
            scanner.scan_network(network_address, subnet_mask)
            
            choice = input("\nWould you like to scan another network? (y/n): ")
            if choice.lower() != 'y':
                print("\n" + "="*60)
                print("Thank you for using our Network Scanner!")
                print("\nPotential Improvements for this project:")
                print("1. Add export functionality (CSV, PDF, JSON)")
                print("2. Implement continuous monitoring mode")
                print("3. Add device fingerprinting capabilities")
                print("4. Include vulnerability scanning features")
                print("5. Add network mapping visualization")
                print("6. Implement custom port range scanning")
                print("7. Add email notifications for discovered hosts")
                print("8. Include historical data comparison")
                print("\nContribute or follow updates:")
                print("GitHub: @qhazeeem")
                print("Twitter: @qhazeeem")
                print("\nYour feedback helps us improve!")
                print("="*60 + "\n")
                break
        
        except ValueError as e:
            print(f"Invalid input: {str(e)}")
        except KeyboardInterrupt:
            print("\nScan interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print_banner()
    main()
