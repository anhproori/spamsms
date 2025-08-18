import aiohttp
import asyncio
import random
import string
import time
import os

# Load proxies từ file proxy.txt
def load_proxies(file_path="proxy.txt"):
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append(line)
        return proxies
    except Exception as e:
        print(f"Lỗi khi load proxy: {str(e)}")
        return []

def generate_random_string(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_credentials():
    username = generate_random_string(10)
    email = f"{generate_random_string(8)}@gmail.com"
    password = "hixinchao"
    return username, email, password

async def register_account(session, username, email, password, proxy):
    data = {
        'username': username,
        'email': email,
        'password': password,
        'repassword': password,
        'recaptcha': '',
    }
    
    proxy_url = f"http://{proxy}"
    
    try:
        async with session.post(
            'https://randomtdat.site/ajaxs/client/register.php',
            data=data,
            proxy=proxy_url,
            timeout=10
        ) as resp:
            text = await resp.text()
            if resp.status == 200:
                print(f"✅ Success - {username} | {email} | Proxy: {proxy}")
                # Ghi vào file success.txt
                with open("success.txt", "a") as f:
                    f.write(f"{username}:{email}:{password}\n")
                return True
            else:
                print(f"❌ Fail - {username} | Status: {resp.status} | Proxy: {proxy}")
                return False
    except Exception as e:
        print(f"⚠️ Lỗi - {username} | {e} | Proxy: {proxy}")
        return False

async def main():
    proxies = load_proxies()
    if not proxies:
        print("Không tìm thấy proxy.txt hoặc proxy trống")
        return

    semaphore = asyncio.Semaphore(5)  # giới hạn task đồng thời

    async def bounded_register(username, email, password, proxy):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                await register_account(session, username, email, password, proxy)

    while True:
        tasks = []
        for _ in range(5):  # 5 tài khoản cùng lúc
            username, email, password = generate_unique_credentials()
            proxy = random.choice(proxies)
            tasks.append(bounded_register(username, email, password, proxy))

        await asyncio.gather(*tasks)
        await asyncio.sleep(1)  # nghỉ 1s trước batch tiếp theo

if __name__ == "__main__":
    asyncio.run(main())
