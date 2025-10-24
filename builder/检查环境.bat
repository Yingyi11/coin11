@echo off
REM =====================================================
REM 快速测试 - 检查打包环境是否就绪
REM =====================================================
chcp 65001 >nul
title 环境检查

echo.
echo ====================================
echo   环境检查
echo ====================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."
echo 当前工作目录: %CD%
echo.

REM 检查 Python
echo [1/4] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 未安装 Python
    echo.
    echo 请访问 https://www.python.org/downloads/
    echo 下载并安装 Python 3.7 或更高版本
    echo.
    set has_error=1
) else (
    echo ✓ Python 已安装
    python --version
)
echo.

REM 检查 pip
echo [2/4] 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ pip 未安装或不在 PATH 中
    set has_error=1
) else (
    echo ✓ pip 已安装
    pip --version
)
echo.

REM 检查 platform-tools
echo [3/4] 检查 ADB 工具...
if exist "platform-tools\adb.exe" (
    echo ✓ ADB 工具已准备
    platform-tools\adb.exe version
) else (
    echo ✗ 未找到 platform-tools 文件夹
    echo.
    echo 请下载 Android Platform Tools:
    echo https://dl.google.com/android/repository/platform-tools-latest-windows.zip
    echo.
    echo 下载后解压到当前目录，确保有 platform-tools 文件夹
    set has_error=1
)
echo.

REM 检查主脚本
echo [4/4] 检查主脚本文件...
if exist "2025淘宝双11.py" (
    echo ✓ 主脚本文件存在
) else (
    echo ✗ 未找到 2025淘宝双11.py
    set has_error=1
)
if exist "utils.py" (
    echo ✓ utils.py 存在
) else (
    echo ✗ 未找到 utils.py
    set has_error=1
)
echo.

REM 总结
echo ====================================
if defined has_error (
    echo ✗ 检查未通过，请先解决上述问题
    echo ====================================
    echo.
    pause
    exit /b 1
) else (
    echo ✓ 所有检查通过，可以开始打包！
    echo ====================================
    echo.
    echo 请运行: 一键打包.bat
    echo.
    pause
)
