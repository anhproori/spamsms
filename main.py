import aiohttp
import asyncio
import random
import string
import time
import platform
import os

# Hàm tạo random string
def generate_random_string(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Hàm tạo tài khoản unique
def generate_unique_credentials():
    username = generate_random_string(10)
    email = f"{generate_random_string(8)}@gmail.com"
    password = "hixinchao"
    return username, email, password

# Hàm đăng ký tài khoản
async def register_account(session, username, email, password):
    data = {
        'username': username,
        'email': email,
        'password': password,
        'repassword': password,
        'recaptcha': '',
    }
    try:
        async with session.post('https://randomtdat.site/ajaxs/client/register.php', data=data, timeout=10) as response:
            text = await response.text()
            if response.status == 200:
                print(f"Đăng ký thành công - Username: {username}, Email: {email}")
                with open("success.txt", "a") as f:
                    f.write(f"{username}:{email}:{password}\n")
                return True
            else:
                print(f"Đăng ký thất bại - Username: {username}, Email: {email}, Status: {response.status}")
                return False
    except Exception as e:
        print(f"Lỗi - Username: {username}, Email: {email}, Lỗi: {str(e)}")
        return False

# Hàm chính
async def main():
    account_count = 0
    max_concurrent = 5  # số luồng chạy cùng lúc
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_register(username, email, password):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await register_account(session, username, email, password)
    
    while True:
        tasks = []
        for _ in range(max_concurrent):
            username, email, password = generate_unique_credentials()
            tasks.append(bounded_register(username, email, password))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if result and not isinstance(result, Exception):
                account_count += 1
                print(f"Tổng tài khoản đã đăng ký: {account_count}")
        
        await asyncio.sleep(0.1)

# Chạy script
if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
