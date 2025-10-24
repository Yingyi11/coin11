#!/usr/bin/env python
# -*- coding: utf-8 -*-
print("Python script starting...", flush=True)

import time
import random
import re

print("Importing uiautomator2...", flush=True)
import uiautomator2 as u2

print("Importing utils...", flush=True)
from utils import check_chars_exist, get_current_app

print("=" * 60, flush=True)
print("淘宝双11自动化脚本启动", flush=True)
print("=" * 60)

print("正在连接设备...")
d = u2.connect()
print("✓ 设备连接成功")

print("正在启动淘宝应用...")
d.app_start("com.taobao.taobao", stop=True, use_monkey=True)
print("✓ 淘宝应用已启动")

print("获取屏幕信息...")
screen_width = d.info["displayWidth"]
screen_height = d.info["displayHeight"]
print(f"✓ 屏幕尺寸: {screen_width}x{screen_height}")

print("等待 5 秒让应用完全加载...")
time.sleep(5)
print("✓ 等待完成")

in_search = False
in_other_app = False
have_clicked = []

print("启动监视器上下文...")
ctx = d.watch_context()
# ctx.when("O1CN012qVB9n1tvZ8ATEQGu_!!6000000005964-2-tps-144-144").click()
# ctx.when("O1CN01TkBa3v1zgLfbNmfp7_!!6000000006743-2-tps-72-72").click()
ctx.when("点击刷新").click()
# ctx.when(xpath="//android.app.Dialog//android.widget.Button[@text='关闭']").click()
# ctx.when(xpath="//android.widget.TextView[@package='com.eg.android.AlipayGphone']").click()
ctx.when(
    xpath="//android.widget.FrameLayout[@resource-id='com.taobao.taobao:id/poplayer_native_state_center_layout_frame_id']/android.widget.ImageView"
).click()
ctx.start()
print("✓ 监视器已启动")
print("=" * 60)
print()


def close_all_dialog():
    btn1 = d(className="android.widget.TextView", text="去使用")
    if btn1.exists:
        btn1.right(className="android.widget.ImageView").click()
        time.sleep(2)


def check_in_task():
    temp_package, temp_activity = get_current_app(d)
    if (
        temp_package == "com.taobao.taobao"
        and temp_activity == "com.taobao.themis.container.app.TMSActivity"
    ):
        phy_view = d(className="android.widget.TextView", text="做任务赚体力")
        if phy_view.exists(timeout=5):
            return True
    elif (
        temp_package == "com.taobao.taobao"
        and temp_activity == "com.taobao.tao.welcome.Welcome"
    ):
        to_11()
        return True
    return False


def to_11():
    """导航到任务列表界面的完整流程"""
    print("开始导航到任务列表界面...")
    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        package_name, activity_name = get_current_app(d)
        print(f"[to_11] 当前界面: {package_name}--{activity_name}")

        # 检查是否已在任务界面
        if (
            package_name == "com.taobao.taobao"
            and activity_name == "com.taobao.themis.container.app.TMSActivity"
        ):
            print("✓ 已在任务列表界面")
            time.sleep(2)
            break

        # 检查是否在 Welcome 首屏（使用 elif 避免被后面的 elif 覆盖）
        elif (
            package_name == "com.taobao.taobao"
            and activity_name == "com.taobao.tao.welcome.Welcome"
        ):
            print("[to_11] 在 Welcome 首屏，寻找'领淘金币'...")
            time.sleep(2)  # 等待页面完全加载

            # 第1步：多种方式查找"领淘金币"按钮
            coin_btn = None

            # 方式1: 通过 description 查找
            coin_btn = d(description="领淘金币")
            if not coin_btn.exists:
                print("[to_11] description方式未找到，尝试text方式...")
                # 方式2: 通过 text 查找
                coin_btn = d(text="领淘金币")

            if not coin_btn.exists:
                print("[to_11] text方式未找到，尝试textContains方式...")
                # 方式3: 通过 textContains 查找
                coin_btn = d(textContains="淘金币")

            if not coin_btn.exists:
                print("[to_11] 尝试通过TextView查找...")
                # 方式4: 直接查找TextView
                coin_btn = d(
                    className="android.widget.TextView", textMatches=".*淘金币.*"
                )

            if coin_btn.exists:
                print("✓ 找到'领淘金币'元素，点击...")
                # 获取元素中心坐标并点击，避免边缘点击失败
                bounds = coin_btn.info["bounds"]
                center_x = (bounds["left"] + bounds["right"]) // 2
                center_y = (bounds["top"] + bounds["bottom"]) // 2
                d.click(center_x, center_y)
                print(f"   点击坐标: ({center_x}, {center_y})")
                time.sleep(4)  # 增加等待时间

                # 第2步：等待页面切换，查找"赚金币"或"赚体力"（优先赚金币）
                print("[to_11] 等待'赚金币'/'赚体力'按钮出现...")
                time.sleep(3)  # 增加等待时间

                # 多种方式查找"赚金币"或"赚体力"按钮（优先查找赚金币）
                physical_btn = None

                # 优先尝试查找"赚金币"
                physical_btn = d(text="赚金币")
                if not physical_btn.exists:
                    print("[to_11] 未找到'赚金币'，尝试'赚体力'...")
                    physical_btn = d(text="赚体力")

                if not physical_btn.exists:
                    print("[to_11] 尝试textContains方式...")
                    physical_btn = d(textContains="赚金币")
                    if not physical_btn.exists:
                        physical_btn = d(textContains="赚体力")

                if not physical_btn.exists:
                    print("[to_11] 尝试通过Button查找...")
                    physical_btn = d(
                        className="android.widget.Button", textMatches=".*赚.*"
                    )

                if physical_btn.exists:
                    print(
                        f"✓ 找到按钮: {physical_btn.info.get('text', '未知')}，点击进入任务列表..."
                    )
                    # 同样使用坐标点击
                    bounds = physical_btn.info["bounds"]
                    center_x = (bounds["left"] + bounds["right"]) // 2
                    center_y = (bounds["top"] + bounds["bottom"]) // 2
                    d.click(center_x, center_y)
                    print(f"   点击坐标: ({center_x}, {center_y})")
                    time.sleep(5)

                    # 验证是否成功进入任务列表
                    pkg, act = get_current_app(d)
                    if act == "com.taobao.themis.container.app.TMSActivity":
                        print("✓ 成功进入任务列表界面")
                        break
                    else:
                        print(f"✗ 点击后未立即进入任务列表，当前: {act}")
                        attempt += 1
                else:
                    print("✗ 未找到'赚体力'/'赚金币'按钮")
                    # 打印当前页面信息用于调试
                    print("[to_11] 打印当前页面元素信息...")
                    btns = d(className="android.widget.Button")
                    tvs = d(className="android.widget.TextView")
                    print(f"   页面有 {len(btns)} 个 Button, {len(tvs)} 个 TextView")
                    print("   所有 Button 文本:")
                    for i in range(min(20, len(btns))):
                        try:
                            text = btns[i].get_text()
                            if text:
                                print(f"      [Button {i}] {text}")
                        except:
                            pass
                    print("   所有 TextView 文本(前20个):")
                    for i in range(min(20, len(tvs))):
                        try:
                            text = tvs[i].get_text()
                            if text:
                                print(f"      [TextView {i}] {text}")
                        except:
                            pass

                    # 尝试通过屏幕区域点击
                    print("[to_11] 尝试通过屏幕区域估算点击...")
                    # 假设"赚体力"按钮在屏幕中下方
                    d.click(screen_width // 2, int(screen_height * 0.7))
                    time.sleep(3)
                    attempt += 1
            else:
                print("✗ 未找到'领淘金币'元素")
                # 打印页面信息用于调试
                print("[to_11] 打印当前Welcome页面元素...")
                xml = d.dump_hierarchy()
                if "淘金币" in xml:
                    print("   XML中有'淘金币'关键字")
                    # 尝试查找所有包含"金币"的元素
                    all_views = d(textMatches=".*金币.*")
                    print(f"   找到 {len(all_views)} 个包含'金币'的元素")
                    for i in range(min(5, len(all_views))):
                        try:
                            info = all_views[i].info
                            print(
                                f"      [{i}] class={info.get('className')}, text={info.get('text')}, desc={info.get('contentDescription')}"
                            )
                        except:
                            pass
                else:
                    print("   XML中没有'淘金币'关键字")

                # 尝试通过屏幕坐标点击（估算领淘金币的位置）
                print("[to_11] 尝试通过屏幕坐标点击（估算位置）...")
                # 通常这类入口在屏幕中央或下方
                d.click(screen_width // 2, int(screen_height * 0.5))
                time.sleep(3)
                attempt += 1

        # 其他非Welcome、非目标界面，重启淘宝
        elif package_name == "com.taobao.taobao":
            print(f"[to_11] 在其他淘宝界面: {activity_name}，重启淘宝...")
            d.app_start("com.taobao.taobao", stop=False)
            time.sleep(5)  # 增加等待时间
            attempt += 1
        else:
            print(f"[to_11] 非淘宝应用: {package_name}，启动淘宝...")
            d.app_start("com.taobao.taobao", stop=False)
            time.sleep(5)  # 增加等待时间
            attempt += 1

        if attempt < max_attempts and attempt > 0:
            print(f"[to_11] 第 {attempt}/{max_attempts} 次尝试...")
            time.sleep(2)

    if attempt >= max_attempts:
        print("⚠ 导航到任务界面达到最大尝试次数")
    else:
        print("✓ 成功导航到任务列表界面")

    print("导航流程完成")


def operate_task():
    start_time = time.time()
    cancel_btn = d(resourceId="android:id/button2", text="取消")
    if cancel_btn.exists:
        cancel_btn.click()
        time.sleep(2)
        return

    # 执行模拟滑动操作（浏览任务内容）
    while True:
        if time.time() - start_time > 18:
            break
        start_x = random.randint(screen_width // 6, screen_width // 2)
        start_y = random.randint(screen_height // 2, screen_height - screen_width // 4)
        end_x = random.randint(start_x - 100, start_x)
        end_y = random.randint(start_y - 1200, start_y - 300)
        swipe_time = (
            random.uniform(0.4, 1)
            if end_y - start_y > 500
            else random.uniform(0.2, 0.5)
        )
        print("模拟滑动", start_x, start_y, end_x, end_y, swipe_time)
        d.swipe(start_x, start_y, end_x, end_y, swipe_time)
        time.sleep(random.uniform(1, 3))

    print("开始返回界面")

    # 返回到任务列表的逻辑
    back_count = 0
    max_back = 8
    consecutive_welcome = 0

    while back_count < max_back:
        temp_package, temp_activity = get_current_app(d)
        if temp_package is None or temp_activity is None:
            time.sleep(0.5)
            continue

        print(f"当前界面: {temp_package}--{temp_activity}")

        # 优先检查：如果已经在任务界面，直接成功返回，不再后退
        if (
            temp_package == "com.taobao.taobao"
            and temp_activity == "com.taobao.themis.container.app.TMSActivity"
        ):
            print("✓ 已在任务列表界面，停止后退")
            break

        # 成功返回到任务列表（使用check_in_task进一步验证）
        if check_in_task():
            print("✓ 成功返回到任务列表")
            break

        # Welcome 界面处理
        if temp_activity == "com.taobao.tao.welcome.Welcome":
            consecutive_welcome += 1
            if consecutive_welcome >= 2:
                print(
                    f"⚠ 连续检测到 Welcome {consecutive_welcome} 次，停止返回，调用 to_11() 重新导航"
                )
                to_11()
                break
            print("检测到 Welcome 界面，再尝试后退一次")
            d.press("back")
            time.sleep(1)
            back_count += 1

        # 启动器界面处理
        elif (
            temp_activity == "com.bbk.launcher2.Launcher"
            or "com.taobao.taobao" not in temp_package
        ):
            print("✗ 到达启动器或非淘宝应用，停止返回，调用 to_11() 重新导航")
            to_11()
            break

        # 淘宝内部界面，继续后退
        else:
            print("点击后退")
            d.press("back")
            time.sleep(0.5)
            back_count += 1
            consecutive_welcome = 0  # 重置 Welcome 计数

    print(f"返回界面流程完成（执行了 {back_count} 次后退）")


def check_task_progress(target_count=40):
    """检查任务进度是否达到目标次数"""
    # 查找"完成进度"或"当前进度"文本
    progress_texts = d(className="android.widget.TextView", textMatches=".*进度.*")

    for progress_view in progress_texts:
        try:
            text = progress_view.get_text()
            print(f"[进度检查] 找到进度文本: {text}")

            # 尝试从文本中提取数字，格式可能是 "完成进度 30/40" 或 "当前进度：30/40" 等
            match = re.search(r"(\d+)\s*/\s*(\d+)", text)
            if match:
                current = int(match.group(1))
                total = int(match.group(2))
                print(f"[进度检查] 当前进度: {current}/{total}")

                if current >= target_count or current >= total:
                    print(f"✓ 已达到目标进度 ({current}/{total})")
                    return True
        except Exception as e:
            print(f"[进度检查] 解析进度失败: {e}")
            continue

    print("[进度检查] 未找到进度信息或未达到目标")
    return False


to_11()
finish_count = 0
time1 = time.time()

# 第一阶段：完成赚金币任务
print("\n" + "=" * 60)
print("第一阶段：开始赚金币任务")
print("=" * 60)
while True:
    try:
        # 检查任务进度
        if check_task_progress(40):
            print("✓ 金币任务进度已达到40次，结束金币任务")
            break

        print("开始查找金币任务。。。")
        get_btn = d(className="android.widget.Button", text="立即领取")
        if get_btn.exists:
            get_btn.click()
            time.sleep(3)
        to_btn = d(className="android.widget.Button", text="去完成")
        if to_btn.exists:
            need_click_view = None
            need_click_index = 0
            task_name = None
            for index, view in enumerate(to_btn):
                text_div = view.sibling(
                    className="android.view.View", instance=0
                ).child(className="android.widget.TextView", instance=0)
                if text_div.exists:
                    if check_chars_exist(text_div.get_text()):
                        continue
                    task_name = text_div.get_text()
                    if task_name in have_clicked:
                        continue
                    need_click_index = index
                    need_click_view = view
                    break
            if need_click_view:
                print(f"点击金币任务按钮: {task_name}")
                if task_name not in have_clicked:
                    have_clicked.append(task_name)
                    finish_count += 1
                d.click(
                    random.randint(
                        need_click_view.bounds()[0] + 10,
                        need_click_view.bounds()[2] - 10,
                    ),
                    random.randint(
                        need_click_view.bounds()[1] + 10,
                        need_click_view.bounds()[3] - 10,
                    ),
                )
                time.sleep(4)
                search_view = d(className="android.view.View", text="搜索有福利")
                if search_view.exists:
                    d(className="android.widget.EditText", instance=0).send_keys(
                        "笔记本电脑"
                    )
                    d(className="android.widget.Button", text="搜索").click()
                    in_search = True
                    time.sleep(4)
                operate_task()
            else:
                print("✓ 没有更多可执行的金币任务")
                break
        else:
            print("✓ 没有更多金币任务")
            break
        time.sleep(4)
    except Exception as e:
        print("出现异常，继续下一轮", str(e))

# 第二阶段：切换到赚体力任务
print("\n" + "=" * 60)
print("第二阶段：切换到赚体力任务")
print("=" * 60)

# 检查当前界面，如果在任务界面，先返回到淘金币主页
package_name, activity_name = get_current_app(d)
print(f"[切换体力] 当前界面: {package_name}--{activity_name}")

if activity_name == "com.taobao.themis.container.app.TMSActivity":
    print("[切换体力] 在任务列表界面，返回到淘金币主页...")
    d.press("back")
    time.sleep(3)
    package_name, activity_name = get_current_app(d)
    print(f"[切换体力] 返回后界面: {package_name}--{activity_name}")

# 如果返回到了 Welcome 首页，需要重新点击"领淘金币"进入淘金币页面
if activity_name == "com.taobao.tao.welcome.Welcome":
    print("[切换体力] 在 Welcome 首页，需要重新进入淘金币页面...")

    # 查找并点击"领淘金币"
    coin_btn = d(textContains="淘金币")
    if not coin_btn.exists:
        coin_btn = d(description="领淘金币")
    if not coin_btn.exists:
        coin_btn = d(text="领淘金币")

    if coin_btn.exists:
        print("✓ 找到'领淘金币'，点击进入...")
        bounds = coin_btn.info["bounds"]
        center_x = (bounds["left"] + bounds["right"]) // 2
        center_y = (bounds["top"] + bounds["bottom"]) // 2
        d.click(center_x, center_y)
        print(f"   点击坐标: ({center_x}, {center_y})")
        time.sleep(4)
    else:
        print("✗ 未找到'领淘金币'，尝试估算位置点击...")
        d.click(screen_width // 2, int(screen_height * 0.35))
        time.sleep(4)

# 现在应该在淘金币主页，查找"赚体力"按钮
print("[切换体力] 在淘金币页面，查找'赚体力'按钮...")
time.sleep(2)

# 多种方式查找"赚体力"按钮
physical_btn = d(text="赚体力")
if not physical_btn.exists:
    print("[切换体力] text方式未找到，尝试textContains...")
    physical_btn = d(textContains="赚体力")

if not physical_btn.exists:
    print("[切换体力] 尝试Button类型查找...")
    physical_btn = d(className="android.widget.Button", textMatches=".*赚体力.*")

if not physical_btn.exists:
    print("[切换体力] 尝试TextView类型查找...")
    physical_btn = d(className="android.widget.TextView", textMatches=".*赚体力.*")

if physical_btn.exists:
    print("✓ 找到'赚体力'按钮，点击切换到体力任务...")
    bounds = physical_btn.info["bounds"]
    center_x = (bounds["left"] + bounds["right"]) // 2
    center_y = (bounds["top"] + bounds["bottom"]) // 2
    d.click(center_x, center_y)
    print(f"   点击坐标: ({center_x}, {center_y})")
    time.sleep(5)

    # 验证是否进入体力任务页面
    pkg, act = get_current_app(d)
    if act == "com.taobao.themis.container.app.TMSActivity":
        print("✓ 成功进入体力任务列表界面")
    else:
        print(f"⚠ 点击后界面: {act}，可能未成功进入")
else:
    print("✗ 未找到'赚体力'按钮")
    # 打印当前页面所有元素信息用于调试
    print("[切换体力] 打印当前页面元素信息...")
    btns = d(className="android.widget.Button")
    tvs = d(className="android.widget.TextView")
    print(f"   页面有 {len(btns)} 个 Button, {len(tvs)} 个 TextView")
    print("   所有 Button 文本:")
    for i in range(min(10, len(btns))):
        try:
            text = btns[i].get_text()
            if text:
                print(f"      [Button {i}] {text}")
        except:
            pass
    print("   包含'体力'的 TextView:")
    for tv in tvs:
        try:
            text = tv.get_text()
            if text and "体力" in text:
                print(f"      TextView: {text}")
        except:
            pass

# 执行体力任务
have_clicked_physical = []  # 重置已点击列表，专门用于体力任务
while True:
    try:
        # 检查任务进度
        if check_task_progress(40):
            print("✓ 体力任务进度已达到40次，结束体力任务")
            break

        print("开始查找体力任务。。。")
        get_btn = d(className="android.widget.Button", text="立即领取")
        if get_btn.exists:
            get_btn.click()
            time.sleep(3)
        to_btn = d(className="android.widget.Button", text="去完成")
        if to_btn.exists:
            need_click_view = None
            need_click_index = 0
            task_name = None
            for index, view in enumerate(to_btn):
                text_div = view.sibling(
                    className="android.view.View", instance=0
                ).child(className="android.widget.TextView", instance=0)
                if text_div.exists:
                    if check_chars_exist(text_div.get_text()):
                        continue
                    task_name = text_div.get_text()
                    if task_name in have_clicked_physical:
                        continue
                    need_click_index = index
                    need_click_view = view
                    break
            if need_click_view:
                print(f"点击体力任务按钮: {task_name}")
                if task_name not in have_clicked_physical:
                    have_clicked_physical.append(task_name)
                    finish_count += 1
                d.click(
                    random.randint(
                        need_click_view.bounds()[0] + 10,
                        need_click_view.bounds()[2] - 10,
                    ),
                    random.randint(
                        need_click_view.bounds()[1] + 10,
                        need_click_view.bounds()[3] - 10,
                    ),
                )
                time.sleep(4)
                search_view = d(className="android.view.View", text="搜索有福利")
                if search_view.exists:
                    d(className="android.widget.EditText", instance=0).send_keys(
                        "笔记本电脑"
                    )
                    d(className="android.widget.Button", text="搜索").click()
                    in_search = True
                    time.sleep(4)
                operate_task()
            else:
                print("✓ 没有更多可执行的体力任务")
                break
        else:
            print("✓ 没有更多体力任务")
            break
        time.sleep(4)
    except Exception as e:
        print("出现异常，继续下一轮", str(e))

print(f"\n共自动化完成 {finish_count} 个任务")

# 第三阶段：跳一跳
print("\n" + "=" * 60)
print("第三阶段：开始跳一跳")
print("=" * 60)

temp_btn = d(className="android.widget.TextView", text="做任务赚体力")
if temp_btn.exists:
    print("点击缩回弹框")
    temp_btn.right(className="android.widget.Button").click()
time.sleep(4)
while True:
    print("开始跳一跳。。。")
    share_view = d(
        className="android.view.View",
        textMatches=r"分享给好友立得体力|去抢频道额外优惠",
    )
    if share_view.exists:
        print("存在分享给好友立得体力弹框，关闭它")
        close_btn = d.xpath(
            '//android.view.View[@text="分享给好友立得体力" or @text="去抢频道额外优惠"]/preceding-sibling::android.view.View[3]'
        )
        if close_btn.exists:
            print("关闭按钮存在，关闭它")
            close_btn.click()
            time.sleep(3)
    dump_btn = d(className="android.widget.Button", textContains="跳一跳拿钱")
    if dump_btn.exists:
        dump_text = dump_btn.get_text()
        match = re.search(r"剩余 (\d+) 体力", dump_text)
        if match:
            phy_num = int(match.group(1))
            if phy_num <= 10:
                break
            print(f"当前剩余体力：{phy_num}")
            # d.shell(f"input touchscreen swipe {dump_btn.center()[0]} {dump_btn.center()[1]} {dump_btn.center()[0]} {dump_btn.center()[1]} 5000")
            dump_btn.long_click(duration=5)
            time.sleep(7)
        else:
            break
    else:
        break

d.watcher.remove()
d.shell("settings put system accelerometer_rotation 0")
print("关闭手机自动旋转")
time2 = time.time()
minutes, seconds = divmod(int(time2 - time1), 60)  # 同时计算分钟和秒
print(f"共耗时: {minutes} 分钟 {seconds} 秒")

print("\n" + "=" * 60)
print("✓ 所有任务已完成！")
print("=" * 60)
print("\n按任意键退出程序...")
try:
    input()
except (EOFError, KeyboardInterrupt):
    pass
