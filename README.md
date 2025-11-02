# 淘宝双11自动化工具

使用 uiautomator2 自动化完成2025年淘金币任务和体力任务。

## 功能特点

- ✅ 自动完成淘金币任务（默认目标40次，可配置）
- ✅ 自动完成赚体力任务（默认目标50次，可配置）
- ✅ 自动跳一跳游戏（可配置保留体力值）
- ✅ 智能任务过滤（排除需要人工参与的任务）
- ✅ 自动处理弹窗和广告
- ✅ 进度检查和任务完成提示
- ✅ 支持配置文件和命令行参数
- ✅ **Hydra配置管理**：通过配置文件轻松调整所有参数
- ✅ **灵活的任务控制**：可以选择性开启/关闭金币、体力、跳一跳任务
- ✅ **命令行参数覆盖**：无需修改文件即可临时调整配置
---

## 快速开始

### 方式一：直接运行（需要 Python 环境）

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 连接设备

- 使用 USB 数据线连接手机到电脑
- 在手机上开启 **USB 调试** 模式
- 确认手机授权弹窗

#### 3. 配置任务参数（可选）

编辑 `conf/config.yaml` 文件，调整任务参数：

```yaml
task:
  coin:
    target_count: 40  # 金币任务目标次数
    enabled: true     # 是否执行
  physical:
    target_count: 50  # 体力任务目标次数
    enabled: true
  jump:
    enabled: true     # 是否执行跳一跳
    min_physical: 10  # 最少保留体力
```


#### 4. 运行脚本

**基础运行：**
```bash
python "2025淘宝双11.py"
```

**使用命令行参数（无需修改配置文件）：**
```bash
# 只做金币任务
python "2025淘宝双11.py" task.physical.enabled=false task.jump.enabled=false

# 修改目标次数
python "2025淘宝双11.py" task.coin.target_count=50

# 加快浏览速度
python "2025淘宝双11.py" operation.browse_duration=15
```

或使用 conda：
```bash
conda run -p <your_conda_path> --no-capture-output python "2025淘宝双11.py"
```

---

### 方式二：使用打包的 EXE（无需 Python）

#### 开发者打包步骤

1. **准备 ADB 工具**（仅首次需要）
   
   下载：https://dl.google.com/android/repository/platform-tools-latest-windows.zip
   
   解压到项目根目录，确保有 `platform-tools` 文件夹

2. **一键打包**
   
   双击运行：`builder\一键打包.bat`
   
   等待 5-10 分钟，打包完成后会输出到 `dist/淘宝双11自动化工具/`

3. **分发给用户**
   
   将 `dist/淘宝双11自动化工具/` 整个文件夹压缩为 zip 分发

#### 用户使用步骤

1. 解压 zip 文件
2. 连接手机并开启 USB 调试
3. 双击 `launcher.bat` 或 `淘宝双11自动化工具.exe` 启动

**用户无需：**
- ❌ 安装 Python
- ❌ 安装依赖包
- ❌ 手动配置 ADB

---

## 手机设置指南

### 开启 USB 调试

#### 小米/Redmi
1. 设置 → 我的设备 → 全部参数 → 连续点击"MIUI版本"7次
2. 设置 → 更多设置 → 开发者选项 → 开启"USB调试"

#### 华为/荣耀
1. 设置 → 关于手机 → 连续点击"版本号"7次
2. 设置 → 系统和更新 → 开发人员选项 → 开启"USB调试"

#### OPPO/Vivo
1. 设置 → 关于手机 → 连续点击"版本号"7次
2. 设置 → 其他设置 → 开发者选项 → 开启"USB调试"

### 验证连接

```bash
# 进入 platform-tools 目录
cd platform-tools

# 查看连接的设备
adb devices
```

应该显示类似：
```
List of devices attached
1234567890      device
```

---

## 项目结构

```
coin11-tb/
├── 2025淘宝双11.py          # 主程序脚本
├── utils.py                 # 工具函数库
├── requirements.txt         # Python 依赖列表
├── README.md                # 项目说明（本文件）
├── platform-tools/          # ADB 工具（需要下载）
│   ├── adb.exe
│   └── ...
├── builder/                 # 打包工具目录
│   ├── 一键打包.bat         # 一键打包脚本
│   ├── 重新打包.bat         # 重新打包脚本
│   ├── 检查环境.bat         # 环境检查
│   ├── build_exe.py         # Python 打包脚本
│   └── build_simple.spec    # PyInstaller 配置
├── dist/                    # 打包输出目录
│   └── 淘宝双11自动化工具/
└── build/                   # 临时构建文件
```

---

## 依赖项

```
uiautomator2>=3.0.0    # Android 自动化框架
opencv-python>=4.8.0   # 图像处理
numpy>=1.24.0          # 数值计算
ddddocr>=1.4.11        # OCR 识别
Pillow>=10.0.0         # 图像处理
```

---

## 使用说明

### 运行流程

1. **程序启动**
   - 连接设备
   - 启动淘宝应用
   - 初始化监视器

2. **第一阶段：赚金币任务**
   - 自动导航到任务列表
   - 循环完成金币任务
   - 达到40次或无任务后结束

3. **第二阶段：赚体力任务**
   - 切换到体力任务页面
   - 循环完成体力任务
   - 达到40次或无任务后结束

4. **第三阶段：跳一跳**
   - 自动玩跳一跳游戏
   - 消耗剩余体力
   - 体力低于10时停止

5. **完成**
   - 显示总耗时和完成任务数
   - 等待用户按键退出

### 注意事项

- ⚠️ 程序运行时请保持手机屏幕常亮
- ⚠️ 不要手动操作手机，让程序自动执行
- ⚠️ 确保手机已安装淘宝 App
- ⚠️ 网络连接稳定，避免中途断网

---

## 打包相关

### 打包脚本说明

| 脚本 | 说明 | 使用时机 |
|------|------|----------|
| `builder/一键打包.bat` | 自动安装依赖并打包 | 首次打包 |
| `builder/重新打包.bat` | 清理并重新打包 | 修改代码后 |
| `builder/检查环境.bat` | 检查打包环境 | 打包前检查 |

### 打包后文件结构

```
淘宝双11自动化工具/
├── 淘宝双11自动化工具.exe    # 主程序
├── launcher.bat              # 启动器
├── 使用说明.txt              # 用户文档
├── platform-tools/           # ADB 工具
└── _internal/                # 运行时依赖
```

### 打包要求

- Python 3.7+
- PyInstaller 6.0+
- platform-tools（Android SDK Platform Tools）

详细打包说明见 `builder/README.md`

---

## 常见问题

### Q: 提示找不到设备？
**A:** 
- 检查 USB 连接是否正常
- 检查是否已开启 USB 调试
- 尝试重新插拔 USB 线
- 在手机上确认授权弹窗

### Q: 程序运行后没有反应？
**A:** 
- 确保淘宝 App 已安装
- 检查手机是否解锁
- 查看是否有弹窗阻止自动化

### Q: 任务无法完成？
**A:** 
- 淘宝界面可能更新，脚本需要适配
- 检查网络连接是否稳定
- 查看控制台日志定位问题

### Q: 打包后文件很大（500MB+）？
**A:** 正常现象，包含了 Python 运行时、OpenCV、OCR 模型等依赖

### Q: 杀毒软件报毒？
**A:** PyInstaller 打包的程序可能被误报，添加到白名单即可

---

## 开发调试

### 查看 UI 组件

```bash
pip install uiautodev
uiauto.dev
```

### 获取当前应用信息

```bash
adb shell dumpsys window | grep mCurrentFocus
# Windows: findstr 代替 grep
```

### 截图和 UI 层级

```bash
# 截图
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .

# UI 层级
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml .
```

---

## 致谢

主要代码逻辑来自于 [coin11-tb 项目](https://github.com/czl0325/coin11-tb)。

本项目在原项目基础上进行了优化：
- 修复了入口查找和死循环问题
- 优化了任务导航逻辑
- 增加了进度检查功能
- 改进了错误处理机制
- 可以一键自动完成金币和体力任务
- 完善了打包方案

---

## 许可证

本项目仅供学习交流使用，请勿用于商业目的。