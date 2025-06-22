# 游戏进程名规则集（适用于 mihomo）

## 安卓游戏

```yaml
  android-game:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/moranjianghe/game-process-rules/main/android.yaml
    path: ./rule_providers/android-game.yaml
    interval: 86400
```

## Windows 游戏

```yaml
  windows-game:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/moranjianghe/game-process-rules/main/windows.yaml
    path: ./rule_providers/windows-game.yaml
    interval: 86400
```

自用规则，随缘更新。

性能可能不太好，谨慎使用。

欢迎增加新的条目。
