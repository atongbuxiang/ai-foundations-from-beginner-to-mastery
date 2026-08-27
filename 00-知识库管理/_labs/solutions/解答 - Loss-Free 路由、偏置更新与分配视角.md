---
type: solution
status: draft
area: [architecture, moe, loss-free, assignment]
topic: "[[Loss-Free 路由、偏置更新与分配视角]]"
exercise: "[[习题 - Loss-Free 路由、偏置更新与分配视角]]"
sources: ["[[S-2024-DeepSeek-V3-MoE]]", "[[S-2025-Su-10757-MoE-Loss-Free]]", "[[S-2026-Su-11619-MoE-Quantile-Balancing]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Loss-Free 路由、偏置更新与分配视角

## A. 识别与复述

### ARCH-LFREE-A01
Loss-free 指不把显式均衡辅助项加进优化 loss。它不排除用负载统计更新 bias/threshold，不排除状态、步长、EMA、同步、capacity 或对离散 selection 的干预，所以不是“无均衡”或“无训练影响”。

### ARCH-LFREE-A02
$s_i+b_i$ 让资源反馈改变 Top-k；选中后用原 $s_i$ 计算 weight，可避免校正 bias 直接改变 mixture amplitude。两者仍通过 index 相连：bias 换掉专家时，输出函数改变。

### ARCH-LFREE-A03
$$\max_A\sum_{t,i}A_{ti}s_{ti},\quad A_{ti}\in\{0,1\},$$
满足行约束 $\sum_iA_{ti}=k$ 与列容量 $\sum_tA_{ti}\le C_i$。不同方案也可把列约束改为等号或允许逐 token 动态行和。

## B. 手算与建模

### ARCH-LFREE-B01
误差 $e=[2,-2]$，符号反馈 $b'=b-.1\operatorname{sign}(e)=[-.1,+.1]$。热门 expert 1 被降权，冷门 expert 2 被升权。

### ARCH-LFREE-B02
不加 bias 时 $.55>.50$，选 expert 1；加 bias 后调整分数为 $[.45,.60]$，选 expert 2。若 mixing 只用原 score，选中专家的组合幅度仍按原规则计算。

### ARCH-LFREE-B03
一种可行解是 token 1、2→expert 1，token 3→expert 2，token 4→expert 3；列负载 $[2,1,1]$ 均不超 2，总分 $9+8+9+9=35$。它恰好也是逐行最大选择；矩阵改变时容量可能迫使放弃逐行最大。

## C. 推导与证明

### ARCH-LFREE-C01
为 $\sum_tA_{ti}\le C_i$ 引入 $\beta_i\ge0$：
$$\mathcal L=\sum_{t,i}A_{ti}s_{ti}-\sum_i\beta_i(\sum_tA_{ti}-C_i)
=\sum_{t,i}A_{ti}(s_{ti}-\beta_i)+\sum_i\beta_iC_i.$$
固定 dual 时，token 按 $s_{ti}-\beta_i$ 选择；稀缺专家的正价格等价于负 selection bias。

### ARCH-LFREE-C02
$k_t=\sum_i\mathbf1[s_{ti}>\beta_i]$。不同 token 的 score 超过各 expert threshold 的个数不同，所以行和不再固定；调整每列 $\beta_i$ 可近似控制专家 quota。

### ARCH-LFREE-C03
$e_i>0$ 时下一步 $b_i$ 下降，局部倾向减少该专家选择；$e_i<0$ 相反。但 $e(b)$ 由离散 Top-k、其他专家、数据分布和延迟共同决定，可能不连续且时变；没有对响应增益/单调性和步长的假设，不能推出收敛。

## D. 边界、反例与纠错

### ARCH-LFREE-D01
若原本 expert 1 被选、加 bias 后 expert 2 被选，即使两者 weight 都为 1，输出从 $f_1(x)$ 变成 $f_2(x)$。只有专家输出恰好相同才不变。

### ARCH-LFREE-D02
两专家、全部 token 总选 adjusted score 较大的一个；大步长一次把热门 expert 的 bias 从 0 降到 −10、冷门升到 +10，下一批会全部翻到另一专家，再反向更新回去，形成周期二振荡。

### ARCH-LFREE-D03
统计延迟使 $b$ 修正过去的拥塞，当前负载可能已反向；数据从语言 A 突变到 B 时，旧 quantile/bias 与新 score 分布不匹配。应测滞后、漂移恢复和更新窗口。

## E. AI 迁移

### ARCH-LFREE-E01
固定 checkpoint family、Router score、capacity、placement、数据和预算；一组扫 $\lambda$，一组扫 $\eta$/更新规则，并含无均衡基线。报告 quality、load/drop、bias/aux 时序、吞吐和漂移响应，多 seed 比较 Pareto。

### ARCH-LFREE-E02
用精确排序 quantile 作 reference，比较 histogram/bin、采样和分布式合并方案；扫分布形状、batch、bins 与漂移。记录 threshold error、quota error、assignment disagreement、通信、时间和最终 quality。

### ARCH-LFREE-E03
监控 bias/threshold 范围与速度、load max/CV、振荡自相关、drop、assignment churn、quality 和 step tail。设置 clipping、减小步长、EMA、回退到最近稳定 bias 或临时 aux loss；触发与恢复条件必须版本化。

