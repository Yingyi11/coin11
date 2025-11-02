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

## 打包内容

打包后的文件夹包含：

- ✅ 主程序 (`淘宝双11自动化工具.exe`)
- ✅ 启动器 (`launcher.bat`)
- ✅ 配置文件 (`conf/config.yaml`) - **用户可修改**
- ✅ 工具目录 (`utils/`)
- ✅ ADB工具 (`platform-tools/`)
- ✅ 使用说明 (`使用说明.txt`)

## 配置文件说明

**重要更新**: 现在打包会包含 `conf/config.yaml` 配置文件，用户可以通过编辑配置文件来调整：

- 任务开关（金币/体力/跳一跳）
- 目标次数
- 浏览时长
- 等待时间
- 搜索关键词等

用户修改配置后直接运行即可，无需重新打包！

