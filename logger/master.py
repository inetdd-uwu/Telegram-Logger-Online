from playwright.sync_api import sync_playwright
import time
import datetime
import os

print("logger start...")

USER = input("file: ")
USERNAME = input("username: ").replace("@", "")

LOG_FILE = f"log/user/{USER}.txt"
STATUS = ".topbar .info .i18n"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def get_sessions():
    if not os.path.exists("session"):
        return []
    return [d for d in os.listdir("session") if os.path.isdir(os.path.join("session", d))]

def logg_online():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] ONLINE\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
        print(f"write: {entry.strip()}")

def main():
    sessions = get_sessions()

    if sessions:
        print(f"Available sessions: {', '.join(sessions)}")
    else:
        print("No saved sessions.")

    sess_name = input("session name (or new name): ").strip()
    if not sess_name:
        sess_name = "default"

    SESS_DIR = f"session/{sess_name}"
    is_new = not os.path.exists(SESS_DIR)

    with sync_playwright() as p:
        if is_new:
            print(f"Creating new session '{sess_name}'. Opening browser...")
        else:
            print(f"Using session '{sess_name}'...")

        browser = p.firefox.launch_persistent_context(
            user_data_dir=SESS_DIR,
            headless=False,
            proxy={"server": "socks5://127.0.0.1:10808"},
            firefox_user_prefs={"network.proxy.socks_remote_dns": True}
        )

        page = browser.new_page()
        page.goto(f"https://web.telegram.org/k/#@{USERNAME}")

        if is_new:
            print("Log in to Telegram in the browser window.")
            input(">>> Press Enter when done...")
        else:
            time.sleep(5)

        print("Monitoring started.")

        try:
            while True:
                try:
                    element = page.locator(STATUS)
                    if element.count() > 0:
                        status_text = element.first.inner_text().strip().lower()
                        if "online" in status_text or "в сети" in status_text:
                            logg_online()
                except Exception as e:
                    print(f"error: {e}")

                time.sleep(50)

        except KeyboardInterrupt:
            print("\nlogger stoping")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
