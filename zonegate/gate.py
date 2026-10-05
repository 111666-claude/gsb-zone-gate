"""副本门槛：等级、前置成就、冷却与每日次数，用生成器逐个产出。"""


class Gates:
    """副本门槛台账。"""

    def __init__(self, zones):
        self.zones = zones
        self.last = {}
        self.counts = {}

    def allowed(self, player, name, level, earned, day, at_ms):
        """判定一个副本能不能进。"""
        zone = self.zones[name]
        if level < zone["level"]:
            return False
        if not all(req in earned for req in zone["requires"]):
            return False
        last = self.last.get((player, name))
        if last is not None and at_ms - last < zone["cooldown_ms"]:
            return False
        if self.counts.get((player, day, name), 0) >= zone["daily_limit"]:
            return False
        return True

    def enter(self, player, name, day, at_ms):
        """记录一次进入，返回是否放行。"""
        self.last[(player, name)] = at_ms
        key = (player, day, name)
        self.counts[key] = self.counts.get(key, 0) + 1
        return True

    def iter_allowed(self, player, level, earned, day, at_ms):
        """惰性产出允许进入的副本名。"""
        for name in sorted(self.zones):
            if self.allowed(player, name, level, earned, day, at_ms):
                yield name
