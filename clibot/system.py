import subprocess
import platform
import datetime
import os

package_dir = os.path.dirname(os.path.abspath(__file__))

def get_system_clibot():
    """Get system information."""
    system_name = platform.system()
    
    if system_name == "Windows":
        os_info = subprocess.check_output('systeminfo', shell=True).decode('utf-8').splitlines()
        os_name = next((line.split(':', 1)[1].strip() for line in os_info if line.startswith('OS Name:')), "Unknown OS")

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        kernel_info = subprocess.check_output('ver', shell=True).decode('utf-8').strip()
        cpu_info = subprocess.check_output('wmic cpu get caption', shell=True).decode('utf-8').strip().split('\n')[1].strip()
        gpu_info = subprocess.check_output('wmic path win32_videocontroller get caption', shell=True).decode('utf-8').strip().split('\n')[1].strip()
        mem_info = subprocess.check_output('wmic memorychip get capacity', shell=True).decode('utf-8').strip().split('\n')[1].strip()
        disk_info = subprocess.check_output('wmic logicaldisk get size,freespace,caption', shell=True).decode('utf-8').strip().split('\n')[1:]
        disk_info = ', '.join(disk_info)

    else:
        try:
            os_info = subprocess.check_output('cat /etc/os-release', shell=True).decode('utf-8').strip()
            os_name = next((line.split('=')[1].strip('"') for line in os_info.split('\n') if line.startswith('PRETTY_NAME=')), "Unknown OS")
        except subprocess.CalledProcessError:
            os_name = "Unknown OS"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        kernel_info = subprocess.check_output('uname -a', shell=True).decode('utf-8').strip()
        cpu_info_raw = subprocess.check_output('lscpu | grep "Model name"', shell=True).decode('utf-8').strip()
        cpu_info = cpu_info_raw.split(':', 1)[1].strip() if ':' in cpu_info_raw else cpu_info_raw
        gpu_info = subprocess.check_output(r"lspci | grep -i 'vga\|3d\|2d'", shell=True).decode('utf-8').strip()
        mem_info_raw = subprocess.check_output('free -h | grep "Mem"', shell=True).decode('utf-8').strip().split()
        mem_info = f"Total: {mem_info_raw[1]}, Used: {mem_info_raw[2]}, Free: {mem_info_raw[3]}, Shared: {mem_info_raw[4]}, Buffers: {mem_info_raw[5]}, Available: {mem_info_raw[6]}"
        disk_info_raw = subprocess.check_output('df -h --total | grep "total"', shell=True).decode('utf-8').strip().split()
        disk_info = f"Total: {disk_info_raw[1]}, Used: {disk_info_raw[2]}, Available: {disk_info_raw[3]}, Use%: {disk_info_raw[4]}, Mounted on: {disk_info_raw[5]}"

    system_prompt = prompt.format(
        os_name=os_name,
        now=now,
        kernel_info=kernel_info,
        cpu_info=cpu_info,
        gpu_info=gpu_info,
        mem_info=mem_info,
        disk_info=disk_info,
    )
    
    return {"role": "system", "content": system_prompt}

prompt = """# Identity and Purpose

- You are Clibot - a versatile CLI AI assistant operating on `{os_name}`. Your primary function is to assist users with their queries and provide relevant information and guidance.
- Ensure your responses are accurate, concise, and relevant, avoiding unnecessary details.

## System Info

- **Date and Time:** `{now}`
- **Kernel:** `{kernel_info}`
- **CPU:** `{cpu_info}`
- **GPU:** `{gpu_info}`
- **Memory:** `{mem_info}`
- **Disk:** `{disk_info}`"""