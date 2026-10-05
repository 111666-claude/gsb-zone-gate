# zone-gate

副本门槛：等级、前置成就、冷却与每日次数，用生成器逐个产出可进入的副本，报告按文本渲染，
只用 Python 标准库。

```
python3 main.py --sample=level
python3 main.py --sample=prereq
python3 main.py --sample=cooldown
python3 main.py --sample=quota
python3 main.py --sample=report
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **等级**：角色等级不小于副本需求才算过，正好等于算过。
- **前置成就**：副本的 `requires` 必须全部在 `earned` 里。
- **冷却**：距上次进入同一个副本不足 `cooldown_ms` 不放行，正好等于冷却算可以进。
- **每日次数**：同一服务日进入同一个副本的次数不超过 `daily_limit`，超出不放行。
- **惰性**：`iter_allowed` 是生成器，调用时不判定，迭代时才逐个判定。
- **代价**：单个副本判定摊还 O(1)，内存 O(副本数)；每秒 10 万次判定。

## 输出契约（不改格式）

```
cave=..
vault=..
arena=..
name  open/locked      （--sample=report 的对齐文本）
```

## 目录

```
zonegate/gate.py    等级、前置、冷却与每日次数
main.py             样例入口与文本报告
tests/test_gate.py  unittest 用例
```
