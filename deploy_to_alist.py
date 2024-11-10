import requests
import os
import time

# 登录获取 token
def get_token():
    url = 'http://pclhomeplazaoss.lingyunawa.top:26994/api/auth/login'
    data = {'Username': 'your_username', 'Password': 'your_password'}
    response = requests.post(url, data=data)
    response_data = response.json()

    if response.status_code == 200 and 'data' in response_data:
        token = response_data['data']['token']
        return token
    else:
        raise Exception("无法获取 token，请检查账号密码或登录接口")

# 上传文件的函数
def upload_file(token, file_path, target_path):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/octet-stream'
    }

    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # 上传文件
    upload_url = 'http://pclhomeplazaoss.lingyunawa.top:26994/api/fs/put'
    params = {
        'File-Path': target_path,
        'Content-Length': str(len(file_data))
    }

    # 发起 PUT 请求
    response = requests.put(upload_url, headers=headers, params=params, data=file_data)

    # 处理上传结果
    if response.status_code == 200:
        print(f"文件 {file_path} 上传成功")
    else:
        print(f"上传失败：{response.json()}")

# 主逻辑
def main():
    try:
        # 获取 token
        token = get_token()
        print(f"Token 获取成功: {token}")
        
        # 文件路径列表
        files_to_upload = [
            'file1.txt', 
            'file2.txt',
            # 在此添加其他需要上传的文件
        ]
        
        # 目标目录
        target_directory = 'Homepages/Joker2184'

        # 遍历文件并上传
        for file in files_to_upload:
            if os.path.exists(file):  # 检查文件是否存在
                target_path = os.path.join(target_directory, file)
                print(f"正在上传 {file} 到 {target_path}...")
                upload_file(token, file, target_path)
            else:
                print(f"文件 {file} 不存在，跳过上传")

    except Exception as e:
        print(f"发生错误: {e}")
        # 如果遇到 token 无效，可以重新获取 token 并重新上传
        print("尝试重新获取 token 并继续上传...")
        time.sleep(2)  # 等待几秒钟
        main()  # 递归调用重新运行

if __name__ == '__main__':
    main()
