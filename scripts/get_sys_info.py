import platform
import os

def get_system_info():
    """Gathers and returns a dictionary of system information."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "user": os.getlogin(),
    }
    return info

if __name__ == "__main__":
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key.capitalize()}: {value}")
