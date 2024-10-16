import requests
import re
import os

# GitHub 仓库信息
OWNER = 'Hex-Dragon'
REPO = 'PCL2'

# GitHub API URL
RELEASES_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/releases'

# 个人访问令牌
TOKEN = ''  # 替换为你的 token

# UpdateHomepage.yml 文件路径
YAML_FILE_PATH = r''

def get_version():
    """从 GitHub releases 获取最新的 2.8.x 版本号及其状态"""
    headers = {'Authorization': f'token {TOKEN}'}
    response = requests.get(RELEASES_URL, headers=headers)
    if response.status_code == 200:
        releases = response.json()
        for release in releases:
            version = release['tag_name']
            if re.match(r'2\.8\.\d+', version):
                is_prerelease = release.get('prerelease', False)
                return version, is_prerelease
    else:
        print(f"无法获取 releases: {response.status_code}")
    return None, None

def update_yaml(version, is_prerelease):
    """更新 UpdateHomepage.yml 文件"""
    if is_prerelease:
        version_text = f'快照版{version}'
    else:
        version_text = f'正式版{version}'

    content = f"""cards:
- {version_text}
- ThatCatSay
- PRList
- NewFooter
"""
    with open(YAML_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"YAML 文件已更新至: {YAML_FILE_PATH}")

def main():
    version, is_prerelease = get_version()
    if version:
        update_yaml(version, is_prerelease)
    else:
        print("未找到符合条件的版本号.")

if __name__ == '__main__':
    main()
