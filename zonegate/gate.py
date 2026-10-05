"""副本门槛：等级、前置成就、冷却与每日次数，用生成器逐个产出。"""


class Gates:
    """副本门槛台账。"""

    def __init__(self, zones):
        self.zones = zones
        self._names = sorted(zones)
        self._last = {}
        self._counts = {}

    def allowed(self, player, name, level, earned, day, at_ms):
        """判定一个副本能不能进：等级、前置、冷却、每日次数逐项检查。"""
        zone = self.zones[name]
        if level < zone["level"]:
            return False
        if any(req not in earned for req in zone["requires"]):
            return False
        last_ms = self._last.get((player, name))
        if last_ms is not None and at_ms - last_ms < zone["cooldown_ms"]:
            return False
        if self._counts.get((player, day, name), 0) >= zone["daily_limit"]:
            return False
        return True

    def enter(self, player, name, day, at_ms):
        """记录一次进入；冷却未到或当日次数用尽则不放行也不计数。"""
        zone = self.zones[name]
        last_ms = self._last.get((player, name))
        if last_ms is not None and at_ms - last_ms < zone["cooldown_ms"]:
            return False
        key = (player, day, name)
        if self._counts.get(key, 0) >= zone["daily_limit"]:
            return False
        self._last[(player, name)] = at_ms
        self._counts[key] = self._counts.get(key, 0) + 1
        return True

    def iter_allowed(self, player, level, earned, day, at_ms):
        """惰性产出允许进入的副本名。"""
        earned = earned if isinstance(earned, (set, frozenset)) else set(earned)
        for name in self._names:
            if self.allowed(player, name, level, earned, day, at_ms):
                yield name
