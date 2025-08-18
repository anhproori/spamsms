import aiohttp
import asyncio
import random
import string
import time
import platform

def load_proxies(file_path="proxy_2.txt"):
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    ip, port, user, passw = line.split(':')
                    proxy = f'http://{user}:{passw}@{ip}:{port}'
                    proxies.append(proxy)
        return proxies
    except Exception as e:
        print(f"L: {str(e)}")
        return []

def generate_random_string(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
    
    try:
        async with session.post('https://randomtdat.site/ajaxs/client/register.php', data=data, proxy=proxy, timeout=10) as response:
            if response.status == 200:
                text = await response.text()
                print(f"Đăng ký thành công - Username: {username}, Email: {email}, Proxy: {proxy}, Response: {text}")
                return True
            else:
                text = await response.text()
                print(f"Đăng ký thất bại - Username: {username}, Email: {email}, Proxy: {proxy}, Status: {response.status}, Response: {text}")
                return False
    except Exception as e:
        print(f"L - Username: {username}, Email: {email}, Proxy: {proxy}, Lỗi: {str(e)}")
        return False

async def main():
    proxies = load_proxies()
    if not proxies:
        print("Không tìm thấy file proxy.txt")
        return
    
    account_count = 0
    max_concurrent = 10
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_register(username, email, password, proxy):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await register_account(session, username, email, password, proxy)
    
    while True:
        tasks = []
        for _ in range(max_concurrent):
            username, email, password = generate_unique_credentials()
            proxy = random.choice(proxies)
            tasks.append(bounded_register(username, email, password, proxy))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if result and not isinstance(result, Exception):
                account_count += 1
                print(f"Tổng tài khoản đã đăng ký: {account_count}")
        
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
