import os
import time
import ctypes
import psutil
import subprocess
import sys

def kill_process_by_name(name):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if name.lower() in proc.info['name'].lower():
                proc.kill()
                print(f"Killed {name} (PID: {proc.info['pid']})")
    except Exception as e:
        print(f"Error killing {name}: {e}")

def kill_process_windows_api(name):
    try:
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, get_pid_by_name(name))
        if handle:
            ctypes.windll.kernel32.TerminateProcess(handle, -1)
            ctypes.windll.kernel32.CloseHandle(handle)
            print(f"Terminated {name} via Windows API")
    except Exception as e:
        print(f"Error terminating {name} via API: {e}")

def get_pid_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None

def taskkill(name):
    try:
        subprocess.run(['taskkill', '/f', '/im', name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Killed {name} via taskkill")
    except subprocess.CalledProcessError as e:
        print(f"Error killing {name} via taskkill: {e}")

def main():
    processes = ['IMTWin.exe', 'IMTWin32.exe']

    while True:
        for proc in processes:
            try:
                # Method 1: psutil
                kill_process_by_name(proc)

                # Method 2: Windows API
                kill_process_windows_api(proc)

                # Method 3: taskkill
                taskkill(proc)
            except Exception as e:
                print(f"Error with {proc}: {e}")

        time.sleep(0.01)  # 10ms delay

if __name__ == "__main__":
    print("IMTWin Killer - Press Ctrl+C to stop")
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(0)
