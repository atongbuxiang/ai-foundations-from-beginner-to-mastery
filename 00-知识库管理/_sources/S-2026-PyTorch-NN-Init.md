---
type: source
status: active
area: [sources, software, pytorch, initialization]
source_type: official-documentation
title: "torch.nn.init"
author: [PyTorch]
year: 2026
url: "https://docs.pytorch.org/docs/stable/nn.init"
accessed: 2026-08-23
source_tier: B
venue: "PyTorch official documentation"
related: ["[[Xavier、Glorot 初始化]]", "[[Kaiming、He 初始化]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]"]
created: 2026-08-23
updated: 2026-08-23
---
# PyTorch 2026：torch.nn.init

> [!abstract] 来源定位
> 官方文档定义当前 Xavier/Kaiming uniform/normal、gain、fan-in/fan-out 与矩阵布局约定，并明确说明 fan-in 偏向前向尺度、fan-out 偏向反向尺度。本库用它承担 API 与 shape 语义；初始化为何成立仍由概率推导和原论文承担。
