import socket
import psutil

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            print(f"Port {port} is FREE.")
        except socket.error:
            print(f"Port {port} is IN USE.")
            find_procs_by_port(port)

def find_procs_by_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    print(f"Process using port {port}: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    check_port(5000)
