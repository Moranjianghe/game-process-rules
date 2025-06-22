
# -*- coding: utf-8 -*-
"""
游戏规则统计脚本
生成项目的统计信息
"""

import json
import yaml
import os
from typing import Dict, List

def read_yaml_rules(file_path: str) -> List[str]:
    """读取YAML文件中的规则"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('payload', [])
    except Exception as e:
        print(f"读取 {file_path} 失败: {e}")
        return []

def count_rules(rules: List[str]) -> int:
    """统计规则数量（排除注释行）"""
    count = 0
    for rule in rules:
        if isinstance(rule, str) and rule.strip().startswith('- PROCESS-NAME,'):
            count += 1
    return count

def extract_game_categories(rules: List[str]) -> Dict[str, int]:
    """从规则中提取游戏分类统计"""
    categories = {}
    current_category = "其他"
    
    for rule in rules:
        if isinstance(rule, str):
            rule = rule.strip()
            if rule.startswith('#') and '类游戏' in rule:
                current_category = rule.replace('#', '').strip()
                if current_category not in categories:
                    categories[current_category] = 0
            elif rule.startswith('- PROCESS-NAME,'):
                categories[current_category] = categories.get(current_category, 0) + 1
    
    return categories

def generate_stats():
    """生成统计信息"""
    print("🎮 游戏进程规则集统计信息")
    print("=" * 50)
    
    # Android游戏统计
    android_rules = read_yaml_rules('f:/code/game-process-rules/android.yaml')
    android_count = count_rules(android_rules)
    android_categories = extract_game_categories(android_rules)
    
    print(f"\n📱 Android游戏规则:")
    print(f"   总数量: {android_count} 个游戏")
    if android_categories:
        print("   分类统计:")
        for category, count in android_categories.items():
            if count > 0:
                print(f"   - {category}: {count} 个")
    
    # Windows游戏统计
    windows_rules = read_yaml_rules('f:/code/game-process-rules/windows.yaml')
    windows_count = count_rules(windows_rules)
    windows_categories = extract_game_categories(windows_rules)
    
    print(f"\n🖥️ Windows游戏规则:")
    print(f"   总数量: {windows_count} 个游戏")
    if windows_categories:
        print("   分类统计:")
        for category, count in windows_categories.items():
            if count > 0:
                print(f"   - {category}: {count} 个")
    
    # 总计
    total_count = android_count + windows_count
    print(f"\n📊 总计: {total_count} 个游戏规则")
    
    # 检查数据库文件
    database_files = [
        'f:/code/game-process-rules/spider/games_database.json',
        'f:/code/game-process-rules/spider/windows_games_database.json'
    ]
    
    print(f"\n📁 数据库文件:")
    for db_file in database_files:
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"   - {os.path.basename(db_file)}: {len(data)} 个条目")
            except Exception as e:
                print(f"   - {os.path.basename(db_file)}: 读取失败 ({e})")
        else:
            print(f"   - {os.path.basename(db_file)}: 文件不存在")
    
    # 生成项目文件统计
    project_files = [
        'android.yaml',
        'windows.yaml', 
        'README.md',
        'spider/game_package_spider.py',
        'spider/windows_game_collector.py'
    ]
    
    print(f"\n📄 项目文件:")
    for file in project_files:
        full_path = f'f:/code/game-process-rules/{file}'
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            size_kb = size / 1024
            print(f"   - {file}: {size_kb:.1f} KB")
        else:
            print(f"   - {file}: 文件不存在")

if __name__ == "__main__":
    generate_stats()
