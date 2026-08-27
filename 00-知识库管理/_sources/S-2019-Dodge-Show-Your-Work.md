---
type: source
status: verified
area: [sources, experimentation, reproducibility, compute-budget]
source_type: paper
title: "Show Your Work: Improved Reporting of Experimental Results"
author: "Dodge et al."
year: 2019
url: "https://aclanthology.org/D19-1224/"
accessed: 2026-08-26
source_tier: A
scope_role: experimental-reporting
related: ["[[训练控制器的联合实验、消融与证据地图]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Dodge 等：把调参预算写入实验结论

> [!abstract] 来源定位
> 论文指出单个 test score 不能支持公平模型比较，主张报告随超参数搜索/训练预算变化的最佳验证表现和计算成本。课程采用其预算意识，同时保留后续工作对具体估计器偏差的批评。

## 课程采用

- 把训练 compute、trial 数、失败运行、selection rule 和最终 test evaluation 分开；
- 对 control bundle 的比较同时匹配 optimizer、schedule、warmup、decay、clipping、averaging 与调参预算；
- 不用一次最好 seed 或最好 checkpoint 代替分布；
- 预先声明主效应、交互效应和停止规则。
