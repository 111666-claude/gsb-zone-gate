"""副本门槛入口：跑样例并渲染一张文本报告。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zonegate.gate import Gates  # noqa: E402

ZONES = {
    "cave": {"level": 10, "requires": [], "cooldown_ms": 1000, "daily_limit": 2},
    "vault": {"level": 1, "requires": ["ach-key"], "cooldown_ms": 0, "daily_limit": 5},
    "arena": {"level": 1, "requires": [], "cooldown_ms": 1000, "daily_limit": 1},
}


def report(rows):
    width = max(len(name) for name, _ in rows)
    return "\n".join("%s  %s" % (name.ljust(width), state) for name, state in rows)


def main(argv=None):
    args = (argv or sys.argv[1:])[:1]
    sample = args[0] if args else "--sample=level"
    gates = Gates(ZONES)
    if sample == "--sample=level":
        allowed = list(gates.iter_allowed("p1", 10, [], 1, 0))
        print("cave=%s" % ("yes" if "cave" in allowed else "no"))
    elif sample == "--sample=prereq":
        allowed = list(gates.iter_allowed("p1", 9, [], 1, 0))
        print("vault=%s" % ("yes" if "vault" in allowed else "no"))
    elif sample == "--sample=cooldown":
        gates.enter("p1", "arena", 1, 0)
        allowed = list(gates.iter_allowed("p1", 9, [], 1, 500))
        print("arena=%s" % ("yes" if "arena" in allowed else "no"))
    elif sample == "--sample=quota":
        gates.enter("p1", "arena", 1, 0)
        allowed = list(gates.iter_allowed("p1", 9, [], 1, 5000))
        print("arena=%s" % ("yes" if "arena" in allowed else "no"))
    elif sample == "--sample=report":
        rows = []
        for name in sorted(ZONES):
            allowed = list(gates.iter_allowed("p1", 10, [], 1, 0))
            rows.append((name, "open" if name in allowed else "locked"))
        print(report(rows))
    else:
        raise SystemExit("需要 --sample=level|prereq|cooldown|quota|report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
