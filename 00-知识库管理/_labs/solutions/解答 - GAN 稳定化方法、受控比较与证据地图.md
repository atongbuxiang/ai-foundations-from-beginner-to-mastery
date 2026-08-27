---
type: solution
status: draft
topic: "[[GAN 稳定化方法、受控比较与证据地图]]"
exercise: "[[习题 - GAN 稳定化方法、受控比较与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - GAN 稳定化方法、受控比较与证据地图
## A. 识别与复述
### GEN24-A01
objective改payoff；regularization改函数类/场；optimizer改离散动力学；schedule改时间尺度/部署参数；architecture改容量/conditioning；data/eval改estimand/estimator。
### GEN24-A02
$L_D=E_r[1-f]_++E_g[1+f]_+$，$L_G=-E_gf$。
### GEN24-A03
无NaN、gradient/update有界、mode count/recall阈值、多seed failure rate、超参数扰动鲁棒、固定预算性能与无测试选点。
## B. 手算与建模
### GEN24-B01
real penalties $0,.5$；fake $0,1$；按四样本各自均值约定，$E_r=.25,E_f=.5$，总 $.75$。
### GEN24-B02
A为100k，B为500k critic updates；不是同 compute。
### GEN24-B03
均值 $72/5=14.4$，中位数11，failure rate $1/5=20\%$。
## C. 推导与证明
### GEN24-C01
real项对 $f$ 在 $f<1$ 导数 $-1$、$f>1$ 为0；fake在 $f>-1$ 为1、$f<-1$ 为0；margin处取次梯度。
### GEN24-C02
二因子例用四组合；主效应为跨另一因子平均的差，interaction为差中之差。多因子同理且需重复seed。
### GEN24-C03
观察只有联合 treatment与control的总差，存在无穷多组件效应分解产生同一总差；无额外组合/假设单组件不可识别。
## D. 边界、反例与纠错
### GEN24-D01
梯度饱和、limit cycle平均或过强正则都可令loss平滑而模型不学/不覆盖。
### GEN24-D02
FID依feature与两矩，非 $W_1$ estimator；改善可来自architecture、regularization或metric gaming。
### GEN24-D03
10 seeds中2个成功FID10、8个collapse；只报最佳10掩盖80% failure。应预注册selection并报全分布。
## E. AI 迁移
### GEN24-E01
匹配G/D架构、参数、data、batch、total updates/wallclock；分别调R1/GP公平强度，统一EMA/selection，报precision/recall/FID与failure多seed。
### GEN24-E02
固定实现commit、encoder weights、resize/color range、real statistics、sample count；重复/bootstrap CI，报告clean/legacy差异与泄漏。
### GEN24-E03
同payoff换regularizer、同regularizer换payoff；测restricted critic与独立OT proxy相关、gradient conditioning与coverage。若Wasserstein payoff无独立增益，可证伪“唯一由距离”主张，但不能证明永远无关。

