#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理模块
使用 Hydra 加载和管理配置
"""

from pathlib import Path
from omegaconf import DictConfig, OmegaConf


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "conf/config.yaml"):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        # 获取项目根目录（utils的上一级目录）
        project_root = Path(__file__).parent.parent
        full_path = project_root / config_path
        
        if not full_path.exists():
            print(f"⚠ 配置文件不存在: {full_path}")
            print("  使用默认配置")
            self.cfg = self._get_default_config()
        else:
            print(f"✓ 加载配置文件: {full_path}")
            self.cfg = OmegaConf.load(full_path)
    
    def _get_default_config(self) -> DictConfig:
        """获取默认配置"""
        default_config = {
            "app": {
                "package_name": "com.taobao.taobao",
                "launch_wait_time": 5
            },
            "task": {
                "coin": {
                    "target_count": 40,
                    "enabled": True
                },
                "physical": {
                    "target_count": 50,
                    "enabled": True
                },
                "jump": {
                    "enabled": True,
                    "min_physical": 10
                }
            },
            "operation": {
                "browse_duration": 18,
                "swipe": {
                    "min_duration": 0.2,
                    "max_duration": 1.0
                },
                "wait_between_tasks": 4,
                "search_keyword": "笔记本电脑"
            },
            "retry": {
                "max_back_times": 10,
                "min_back_times_search": 2,
                "min_back_times_normal": 1,
                "max_no_task_count": 3,
                "navigation_max_attempts": 5
            },
            "debug": {
                "print_buttons": True,
                "verbose": True
            }
        }
        return OmegaConf.create(default_config)
    
    def get(self, key: str, default=None):
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分隔的路径，如 "task.coin.target_count"
            default: 默认值
            
        Returns:
            配置值
        """
        try:
            return OmegaConf.select(self.cfg, key, default=default)
        except Exception as e:
            print(f"⚠ 获取配置失败: {key}, 错误: {e}")
            return default
    
    def __getattr__(self, name):
        """支持属性访问"""
        if name in ["cfg", "get", "_get_default_config"]:
            return object.__getattribute__(self, name)
        return getattr(self.cfg, name)
    
    def print_config(self):
        """打印当前配置"""
        print("\n" + "=" * 60)
        print("当前配置:")
        print("=" * 60)
        print(OmegaConf.to_yaml(self.cfg))
        print("=" * 60 + "\n")


# 全局配置实例
_config_instance = None


def get_config(config_path: str = "conf/config.yaml") -> Config:
    """
    获取全局配置实例（单例模式）
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Config实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


# 便捷函数
def get_value(key: str, default=None):
    """
    获取配置值的便捷函数
    
    Args:
        key: 配置键
        default: 默认值
        
    Returns:
        配置值
    """
    config = get_config()
    return config.get(key, default)


if __name__ == "__main__":
    # 测试代码
    config = get_config()
    config.print_config()
    
    # 测试获取配置
    print("测试获取配置:")
    print(f"  金币任务目标: {config.get('task.coin.target_count')}")
    print(f"  体力任务目标: {config.get('task.physical.target_count')}")
    print(f"  浏览时长: {config.get('operation.browse_duration')}")
    print(f"  最大后退次数: {config.get('retry.max_back_times')}")
