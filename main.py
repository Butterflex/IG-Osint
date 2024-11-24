import os
import sys
import json
import instaloader
import getpass

class IGOsint:
    def __init__(self):
        self.L = instaloader.Instaloader()
        self.logged_in = False
        self.current_profile = None
        self.login_file = os.path.expanduser('~/.ig_login_cache.json')

    def simpan_kredensial(self, username, password):
        try:
            kredensial = {
                'username': username,
                'password': self.enkripsi_password(password)
            }
            with open(self.login_file, 'w') as file:
                json.dump(kredensial, file)
            print("[✓] Kredensial tersimpan dengan aman")
        except Exception as e:
            print(f"[✗] Gagal menyimpan kredensial: {e}")

    def enkripsi_password(self, password):
        return ''.join([chr(ord(c) + 1) for c in password])

    def dekripsi_password(self, enkripted_password):
        return ''.join([chr(ord(c) - 1) for c in enkripted_password])

    def cek_kredensial_tersimpan(self):
        try:
            if os.path.exists(self.login_file):
                with open(self.login_file, 'r') as file:
                    kredensial = json.load(file)
                username = kredensial['username']
                password = self.dekripsi_password(kredensial['password'])
                print(f"\n[!] Kredensial tersimpan ditemukan untuk user: {username}")
                pilihan = input("Gunakan kredensial tersimpan? (y/n): ").lower()
                if pilihan == 'y':
                    return self.login_otomatis(username, password)
            return False
        except Exception as e:
            print(f"[✗] Gagal membaca kredensial: {e}")
            return False

    def login_otomatis(self, username, password):
        try:
            self.L.login(username, password)
            print(f"[✓] Login Otomatis Berhasil untuk {username}")
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[✗] Login Otomatis Gagal: {e}")
            return False

    def login(self):
        try:
            if self.cek_kredensial_tersimpan():
                return True

            username = input("Masukkan username Instagram: ")
            password = getpass.getpass("Masukkan password Instagram (tidak tampil): ")
            self.L.login(username, password)
            print("[✓] Login Berhasil!")
            simpan = input("Simpan kredensial untuk login otomatis? (y/n): ").lower()
            if simpan == 'y':
                self.simpan_kredensial(username, password)
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[✗] Login Gagal: {e}")
            return False

    def hapus_kredensial(self):
        try:
            if os.path.exists(self.login_file):
                os.remove(self.login_file)
                print("[✓] Kredensial berhasil dihapus")
            else:
                print("[!] Tidak ada kredensial tersimpan")
        except Exception as e:
            print(f"[✗] Gagal menghapus kredensial: {e}")

    def main_menu(self):
        while True:
            self.clear_screen()
            self.banner()
            print("\nMENU UTAMA:")
            print("1. Login Instagram")
            if self.logged_in:
                print("2. Stories & Highlights")
                print("3. Informasi Profil")
                print("4. Hapus Kredensial Tersimpan")
                print("5. Keluar")
            else:
                print("2. Keluar")
            
            pilihan = input("\nPilih opsi: ")
            if pilihan == '1':
                self.login()
            elif self.logged_in:
                if pilihan == '2':
                    self.story_highlights_menu()
                elif pilihan == '3':
                    # Implementasi info profil
                    pass
                elif pilihan == '4':
                    self.hapus_kredensial()
                elif pilihan == '5':
                    print("Terima kasih!")
                    sys.exit()
            else:
                if pilihan == '2':
                    print("Terima kasih!")
                    sys.exit()
            input("\nTekan Enter untuk melanjutkan...")

    def story_highlights_menu(self):
        while True:
            self.clear_screen()
            self.banner()
            print("\n🔐 MENU STORIES & HIGHLIGHTS 🔐")
            print("\n⚠️ PERHATIAN:")
            print("- Fitur ini MEMBUTUHKAN LOGIN Instagram")
            print("- Pastikan Anda sudah login")
            print("- Hanya bisa download story/highlight akun yang dapat diakses")
            
            print("\nPILIH OPSI:")
            print("1. Download Stories")
            print("2. Download Highlights")
            print("3. Kembali ke Menu Utama")
            
            pilihan = input("\nMasukkan pilihan (1-3): ")
            
            if not self.logged_in:
                print("\n🚫 PERINGATAN: Anda BELUM LOGIN!")
                print("Silakan login terlebih dahulu di Menu Utama")
                input("Tekan Enter untuk melanjutkan...")
                break

            if pilihan == '1':
                username = input("Masukkan username target: ")
                self.download_stories(username)
            
            elif pilihan == '2':
                username = input("Masukkan username target: ")
                self.download_highlights(username)
            
            elif pilihan == '3':
                break
            
            input("\nTekan Enter untuk melanjutkan...")

    def download_stories(self, username):
        if not self.logged_in:
            print("\n🚫 LOGIN DIPERLUKAN!")
            print("Silakan login terlebih dahulu di Menu Utama")
            return

        try:
            # Buat direktori download
            download_path = os.path.expanduser('~/storage/shared/Instagram_Stories')
            os.makedirs(download_path, exist_ok=True)

            # Ambil profil target
            profile = instaloader.Profile.from_username(self.L.context, username)

            # Download Stories
            print(f"\n[+] Mendownload Stories dari {username}")
            stories = self.L.get_stories(userids=[profile.userid])
            
            story_count = 0
            for story in stories:
                for item in story.get_items():
                    # Download story
                    self.L.download_storyitem(item, target=download_path)
                    story_count += 1
            
            print(f"[✓] Berhasil mendownload {story_count} story")
            print(f"Tersimpan di: {download_path}")

        except Exception as e:
            print(f"[✗] Gagal download stories: {e}")

    def download_highlights(self, username):
        if not self.logged_in:
            print("\n🚫 LOGIN DIPERLUKAN!")
            print("Silakan login terlebih dahulu di Menu Utama")
            return

        try:
            # Buat direktori download
            download_path = os.path.expanduser('~/storage/shared/Instagram_Highlights')
            os.makedirs(download_path, exist_ok=True)

            # Ambil profil target
            profile = instaloader.Profile.from_username(self.L.context, username)

            # Download Highlights
            print(f"\n[+] Mendownload Highlights dari {username}")
            highlights = self.L.get_highlights(profile)
            
            highlight_count = 0
            for highlight in highlights:
                # Buat folder untuk setiap highlight
                highlight_folder = os.path.join(download_path, highlight.title)
                os.makedirs(highlight_folder, exist_ok=True)

                # Download item highlight
                for item in highlight.get_items():
                    self.L.download_storyitem(item, target=highlight_folder)
                    highlight_count += 1
            
            print(f"[✓] Berhasil mendownload {highlight_count} highlight")
            print(f"Tersimpan di: {download_path}")

        except Exception as e:
            print(f"[✗] Gagal download highlights: {e}")

    def banner(self):
        print("""
██╗ ██████╗      ██████╗ ███████╗██╗███╗   ██╗████████╗
██║██╔════╝     ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██║██║  ███╗    ██║   ██║███████╗██║██╔██╗ ██║   ██║   
██║██║   ██║    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
██║╚██████╔╝    ╚██████╔╝███████║██║██║ ╚████║   ██║   
╚═╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    
    IG-Osint
    By Butterflex
    """)

    def clear_screen(self):
        os.system('clear')

def main():
    osint = IGOsint()
    osint.main_menu()

if __name__ == "__main__":
    main()
