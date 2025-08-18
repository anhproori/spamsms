import aiohttp
import asyncio
import random
import string
import platform

PROXY_FILE = "proxy_2.txt"
SUCCESS_FILE = "success.txt"
MAX_CONCURRENT = 10
PROXY_TIMEOUT = 5

def load_proxies(file_path=PROXY_FILE):
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) == 4:
                        ip, port, user, passwd = parts
                        proxy = f"http://{user}:{passwd}@{ip}:{port}"
                        proxies.append(proxy)
        if not proxies:
            print(f"❌ Không tìm thấy proxy hợp lệ trong {file_path}")
        return proxies
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {file_path}")
        return []

def generate_random_string(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_credentials():
    username = generate_random_string(10)
    email = f"{generate_random_string(8)}@gmail.com"
    password = "hixinchao"
    return username, email, password

async def validate_proxy(proxy):
    test_url = "http://httpbin.org/ip"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, proxy=proxy, timeout=PROXY_TIMEOUT) as resp:
                if resp.status == 200:
                    return True
    except:
        pass
    return False

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
            data=data, proxy=proxy, timeout=10
        ) as response:
            text = await response.text()
            if response.status == 200:
                print(f"✅ Thành công - {username} | {email} | Proxy: {proxy}")
                with open(SUCCESS_FILE, "a") as f:
                    f.write(f"{username}:{email}:{password}\n")
                return True
            else:
                print(f"❌ Thất bại - {username} | {email} | Status: {response.status} | Proxy: {proxy}")
                return False
    except Exception as e:
        print(f"⚠️ Lỗi - {username} | Proxy: {proxy} | {str(e)}")
        return False

async def bounded_register(semaphore, username, email, password, proxy):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            return await register_account(session, username, email, password, proxy)

async def main():
    proxies = load_proxies()
    if not proxies:
        return

    # Validate proxies trước khi dùng
    print("⏳ Đang kiểm tra proxy...")
    valid_proxies = []
    for proxy in proxies:
        if await validate_proxy(proxy):
            valid_proxies.append(proxy)
    if not valid_proxies:
        print("❌ Không có proxy nào hợp lệ!")
        return
    print(f"✅ Proxy hợp lệ: {len(valid_proxies)} cái")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    account_count = 0

    while True:
        tasks = []
        for _ in range(MAX_CONCURRENT):
            username, email, password = generate_unique_credentials()
            proxy = random.choice(valid_proxies)
            tasks.append(bounded_register(semaphore, username, email, password, proxy))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if r and not isinstance(r, Exception):
                account_count += 1

        print(f"🔹 Tổng tài khoản đã đăng ký: {account_count}\n")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
