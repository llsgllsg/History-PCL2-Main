import os
import requests

# 登录 URL
login_url = 'http://pclhomeplazaoss.lingyunawa.top:26994/api/auth/login'

# 从环境变量中获取用户名和密码
username = os.getenv('ALIST_USERNAME')
password = os.getenv('ALIST_PASSWORD')

# 登录请求数据
data = {
    'Username': username,
    'Password': password
}

# 发送 POST 请求获取 Token
response = requests.post(login_url, data=data)

# 检查是否成功获取 Token
if response.status_code == 200:
    # 假设返回的数据包含 token，通常是 JSON 格式
    token = response.json().get('token')
    print(f"Login successful, Token: {token}")
else:
    print(f"Login failed. Status code: {response.status_code}, Response: {response.text}")
    exit(1)

# Alist 上传配置
alist_url = 'http://pclhomeplazaoss.lingyunawa.top:26994/api/fs/put'  # 上传接口
file_path = os.getenv('FILE_PATH')  # 本地文件路径
target_path = os.getenv('TARGET_PATH')  # 目标路径（在 Alist 上）

# URL 编码目标文件路径
from urllib.parse import quote
encoded_target_path = quote(target_path)

# 读取文件内容
with open(file_path, 'rb') as f:
    file_content = f.read()

# 获取文件大小
content_length = str(len(file_content))

# 设置请求头
headers = {
    'Authorization': f'Bearer {token}',
    'File-Path': encoded_target_path,
    'Content-Type': 'application/octet-stream',
    'Content-Length': content_length,
}

# 发送 PUT 请求上传文件
response = requests.put(alist_url, headers=headers, data=file_content)

# 检查响应
if response.status_code == 200:
    print(f"File {file_path} uploaded successfully to {target_path}.")
else:
    print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
