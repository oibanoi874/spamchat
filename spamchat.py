import requests, time, os, random
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

def color_input(prompt, color=Fore.YELLOW):
    return input(color + prompt + Style.RESET_ALL).strip()

def banner():
    print(Fore.CYAN + "\n╔" + "═"*50 + "╗")
    print(Fore.CYAN + "║" + Fore.MAGENTA + "         💥 Oinanoi874 Spam Chat 💥         " + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═"*50 + "╣")
    print(Fore.CYAN + "║" + Fore.GREEN + " 1. Gửi lần lượt tin nhắn" + " "*22 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + " 2. Gửi ngẫu nhiên tin nhắn" + " "*20 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + " 3. Gửi so le ảnh + tin nhắn" + " "*18 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + " 4. Gửi ảnh tuần tự" + " "*27 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + " 5. Gửi ảnh ngẫu nhiên" + " "*24 + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═"*50 + "╝\n")

banner()

cookie_input = color_input("👉 Nhập cookie (full): ")
receiver_id = color_input("🎯 ID người nhận: ")
mode = color_input("📌 Nhập số chức năng (1 → 5): ")
delay = float(color_input("⏱️ Độ trễ giữa các lần gửi (giây): "))

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
session.cookies.update({"c_user": c_user, "xs": xs})
headers = {"User-Agent": "Mozilla/5.0"}

print(Fore.BLUE + "\n🔍 Đang lấy fb_dtsg...")
res = session.get("https://mbasic.facebook.com/messages/", headers=headers)
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
    read_url = f"https://mbasic.facebook.com/messages/read/?tid=user:{receiver_id}"
    res = session.get(read_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
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
    payload = {
        "body": msg,
        "tids": f"user:{receiver_id}",
        "wwwupp": "C3",
        "fb_dtsg": fb_dtsg,
        "csid": "autospam",
        "__a": 1,
        "__req": "q",
        "__user": c_user
    }
    res = session.post("https://www.facebook.com/messaging/send/", headers=headers, data=payload)
    return res.status_code == 200

print(Fore.MAGENTA + "\n🚀 BẮT ĐẦU GỬI (Ctrl+C để dừng sớm)")
try:
    msg_count = 0
    img_count = 0
    while True:
        if mode == '1':  # gửi lần lượt
            msg = messages[msg_count % len(messages)] if messages else "[empty]"
            ok = send_text(msg)
            print(Fore.GREEN + f"✅ Gửi: {msg}" if ok else Fore.RED + "❌ Lỗi gửi tin")
            msg_count += 1

        elif mode == '2':  # gửi random
            msg = random.choice(messages) if messages else "[empty]"
            ok = send_text(msg)
            print(Fore.GREEN + f"✅ Random: {msg}" if ok else Fore.RED + "❌ Lỗi gửi tin")
            msg_count += 1

        elif mode == '3':  # gửi so le ảnh + tin nhắn
            img = images[img_count % len(images)] if images else None
            if img:
                img_ok = send_image(img)
                print(Fore.GREEN + f"🖼️ Ảnh gửi: {img}" if img_ok else Fore.RED + "❌ Gửi ảnh lỗi")
                img_count += 1
            if messages:
                msg = messages[msg_count % len(messages)]
                ok = send_text(msg)
                print(Fore.GREEN + f"✅ Tin: {msg}" if ok else Fore.RED + "❌ Gửi tin lỗi")
                msg_count += 1

        elif mode == '4':  # gửi ảnh tuần tự
            img = images[img_count % len(images)] if images else None
            if img:
                img_ok = send_image(img)
                print(Fore.GREEN + f"🖼️ Gửi ảnh: {img}" if img_ok else Fore.RED + "❌ Ảnh lỗi")
                img_count += 1

        elif mode == '5':  # gửi ảnh ngẫu nhiên
            if images:
                img = random.choice(images)
                img_ok = send_image(img)
                print(Fore.GREEN + f"🖼️ Gửi ảnh ngẫu nhiên: {img}" if img_ok else Fore.RED + "❌ Ảnh lỗi")
                img_count += 1

        else:
            break

        time.sleep(delay)
except KeyboardInterrupt:
    print(Fore.YELLOW + "\n⛔ Dừng bởi người dùng.")
