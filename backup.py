import subprocess
import threading
import time

def run_rclone():
    while True:
        print("Menjalankan rclone copy...")
        subprocess.run(["rclone", "copy", "/root/billzfind/Shells.txt", "liebert:/backup_shell/", "--update", "-v"])
        print("Menunggu 30 menit sebelum menjalankan ulang...")
        time.sleep(1800)  # 30 menit

# Jalankan fungsi dalam thread terpisah
thread = threading.Thread(target=run_rclone, daemon=True)
thread.start()

# Tambahkan kode lain jika perlu
while True:
    try:
        time.sleep(1)  # Menjaga script tetap berjalan
    except KeyboardInterrupt:
        print("\nDihentikan oleh pengguna.")
        break
