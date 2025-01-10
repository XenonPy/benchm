import platform
import psutil
import os
import time
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Container

def get_hardware():
    """
    Collects and returns basic system information, including RAM and other details.
    Compatible with macOS and Linux.

    Returns:
        dict: A dictionary containing system information.
    """
    try:
        system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "arch": platform.architecture()[0],
            "hostname": platform.node(),
        }

        cpu_info = {
            "cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
        }

        memory_info = psutil.virtual_memory()
        ram_info = {
            "total_ram": round(memory_info.total / (1024 ** 3), 2),
            "available_ram": round(memory_info.available / (1024 ** 3), 2),
            "used_ram": round(memory_info.used / (1024 ** 3), 2),
            "usage_percent": memory_info.percent,
        }

        system_info.update(cpu_info)
        system_info.update(ram_info)

        return system_info

    except Exception as e:
        return {"Error": str(e)}

def measure_benchmarks():
    results = {}

    def cpu_benchmark():
        start_time = time.time()
        for _ in range(10**7):
            _ = 3.14159 ** 5
        end_time = time.time()
        return end_time - start_time

    results['CPU Performance (s)'] = cpu_benchmark()

    def memory_benchmark():
        size = 100 * 1024 * 1024  
        data = b"a" * size
        start_time = time.time()
        _ = data[::-1]  
        end_time = time.time()
        return end_time - start_time

    results['Memory Speed (s)'] = memory_benchmark()

    def disk_benchmark():
        temp_file = "temp_benchmark_file"
        size = 100 * 1024 * 1024  
        data = b"a" * size

        start_time = time.time()
        with open(temp_file, "wb") as f:
            f.write(data)
        write_time = time.time() - start_time

        start_time = time.time()
        with open(temp_file, "rb") as f:
            _ = f.read()
        read_time = time.time() - start_time

        os.remove(temp_file)

        return write_time, read_time

    write_time, read_time = disk_benchmark()
    results['Disk Write Speed (s)'] = write_time
    results['Disk Read Speed (s)'] = read_time

    return results

system_info = get_hardware()
benchmark_results = measure_benchmarks()

class SystemInfoApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Static(f"OS: {system_info['os']}"),
            Static(f"OS Version: {system_info['os_version']}"),
            Static(f"Release: {system_info['release']}"),
            Static(f"Machine: {system_info['machine']}"),
            Static(f"Processor: {system_info['processor']}"),
            Static(f"Architecture: {system_info['arch']}"),
            Static(f"Hostname: {system_info['hostname']}"),
            Static(f"Cores: {system_info['cores']}"),
            Static(f"Logical Cores: {system_info['logical_cores']}"),
            Static(f"CPU Frequency: {system_info['freq']} MHz"),
            Static(f"Total RAM: {system_info['total_ram']} GB"),
            Static(f"Available RAM: {system_info['available_ram']} GB"),
            Static(f"Used RAM: {system_info['used_ram']} GB"),
            Static(f"RAM Usage: {system_info['usage_percent']}%"),
            Static(f"CPU Performance: {benchmark_results['CPU Performance (s)']} s"),
            Static(f"Memory Speed: {benchmark_results['Memory Speed (s)']} s"),
            Static(f"Disk Write Speed: {benchmark_results['Disk Write Speed (s)']} s"),
            Static(f"Disk Read Speed: {benchmark_results['Disk Read Speed (s)']} s"),
        )

if __name__ == "__main__":
    SystemInfoApp().run()