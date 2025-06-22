#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏包名爬虫
用于从各种来源收集热门Android游戏的包名信息
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup
from typing import Dict, List, Set
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GamePackageSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.games = {}
        
    def extract_package_from_url(self, url: str) -> str:
        """从Google Play URL中提取包名"""
        match = re.search(r'id=([^&\s]+)', url)
        return match.group(1) if match else None
    
    def get_known_games(self) -> Dict[str, str]:
        """返回已知的热门游戏包名列表"""
        return {
            # 从网页抓取获得的热门游戏
            "com.supercell.clashroyale": "部落冲突:皇室战争",
            "com.roblox.client": "Roblox",
            "com.kiloo.subwaysurf": "Subway Surfers 地铁跑酷", 
            "com.youmusic.magictiles": "Magic Tiles 3 - 钢琴游戏",
            "com.scopely.monopolygo": "MONOPOLY GO!",
            "com.dreamgames.royalmatch": "Royal Match",
            "com.nianticlabs.pokemongo": "Pokemon GO",
            "com.dts.freefireth": "Free Fire: 8周年",
            "com.activision.callofduty.shooter": "Call of Duty: Mobile",
            "com.miniclip.eightballpool": "8 Ball Pool",
            "com.robtopx.geometryjumplite": "Geometry Dash Lite",
            "com.king.candycrushsaga": "Candy Crush Saga",
            "com.outfit7.mytalkingtom2": "我的汤姆猫2",
            "jp.pokemon.pokemontcgp": "Pokemon TCG Pocket",
            "com.gof.global": "寒霜启示录",
            "com.tencent.ig": "PUBG MOBILE",
            "com.funtomic.matchmasters": "Match Masters",
            "com.playrix.township": "梦想小镇",
            "com.mojang.minecraftpe": "Minecraft",
            "com.fun.lastwar.gp": "Last War:Survival Game",
            "com.dreamgames.royalkingdom": "Royal Kingdom",
            "com.block.juggle": "Block Blast!",
            "com.bunbunstudio.magicblocktiles": "Music Piano 7",
            "io.supercent.linkedcubic": "蛇冲突 Snake Clash",
            "io.voodoo.holeio": "Hole.io",
            "com.vitastudio.mahjong": "Vita 麻将",
            "com.run.tower.defense": "Kingshot",
            "com.GybeGames.ColorBlockJam": "Color Block Jam",
            "com.innersloth.spacemafia": "Among Us",
            "com.yolo.hiddenobjects": "Find Hidden Objects - Spot It!",
            "com.supercell.clashofclans": "部落冲突 Clash of Clans",
            "com.dts.freefiremax": "Free Fire MAX",
            "com.igg.android.lordsmobile": "王国纪元",
            "com.vizorapps.klondike": "Klondike Adventures",
            "com.bandainamcoent.dblegends_ww": "DRAGON BALL LEGENDS 七龙珠 激战传说",
            "com.devsisters.ck": "薜饼人王国",
            "com.rovio.baba": "Angry Birds 2",
            "com.topgamesinc.evony": "Evony: The King's Return",
            "com.os.airforce": "1945空军",
            "com.playrix.gardenscapes": "梦幻花园 Gardenscapes",
            "com.fgol.HungrySharkEvolution": "Hungry Shark Evolution",
            "com.playrix.homescapes": "梦幻家园 Homescapes",
            "com.gameloft.android.ANMP.GloftA9HM": "狂野飙车:传奇大集结",
            "com.lilithgame.roc.gp": "万国觉醒 RoK",
            "com.tap4fun.ape.gplay": "Age of Apes: 猿族时代",
            "com.lockwoodpublishing.avakinlife": "Avakin Life - 3D 虚拟世界",
            "com.wildspike.wormszone": "Worms Zone .io - Hungry Snake",
            "eu.nordeus.topeleven.android": "Top Eleven 2025",
            "com.miHoYo.GenshinImpact": "原神",
            "com.supercell.brawlstars": "Brawl Stars",
            "com.ea.gp.fifamobile": "EA SPORTS FC Mobile 足球",
            "com.matteljv.uno": "UNO!",
            "com.movile.playkids.pkxd": "PK XD: Fun, friends & games",
            "com.king.candycrushsodasaga": "Candy Crush Soda Saga",
            "com.easybrain.art.puzzle": "Art Puzzle - 艺术拼图游戏",
            "com.zynga.words3": "Words With Friends Word Game",
            "com.outfit7.mytalkinghank": "我的汉克狗:群岛",
            "com.gramgames.mergedragons": "萌龙进化论 Merge Dragons!",
            "com.tocaboca.tocalifeworld": "Toca Boca World",
            
            # 其他热门游戏
            "com.netease.onmyojigp": "阴阳师",
            "com.tencent.tmgp.sgame": "王者荣耀",
            "com.netease.hyxd.bilibili": "崩坏学园2",
            "com.hypergryph.arknights": "明日方舟",
            "com.mihoyo.enterprise.NGHSoD": "崩坏:星穹铁道",
            "com.lilithgame.hgame.gp": "剑与远征",
            "com.garena.game.kgtw": "传说对决",
            "com.igg.android.doomsdaylastsurvivors": "黎明再现 Doomsday: Last Survivors",
            "jp.konami.pesam": "eFootball",
            "com.imangi.templerun2": "Temple Run 2",
            "com.gameinsight.goc": "Gods of Olympus",
            "com.kiloo.subwaysurf": "地铁跑酷",
            "com.outfit7.talkingtom2": "会说话的汤姆猫2",
            "com.glu.deer": "Deer Hunter Classic",
            "com.halfbrick.fruitninja": "水果忍者",
            "com.ea.games.pvz2_row": "植物大战僵尸2",
            "com.netease.mrzh": "第五人格",
            "com.tencent.tmgp.speedmobile": "QQ飞车",
            "com.tencent.lolm": "英雄联盟手游",
            "com.playdemic.golf.android": "Golf Clash",
            "com.ninekyu.panzer.android": "装甲前线",
            "com.netease.dwrg": "决战!平安京",
            "com.mobile.legends": "Mobile Legends: Bang Bang",
            "com.garena.game.codm": "Call of Duty: Mobile",
            "com.epicgames.fortnite": "Fortnite",
            "com.riotgames.league.wildrift": "League of Legends: Wild Rift",
            "com.blizzard.wtcg.hearthstone": "炉石传说",
            "com.netease.g78na.gb": "荒野行动",
            "com.supercell.hayday": "卡通农场",
            "com.outfit7.mytalkingtom": "我的汤姆猫",
            "com.gameloft.android.ANMP.GloftA8HM": "狂野飙车8",
            "com.sgn.cookiejam.gp": "Cookie Jam",
            "com.king.farmheroessaga": "Farm Heroes Saga"
        }
    
    def scrape_apkpure_top_games(self) -> Dict[str, str]:
        """从APKPure获取热门游戏"""
        games = {}
        try:
            url = "https://apkpure.com/cn/game"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                game_links = soup.find_all('a', href=re.compile(r'/[^/]+/[^/]+'))
                
                for link in game_links[:50]:  # 限制数量
                    href = link.get('href', '')
                    if '/com.' in href:
                        # 从APKPure URL提取包名
                        parts = href.split('/')
                        if len(parts) >= 3:
                            package_name = parts[2]
                            game_name = link.get_text(strip=True)
                            if package_name.startswith('com.'):
                                games[package_name] = game_name
                                
        except Exception as e:
            logger.error(f"获取APKPure数据失败: {e}")
            
        return games
    
    def scrape_google_play_charts(self) -> Dict[str, str]:
        """从各种来源收集Google Play热门游戏"""
        games = {}
        
        # 一些热门游戏的包名（手动收集）
        popular_games = {
            "com.facebook.games.tm20": "Messenger",
            "com.zeptolab.ctr.ads": "Cut the Rope 3",
            "com.ubisoft.hungrysharkworld": "Hungry Shark World",
            "com.ea.gp.simpsonstappedout": "The Simpsons: Tapped Out",
            "com.netmarble.mherosgb": "MARVEL Future Fight",
            "com.wb.goog.mkx": "Mortal Kombat X",
            "com.disney.disneymagickingdoms_goo": "Disney Magic Kingdoms",
            "com.gameloft.android.ANMP.GloftDMHM": "Disney Dreamlight Valley",
            "com.zynga.farmville3": "FarmVille 3",
            "com.miniclip.agar.io": "Agar.io",
            "com.socialpoint.dragonland": "Dragon Land",
            "com.miniclip.solitaire": "Solitaire",
            "com.ea.gp.nfs.na": "Need for Speed: No Limits",
            "com.nekki.shadowfight": "Shadow Fight 2",
            "com.ubisoft.jddanceparty": "Just Dance Now",
            "com.nekki.vector": "Vector",
            "com.miniclip.darts": "8 Ball Pool - Miniclip",
            "com.outfit7.talkingginger2": "Talking Ginger 2",
            "com.outfit7.talkingben": "Talking Ben the Dog"
        }
        
        games.update(popular_games)
        return games
    
    def collect_all_games(self) -> Dict[str, str]:
        """收集所有游戏包名"""
        logger.info("开始收集游戏包名...")
        
        all_games = {}
        
        # 添加已知游戏
        known_games = self.get_known_games()
        all_games.update(known_games)
        logger.info(f"添加了 {len(known_games)} 个已知游戏")
        
        # 尝试从APKPure获取
        try:
            apkpure_games = self.scrape_apkpure_top_games()
            all_games.update(apkpure_games)
            logger.info(f"从APKPure获取了 {len(apkpure_games)} 个游戏")
        except Exception as e:
            logger.warning(f"APKPure爬取失败: {e}")
        
        # 添加更多热门游戏
        more_games = self.scrape_google_play_charts()
        all_games.update(more_games)
        logger.info(f"添加了 {len(more_games)} 个额外游戏")
        
        logger.info(f"总共收集到 {len(all_games)} 个游戏包名")
        return all_games
    
    def save_to_json(self, games: Dict[str, str], filename: str):
        """保存游戏列表到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存到 {filename}")
    
    def generate_yaml_rules(self, games: Dict[str, str]) -> str:
        """生成YAML格式的规则"""
        rules = ["payload:"]
        
        # 按游戏名称排序
        sorted_games = sorted(games.items(), key=lambda x: x[1])
        
        for package_name, game_name in sorted_games:
            rules.append(f"- PROCESS-NAME,{package_name} #{game_name}")
        
        return "\n".join(rules)


def main():
    spider = GamePackageSpider()
    
    # 收集所有游戏
    all_games = spider.collect_all_games()
    
    # 保存到JSON文件
    spider.save_to_json(all_games, 'f:/code/game-process-rules/spider/games_database.json')
    
    # 生成YAML规则
    yaml_rules = spider.generate_yaml_rules(all_games)
    
    # 保存YAML规则
    with open('f:/code/game-process-rules/spider/android_rules_generated.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_rules)
    
    print(f"✅ 成功收集了 {len(all_games)} 个游戏包名")
    print("📁 文件已保存:")
    print("   - f:/code/game-process-rules/spider/games_database.json")
    print("   - f:/code/game-process-rules/spider/android_rules_generated.yaml")
    
    return all_games


if __name__ == "__main__":
    main()
