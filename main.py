import aiohttp
import asyncio
import random
import string
import os

# File proxy với định dạng IP:PORT:USER:PASS
PROXY_FILE = "proxy_2.txt"
SUCCESS_FILE = "success.txt"

def load_proxies(file_path=PROXY_FILE):
    proxies = []
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file {file_path}")
        return proxies
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 4:
                    ip, port, user, passwd = parts
                    proxies.append({
                        "url": f"http://{ip}:{port}",
                        "user": user,
                        "pass": passwd
                    })
    return proxies

def generate_random_string(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_credentials():
    username = generate_random_string(10)
    email = f"{generate_random_string(8)}@gmail.com"
    password = generate_random_string(12)
    return username, email, password

async def register_account(session, username, email, password, proxy):
    data = {
        'username': username,
        'email': email,
        'password': password,
        'repassword': password,
        'recaptcha': '',
    }

    try:
        async with session.post(
            'https://randomtdat.site/ajaxs/client/register.php',
            data=data,
            proxy=proxy["url"],
            proxy_auth=aiohttp.BasicAuth(proxy["user"], proxy["pass"]),
            timeout=10
        ) as response:
            text = await response.text()
            if response.status == 200:
                print(f"✅ Đăng ký thành công: {username} | Email: {email} | Proxy: {proxy['url']}")
                with open(SUCCESS_FILE, "a") as f:
                    f.write(f"{username}:{email}:{password}\n")
                return True
            else:
                print(f"❌ Đăng ký thất bại: {username} | Proxy: {proxy['url']} | Status: {response.status}")
                return False
    except Exception as e:
        print(f"⚠️ Lỗi: {username} | Proxy: {proxy['url']} | {str(e)}")
        return False

async def main():
    proxies = load_proxies()
    if not proxies:
        print("Không tìm thấy proxy hợp lệ.")
        return

    semaphore = asyncio.Semaphore(10)
    account_count = 0

    async def bounded_register(username, email, password, proxy):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await register_account(session, username, email, password, proxy)

    while True:
        tasks = []
        for _ in range(10):
            username, email, password = generate_unique_credentials()
            proxy = random.choice(proxies)
            tasks.append(bounded_register(username, email, password, proxy))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if result:
                account_count += 1
        print(f"Tổng account đã đăng ký thành công: {account_count}")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
