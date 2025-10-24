@echo off
REM =====================================================
REM 重新打包 - 清理并重新构建
REM =====================================================
chcp 65001 >nul
title 重新打包程序

echo.
echo ====================================
echo   重新打包程序
echo ====================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."

echo 正在清理旧的构建文件...
if exist "build" (
    rmdir /s /q build
    echo ✓ 已删除 build 目录
)
if exist "dist" (
    rmdir /s /q dist
    echo ✓ 已删除 dist 目录
)
if exist "淘宝双11自动化工具.spec" (
    del /q "淘宝双11自动化工具.spec"
    echo ✓ 已删除 spec 文件
)

echo.
echo 清理完成，正在重新打包...
echo.

call builder\一键打包.bat
