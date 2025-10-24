@echo off
REM =====================================================
REM 淘宝双11自动化工具 - 一键打包脚本
REM =====================================================
chcp 65001 >nul
title 淘宝双11自动化工具 - 打包程序

echo.
echo ====================================================
echo   淘宝双11自动化工具 - 一键打包
echo ====================================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."
echo 当前工作目录: %CD%
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误: 未检测到 Python，请先安装 Python 3.7 或更高版本
    echo.
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python 已安装
python --version
echo.

REM 安装依赖
echo [1/4] 安装 Python 依赖包...
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
echo.
echo ✓ 依赖安装完成
echo.

REM 下载 ADB（如果不存在）
if not exist "platform-tools" (
    echo [2/4] 下载 ADB 工具...
    echo.
    echo 请手动下载 Android Platform Tools 并解压到当前目录
    echo 下载地址: https://dl.google.com/android/repository/platform-tools-latest-windows.zip
    echo.
    echo 下载完成后，请解压 zip 文件到当前目录，确保有 platform-tools 文件夹
    echo.
    pause
) else (
    echo [2/4] ✓ ADB 工具已存在
    echo.
)

REM 清理旧的构建文件
echo [3/4] 清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "淘宝双11自动化工具.spec" del /q "淘宝双11自动化工具.spec"
echo ✓ 清理完成
echo.

REM 开始打包
echo [4/4] 开始打包程序...
echo.

pyinstaller --name=淘宝双11自动化工具 ^
    --onedir ^
    --console ^
    --add-data="utils.py;." ^
    --add-data="platform-tools;platform-tools" ^
    --hidden-import=uiautomator2 ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=ddddocr ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --collect-all=uiautomator2 ^
    "2025淘宝双11.py"

if errorlevel 1 (
    echo.
    echo ✗ 打包失败，请查看上方错误信息
    pause
    exit /b 1
)

REM 创建启动器
echo.
echo 创建启动器和使用说明...
cd dist\淘宝双11自动化工具

REM 创建 launcher.bat
(
echo @echo off
echo chcp 65001 ^>nul
echo title 淘宝双11自动化工具
echo.
echo ====================================
echo   淘宝双11自动化工具
echo ====================================
echo.
echo REM 设置 ADB 环境变量
echo set PATH=%%~dp0platform-tools;%%PATH%%
echo.
echo REM 检查设备连接
echo echo 正在检查设备连接...
echo adb devices
echo.
echo echo.
echo echo 按任意键启动程序...
echo pause ^>nul
echo.
echo REM 启动主程序
echo "%%~dp0淘宝双11自动化工具.exe"
echo.
echo if errorlevel 1 ^(
echo     echo.
echo     echo 程序运行出错
echo     pause
echo ^)
echo.
echo echo.
echo echo 程序已结束
echo pause
) > launcher.bat

REM 创建使用说明
(
echo ====================================
echo   淘宝双11自动化工具 - 使用说明
echo ====================================
echo.
echo 一、快速开始
echo.
echo 1. 连接安卓设备
echo    - 使用 USB 数据线连接手机到电脑
echo    - 在手机上开启 "USB 调试" 模式
echo    - 首次连接需要在手机上确认授权
echo.
echo 2. 运行程序
echo    - 双击 launcher.bat 启动程序
echo    - 或直接双击 淘宝双11自动化工具.exe
echo.
echo 二、开启 USB 调试
echo.
echo 小米/Redmi:
echo   设置 → 我的设备 → 全部参数 → 连续点击"MIUI版本"7次
echo   设置 → 更多设置 → 开发者选项 → 开启"USB调试"
echo.
echo 华为/荣耀:
echo   设置 → 关于手机 → 连续点击"版本号"7次
echo   设置 → 系统和更新 → 开发人员选项 → 开启"USB调试"
echo.
echo OPPO/Vivo:
echo   设置 → 关于手机 → 连续点击"版本号"7次
echo   设置 → 其他设置 → 开发者选项 → 开启"USB调试"
echo.
echo 三、重要提示
echo.
echo - 程序运行时请保持手机屏幕常亮
echo - 不要手动操作手机，让程序自动执行
echo - 确保手机已安装淘宝 App
echo - 首次使用建议先测试几个任务
echo.
echo 四、常见问题
echo.
echo Q: 提示找不到设备？
echo A: 检查 USB 连接、USB 调试是否开启、重新授权
echo.
echo Q: 程序运行后没有反应？
echo A: 确保淘宝已安装、手机已解锁、关闭弹窗
) > 使用说明.txt

cd ..\..

echo.
echo ====================================================
echo ✓ 打包完成！
echo ====================================================
echo.
echo 输出目录: %CD%\dist\淘宝双11自动化工具
echo.
echo 文件清单:
echo   - 淘宝双11自动化工具.exe  (主程序)
echo   - launcher.bat            (启动器，推荐使用)
echo   - 使用说明.txt             (使用文档)
echo   - platform-tools/         (ADB工具)
echo   - _internal/              (程序依赖)
echo.
echo 请将整个 "淘宝双11自动化工具" 文件夹分发给用户
echo 用户双击 launcher.bat 即可运行
echo.

REM 询问是否打开输出目录
echo 是否打开输出目录？(Y/N)
set /p open_dir=
if /i "%open_dir%"=="Y" (
    explorer "dist\淘宝双11自动化工具"
)

echo.
pause
