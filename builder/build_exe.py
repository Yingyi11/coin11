#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建淘宝双11自动化工具的Windows可执行文件
"""
import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile

# 切换到项目根目录
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
os.chdir(root_dir)
print(f"当前工作目录: {os.getcwd()}")
print()

def download_adb():
    """下载 ADB 工具"""
    print("正在下载 ADB 工具...")
    adb_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    adb_zip = "platform-tools.zip"
    
    # 检查是否已下载
    if os.path.exists("platform-tools"):
        print("✓ ADB 工具已存在")
        return
    
    try:
        print(f"从 {adb_url} 下载...")
        urllib.request.urlretrieve(adb_url, adb_zip)
        print("✓ 下载完成，正在解压...")
        
        with zipfile.ZipFile(adb_zip, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        os.remove(adb_zip)
        print("✓ ADB 工具解压完成")
    except Exception as e:
        print(f"✗ 下载 ADB 失败: {e}")
        print("请手动下载 platform-tools 并放置在当前目录")
        sys.exit(1)

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在检查 PyInstaller...")
    try:
        subprocess.check_output([sys.executable, "-m", "PyInstaller", "--version"], 
                               stderr=subprocess.STDOUT)
        print("✓ PyInstaller 已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安装完成")

def build_exe():
    """构建可执行文件"""
    print("\n开始构建可执行文件...")
    
    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--name=淘宝双11自动化工具",
        "--onedir",  # 使用单目录模式，方便携带 ADB
        "--console",  # 显示控制台窗口，方便查看日志和关闭程序
        "--icon=NONE",
        "--add-data=utils.py;.",
        "--add-data=platform-tools;platform-tools",
        "--hidden-import=uiautomator2",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=ddddocr",
        "--hidden-import=PIL",
        "--collect-all=uiautomator2",
        "--collect-all=cv2",
        "--collect-all=ddddocr",
        "2025淘宝双11.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ 构建成功！")
        print(f"可执行文件位置: {os.path.abspath('dist/淘宝双11自动化工具')}")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 构建失败: {e}")
        sys.exit(1)

def create_launcher():
    """创建启动器脚本"""
    print("\n创建启动器...")
    
    launcher_content = '''@echo off
chcp 65001 >nul
title 淘宝双11自动化工具

echo ====================================
echo   淘宝双11自动化工具
echo ====================================
echo.

REM 设置 ADB 环境变量
set PATH=%~dp0platform-tools;%PATH%

REM 检查设备连接
echo 正在检查设备连接...
adb devices

echo.
echo 按任意键启动程序...
pause >nul

REM 启动主程序
"%~dp0淘宝双11自动化工具.exe"

echo.
echo 程序已结束
pause
'''
    
    with open("launcher.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✓ 启动器创建完成: launcher.bat")

def create_readme():
    """创建使用说明"""
    print("\n创建使用说明...")
    
    readme_content = '''# 淘宝双11自动化工具 - 使用说明

## 快速开始

1. **连接安卓设备**
   - 使用 USB 数据线连接手机到电脑
   - 在手机上开启"USB 调试"模式
   - 首次连接需要在手机上确认授权

2. **运行程序**
   - 双击 `launcher.bat` 启动程序
   - 或直接双击 `淘宝双11自动化工具.exe`

## 重要提示

- 程序运行时请保持手机屏幕常亮
- 不要手动操作手机，让程序自动执行
- 确保手机已安装淘宝 App
- 首次使用建议先测试几个任务，确认运行正常

## 开启 USB 调试

### 小米/Redmi
1. 设置 → 我的设备 → 全部参数 → 连续点击"MIUI 版本"7次
2. 设置 → 更多设置 → 开发者选项 → 开启"USB 调试"

### 华为/荣耀
1. 设置 → 关于手机 → 连续点击"版本号"7次
2. 设置 → 系统和更新 → 开发人员选项 → 开启"USB 调试"

### OPPO/Vivo
1. 设置 → 关于手机 → 连续点击"版本号"7次
2. 设置 → 其他设置 → 开发者选项 → 开启"USB 调试"

## 常见问题

**Q: 提示找不到设备？**
A: 
- 检查 USB 连接是否正常
- 检查是否已开启 USB 调试
- 尝试重新插拔 USB 线
- 在手机上确认授权弹窗

**Q: 程序运行后没有反应？**
A: 
- 确保淘宝 App 已安装
- 检查手机是否解锁
- 查看是否有弹窗阻止自动化

**Q: 任务完成不正确？**
A: 淘宝界面可能更新，请联系开发者更新脚本

## 技术支持

如遇问题，请查看抖音/快手教程或联系开发者。

---
构建时间: {build_time}
'''
    
    from datetime import datetime
    readme_content = readme_content.format(build_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open("使用说明.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ 使用说明创建完成: 使用说明.txt")

def main():
    print("=" * 60)
    print("淘宝双11自动化工具 - 打包脚本")
    print("=" * 60)
    print()
    
    # 步骤1: 下载 ADB
    download_adb()
    
    # 步骤2: 安装 PyInstaller
    install_pyinstaller()
    
    # 步骤3: 构建可执行文件
    build_exe()
    
    # 步骤4: 复制 ADB 到 dist 目录
    print("\n复制 ADB 工具到输出目录...")
    dist_dir = os.path.join("dist", "淘宝双11自动化工具")
    if os.path.exists(dist_dir):
        adb_dest = os.path.join(dist_dir, "platform-tools")
        if os.path.exists("platform-tools"):
            if os.path.exists(adb_dest):
                shutil.rmtree(adb_dest)
            shutil.copytree("platform-tools", adb_dest)
            print("✓ ADB 工具已复制")
    
    # 步骤5: 创建启动器和说明
    os.chdir(dist_dir)
    create_launcher()
    create_readme()
    
    print("\n" + "=" * 60)
    print("✓ 打包完成！")
    print("=" * 60)
    print(f"\n输出目录: {os.path.abspath('.')}")
    print("\n请将整个文件夹分发给用户，双击 launcher.bat 即可运行")
    print("\n文件清单:")
    print("  - 淘宝双11自动化工具.exe  (主程序)")
    print("  - launcher.bat          (启动器)")
    print("  - 使用说明.txt           (使用文档)")
    print("  - platform-tools/       (ADB 工具)")
    print("  - _internal/            (程序依赖)")

if __name__ == "__main__":
    main()
