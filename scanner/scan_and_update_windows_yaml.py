#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描指定目录下的可联网可执行文件，并将其进程名自动加入 windows.yaml 规则文件。
"""
import os
import yaml
import pefile
import socket
import struct
from typing import List, Set

def is_exe_file(filepath: str) -> bool:
    return filepath.lower().endswith('.exe') and os.path.isfile(filepath)

def check_internet_access(filepath: str) -> bool:
    """
    检查exe文件是否有联网行为（简单静态分析：查找常见socket相关API导入）
    """
    try:
        pe = pefile.PE(filepath, fast_load=True)
        pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll = entry.dll.decode(errors='ignore').lower()
                if 'ws2_32' in dll or 'wininet' in dll or 'winhttp' in dll:
                    return True
                for imp in entry.imports:
                    if imp.name:
                        name = imp.name.decode(errors='ignore').lower()
                        if any(api in name for api in ['socket', 'connect', 'send', 'recv', 'inet', 'http', 'url', 'gethost']):
                            return True
        return False
    except Exception:
        return False

def scan_executables_with_internet_access(scan_dir: str) -> Set[str]:
    """
    扫描目录下所有exe文件，返回进程名集合（仅后缀判断）
    """
    result = set()
    for root, _, files in os.walk(scan_dir):
        for file in files:
            if is_exe_file(os.path.join(root, file)):
                result.add(file)
    return result

def load_windows_yaml(yaml_path: str) -> List[str]:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

def save_windows_yaml(yaml_path: str, lines: List[str]):
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def update_windows_yaml_with_new_processes(yaml_path: str, new_processes: Set[str]):
    lines = load_windows_yaml(yaml_path)
    existing = set()
    for line in lines:
        if line.strip().startswith('- PROCESS-NAME,'):
            proc = line.split(',')[1].split('#')[0].strip()
            existing.add(proc)
    to_add = [p for p in new_processes if p not in existing]
    if not to_add:
        print('没有新进程需要添加。')
        return
    # 在文件末尾添加
    with open(yaml_path, 'a', encoding='utf-8') as f:
        for proc in to_add:
            f.write(f'- PROCESS-NAME,{proc} #自动扫描添加\n')
    print(f'已添加 {len(to_add)} 个新进程到 {yaml_path}')

def main():
    # 交互输入路径
    scan_dir = input('请输入要扫描的目录路径: ').strip()
    if not scan_dir:
        print('未输入目录，退出。')
        return
    scan_dir = os.path.abspath(scan_dir)
    yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../windows.yaml'))

    print(f'扫描目录: {scan_dir}')
    print(f'规则文件: {yaml_path}')

    found = scan_executables_with_internet_access(scan_dir)
    if not found:
        print('未发现exe文件。')
        return
    print(f'发现 {len(found)} 个exe:')
    for p in found:
        print('  ', p)
    update_windows_yaml_with_new_processes(yaml_path, found)

if __name__ == '__main__':
    main()
