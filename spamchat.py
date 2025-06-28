import requests, time, os, random
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def banner():
    width = 56
    print(rgb(255, 0, 255) + "╔" + "═" * width + "╗")
    print(rgb(255, 200, 0) + "║" + " 💥 Oinanoi874 Spam Chat 💥 ".center(width) + "║")
    print(rgb(255, 0, 255) + "╠" + "═" * width + "╣")
    menu = [
        "1. Gửi lần lượt tin nhắn",
        "2. Gửi ngẫu nhiên tin nhắn",
        "3. Gửi so le ảnh + tin nhắn",
        "4. Gửi ảnh tuần tự",
        "5. Gửi ảnh ngẫu nhiên"
    ]
    for m in menu:
        print(rgb(0, 255, 255) + "║ " + rgb(0, 255, 100) + m.ljust(width - 2) + rgb(0, 255, 255) + "║")
    print(rgb(255, 0, 255) + "╚" + "═" * width + "╝\n")

banner()

cookie_input = input(rgb(255, 255, 0) + "👉 Nhập cookie (full): ").strip()
receiver_id = input(rgb(0, 255, 255) + "🎯 ID người nhận: ").strip()
mode = input(rgb(255, 100, 255) + "📌 Nhập số chức năng (1 → 5): ").strip()
delay = float(input(rgb(100, 255, 255) + "⏱️ Độ trễ giữa các lần gửi (giây): ").strip())

cookies = {}
for part in cookie_input.split(';'):
    if '=' in part:
        k, v = part.strip().split('=', 1)
        cookies[k.strip()] = v.strip()

c_user = cookies.get("c_user")
xs = cookies.get("xs")

if not c_user or not xs:
    print(Fore.RED + "❌ Cookie không hợp lệ!")
    exit()

session = requests.Session()
session.cookies.update(cookies)
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Referer": f"https://mbasic.facebook.com/messages/read/?tid=user:{receiver_id}"
}

print(Fore.BLUE + "\n🔍 Đang lấy fb_dtsg...")
res = session.get(f"https://mbasic.facebook.com/messages/read/?tid=user:{receiver_id}", headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
fb_dtsg_input = soup.find("input", {"name": "fb_dtsg"})

if not fb_dtsg_input:
    print(Fore.RED + "❌ Không lấy được fb_dtsg!")
    exit()

fb_dtsg = fb_dtsg_input["value"]
print(Fore.GREEN + "✅ Lấy fb_dtsg thành công!")

messages = []
if mode in ['1', '2', '3']:
    print(Fore.CYAN + "\n📥 Nhập tin nhắn (gõ 'xong' để kết thúc):")
    while True:
        msg = input("💬 → ").strip()
        if msg.lower() == 'xong':
            break
        if msg:
            messages.append(msg)

images = []
if mode in ['3', '4', '5']:
    print(Fore.CYAN + "\n🖼️ Nhập đường dẫn các ảnh (gõ 'xong' để kết thúc):")
    while True:
        path = input("🖼️ → ").strip()
        if path.lower() == 'xong':
            break
        if os.path.exists(path):
            images.append(path)
        else:
            print(Fore.RED + "❌ Không tìm thấy ảnh:", path)

def send_image(image_path):
    form = soup.find("form", {"method": "post", "enctype": "multipart/form-data"})
    if not form:
        print(Fore.RED + "❌ Không tìm thấy form gửi ảnh.")
        return False
    upload_url = "https://mbasic.facebook.com" + form.get("action")
    inputs = form.find_all("input")
    data = {i.get("name"): i.get("value") for i in inputs if i.get("name")}
    files = {"file1": open(image_path, "rb")}
    res = session.post(upload_url, data=data, files=files)
    return res.status_code == 200

def send_text(msg):
    form = soup.find("form", {"method": "post"})
    if not form:
        print(Fore.RED + "❌ Không tìm thấy form gửi tin nhắn.")
        return False
    action = form.get("action")
    send_url = "https://mbasic.facebook.com" + action
    inputs = form.find_all("input")
    data = {i.get("name"): i.get("value") for i in inputs if i.get("name")}
    data["body"] = msg
    res = session.post(send_url, headers=headers, data=data)
    return res.status_code == 200

print(rgb(200, 100, 255) + "\n🚀 BẮT ĐẦU GỬI (Ctrl+C để dừng sớm)")
try:
    msg_count = 0
    img_count = 0
    while True:
        if mode == '1':
            msg = messages[msg_count % len(messages)] if messages else "[empty]"
            ok = send_text(msg)
            print((Fore.GREEN if ok else Fore.RED) + f"Gửi: {msg}")
            msg_count += 1

        elif mode == '2':
            msg = random.choice(messages) if messages else "[empty]"
            ok = send_text(msg)
            print((Fore.GREEN if ok else Fore.RED) + f"Random: {msg}")
            msg_count += 1

        elif mode == '3':
            img = images[img_count % len(images)] if images else None
            if img:
                img_ok = send_image(img)
                print((Fore.GREEN if img_ok else Fore.RED) + f"Ảnh gửi: {img}")
                img_count += 1
            if messages:
                msg = messages[msg_count % len(messages)]
                ok = send_text(msg)
                print((Fore.GREEN if ok else Fore.RED) + f"Tin: {msg}")
                msg_count += 1

        elif mode == '4':
            img = images[img_count % len(images)] if images else None
            if img:
                img_ok = send_image(img)
                print((Fore.GREEN if img_ok else Fore.RED) + f"Gửi ảnh: {img}")
                img_count += 1

        elif mode == '5':
            if images:
                img = random.choice(images)
                img_ok = send_image(img)
                print((Fore.GREEN if img_ok else Fore.RED) + f"Gửi ảnh ngẫu nhiên: {img}")
                img_count += 1

        else:
            break

        time.sleep(delay)
except KeyboardInterrupt:
    print(Fore.YELLOW + "\n⛔ Dừng bởi người dùng.")
