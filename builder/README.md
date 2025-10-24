# 打包工具

将 Python 脚本打包为 Windows 可执行文件（.exe），用户无需安装 Python 和依赖。

## 快速使用

### 1. 准备 ADB 工具（仅首次需要）

下载并解压到项目根目录：
```
https://dl.google.com/android/repository/platform-tools-latest-windows.zip
```

确保有 `platform-tools` 文件夹。

### 2. 一键打包

双击运行：
```
一键打包.bat
```

### 3. 输出位置

```
dist/淘宝双11自动化工具/
```

## 文件说明

- `一键打包.bat` - 自动安装依赖并打包（首次使用）
- `重新打包.bat` - 清理旧文件并重新打包（修改代码后使用）
- `检查环境.bat` - 检查打包环境是否就绪
- `build_exe.py` - Python 打包脚本
- `build_simple.spec` - PyInstaller 配置文件

