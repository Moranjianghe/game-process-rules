#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows游戏进程名收集器
用于收集和整理常见Windows游戏的进程名
"""

import json
import logging
from typing import Dict, List

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WindowsGameCollector:
    def __init__(self):
        self.games = {}
    
    def get_windows_games(self) -> Dict[str, str]:
        """返回Windows热门游戏进程名列表"""
        return {
            # MOBA类游戏
            "League of Legends.exe": "英雄联盟",
            "LeagueClient.exe": "英雄联盟客户端",
            "LeagueClientUx.exe": "英雄联盟客户端UX",
            "Dota 2.exe": "Dota 2",
            "dota2.exe": "Dota 2",
            
            # 射击类游戏
            "valorant.exe": "无畏契约",
            "VALORANT-Win64-Shipping.exe": "无畏契约",
            "csgo.exe": "CS:GO",
            "cs2.exe": "Counter-Strike 2",
            "TslGame.exe": "绝地求生",
            "FortniteClient-Win64-Shipping.exe": "堡垒之夜",
            "Overwatch.exe": "守望先锋",
            "OverwatchLauncher.exe": "守望先锋启动器",
            "Apex Legends.exe": "Apex英雄",
            "r5apex.exe": "Apex英雄",
            "RainbowSix.exe": "彩虹六号：围攻",
            "RainbowSixGame.exe": "彩虹六号：围攻",
            
            # RPG类游戏
            "YuanShen.exe": "原神",
            "GenshinImpact.exe": "原神",
            "StarRail.exe": "崩坏：星穹铁道",
            "Honkai Impact 3rd.exe": "崩坏3",
            "BH3.exe": "崩坏3",
            "WutheringWaves.exe": "鸣潮",
            "TheFinalShape.exe": "命运2",
            "destiny2.exe": "命运2",
            "Diablo III64.exe": "暗黑破坏神3",
            "Diablo IV.exe": "暗黑破坏神4",
            "PathOfExile.exe": "流放之路",
            "PathOfExile_x64.exe": "流放之路",
            
            # 沙盒建造类游戏
            "Minecraft.exe": "我的世界",
            "MinecraftLauncher.exe": "我的世界启动器",
            "javaw.exe": "我的世界Java版",
            "Terraria.exe": "泰拉瑞亚",
            "valheim.exe": "英灵神殿",
            "7DaysToDie.exe": "七日杀",
            
            # 竞速类游戏
            "ForzaHorizon5.exe": "极限竞速：地平线5",
            "ForzaHorizon4.exe": "极限竞速：地平线4",
            "NeedForSpeed.exe": "极品飞车",
            "NFSHEAT.exe": "极品飞车：热度",
            "dirt5.exe": "尘埃5",
            "F1_22.exe": "F1 22",
            
            # 策略类游戏
            "AoE2DE_s.exe": "帝国时代2决定版",
            "AoE4.exe": "帝国时代4",
            "Civ6.exe": "文明6",
            "CivilizationVI.exe": "文明6",
            "TotalWarWarhammer3.exe": "全面战争：战锤3",
            "starcraft2.exe": "星际争霸2",
            "SC2.exe": "星际争霸2",
            
            # 休闲益智类游戏
            "Among Us.exe": "Among Us",
            "FallGuys_client.exe": "糖豆人",
            "RocketLeague.exe": "火箭联盟",
            "Cuphead.exe": "茶杯头",
            "Hades.exe": "哈迪斯",
            
            # 模拟类游戏
            "Cities.exe": "城市天际线",
            "TheSims4.exe": "模拟人生4",
            "TS4.exe": "模拟人生4",
            "EuroTruckSimulator2.exe": "欧洲卡车模拟2",
            "ets2.exe": "欧洲卡车模拟2",
            "AmericanTruckSimulator.exe": "美国卡车模拟",
            "ats.exe": "美国卡车模拟",
            
            # 动作冒险类游戏
            "GTA5.exe": "侠盗猎车手5",
            "GTAVLauncher.exe": "侠盗猎车手5启动器",
            "RDR2.exe": "荒野大镖客：救赎2",
            "Cyberpunk2077.exe": "赛博朋克2077",
            "ac_odyssey.exe": "刺客信条：奥德赛",
            "ACValhalla.exe": "刺客信条：英灵殿",
            "witcher3.exe": "巫师3：狂猎",
            "EldenRing.exe": "艾尔登法环",
            "sekiro.exe": "只狼：影逝二度",
            "DarkSoulsIII.exe": "黑暗之魂3",
            
            # 体育类游戏
            "FIFA23.exe": "FIFA 23",
            "eafc24.exe": "EA Sports FC 24",
            "PES2021.exe": "实况足球2021",
            "NBA2K23.exe": "NBA 2K23",
            "NBA2K24.exe": "NBA 2K24",
            
            # 卡牌类游戏
            "Hearthstone.exe": "炉石传说",
            "Gwent.exe": "昆特牌",
            "MTGA.exe": "万智牌竞技场",
            
            # 音乐类游戏
            "osu!.exe": "osu!",
            "Beat Saber.exe": "节拍军刀",
            "Rocksmith2014.exe": "摇滚史密斯2014",
            
            # 平台启动器
            "Steam.exe": "Steam平台",
            "steamwebhelper.exe": "Steam网页助手",
            "EpicGamesLauncher.exe": "Epic Games启动器",
            "UnrealEngineLauncher.exe": "虚幻引擎启动器",
            "Origin.exe": "Origin平台",
            "EADesktop.exe": "EA桌面版",
            "Battle.net.exe": "暴雪战网",
            "Blizzard Battle.net.exe": "暴雪战网",
            "UbisoftConnect.exe": "育碧连接",
            "upc.exe": "育碧连接",
            "WeGameTGP.exe": "WeGame腾讯游戏平台",
            "launcher.exe": "通用启动器",
            
            # 游戏录制/直播工具
            "obs64.exe": "OBS Studio",
            "obs32.exe": "OBS Studio 32位",
            "XSplit.Core.exe": "XSplit",
            "streamlabs obs.exe": "Streamlabs OBS",
            "GameBarFTServer.exe": "Xbox Game Bar",
            "ShadowPlay.exe": "NVIDIA ShadowPlay",
            
            # 游戏优化工具
            "MSIAfterburner.exe": "微星Afterburner",
            "RTSS.exe": "RivaTuner Statistics Server",
            "GeForceExperience.exe": "NVIDIA GeForce Experience",
            "RadeonSoftware.exe": "AMD Radeon Software"
        }
    
    def generate_yaml_rules(self, games: Dict[str, str]) -> str:
        """生成YAML格式的Windows游戏规则"""
        rules = ["payload:"]
        
        # 按游戏名称排序
        sorted_games = sorted(games.items(), key=lambda x: x[1])
        
        for process_name, game_name in sorted_games:
            rules.append(f"- PROCESS-NAME,{process_name} #{game_name}")
        
        return "\n".join(rules)
    
    def save_to_json(self, games: Dict[str, str], filename: str):
        """保存游戏列表到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存到 {filename}")


def main():
    collector = WindowsGameCollector()
    
    # 获取Windows游戏列表
    windows_games = collector.get_windows_games()
    
    # 保存到JSON文件
    collector.save_to_json(windows_games, 'f:/code/game-process-rules/spider/windows_games_database.json')
    
    # 生成YAML规则
    yaml_rules = collector.generate_yaml_rules(windows_games)
    
    # 保存YAML规则
    with open('f:/code/game-process-rules/spider/windows_rules_generated.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_rules)
    
    print(f"✅ 成功收集了 {len(windows_games)} 个Windows游戏进程名")
    print("📁 文件已保存:")
    print("   - f:/code/game-process-rules/spider/windows_games_database.json")
    print("   - f:/code/game-process-rules/spider/windows_rules_generated.yaml")
    
    return windows_games


if __name__ == "__main__":
    main()
