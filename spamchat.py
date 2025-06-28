import requests, time, os
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

def color_input(prompt, color=Fore.YELLOW):
    return input(color + prompt + Style.RESET_ALL).strip()

def banner():
    print(Fore.CYAN + "╔" + "═"*38 + "╗")
    print(Fore.CYAN + "║" + Fore.MAGENTA + "   🖼️📩 oibanoi874 Spam Chat    " + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═"*38 + "╝\n")

banner()

cookie_input = color_input("👉 Nhập cookie: ")
receiver_id = color_input("🎯 ID người nhận: ")
message = color_input("💬 Tin nhắn muốn gửi: ")
image_path = color_input("🖼️ Đường dẫn ảnh: ")
delay = float(color_input("⏱️ Độ trễ mỗi lần gửi (giây): "))

cookies = {}
for part in cookie_input.split(";"):
    if "=" in part:
        k, v = part.strip().split("=", 1)
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
print(Fore.GREEN + "✅ Lấy fb_dtsg thành công!\n")

def send_image():
    if not os.path.exists(image_path):
        print(Fore.RED + f"❌ Không tìm thấy ảnh: {image_path}")
        return False
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

print(Fore.MAGENTA + "\n🚀 BẮT ĐẦU GỬI ẢNH + TIN NHẮN (Ctrl+C để dừng)\n")
try:
    while True:
        img_ok = send_image()
        print(Fore.GREEN + "🖼️ Ảnh đã gửi!" if img_ok else Fore.RED + "❌ Lỗi gửi ảnh.")

        txt_ok = send_text(message)
        print(Fore.GREEN + f"💬 Tin nhắn: {message}" if txt_ok else Fore.RED + "❌ Gửi tin nhắn lỗi.")

        time.sleep(delay)
except KeyboardInterrupt:
    print(Fore.YELLOW + "\n⛔ Dừng bởi người dùng.")
