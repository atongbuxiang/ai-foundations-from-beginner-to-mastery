# 资产目录

本目录只保存版权和来源清晰、确实服务于笔记理解的视觉资产。

```text
figures/   自绘架构图、几何图和 SVG
plots/     由 `00-知识库管理/_labs` 实验生成的图
images/    获得许可保存的外部图片，按 source-id 分目录
```

详细要求见[[04-图示与资产规范]]，生产步骤见[[06-图文编排与制图工作流]]。自绘图从[`_templates/svg/`](../_templates/svg/README.md)中的三种教材插图模板开始；外部文件逐项登记在[[外部图像资产登记]]。Mermaid 图直接保存在 Markdown 中，不需要复制到本目录。

当前可复现图包括：

- `plots/effective-rank/`：有效秩比较；
- `plots/perturbation/`：谱间隙与特征向量稳定性；
- `plots/qr/`：Gram–Schmidt 正交性误差；
- `plots/cholesky/`：正定边界、条件数与 Cholesky pivot；
- `plots/matrix-functions/`：稳定非正规系统的矩阵指数有限时间瞬态；
- `plots/polar-decomposition/`：Newton–Schulz 极分解在不同条件数和秩亏边界上的正交性误差；
- `plots/matrix-sign/`：固定点谱下，非正规性对 matrix sign 范数、Fréchet 导数和统一缩放 Newton 步数的影响；
- `plots/stationary-iterations/`：Jacobi 频率阻尼、Jacobi/GS/SOR 真残差与非正规暂态；
- `plots/preconditioning/`：对称预条件谱、PCG 真残差与块强度—总工作权衡；
- `plots/conjugate-gradient/`：能量几何、谱聚集加速与低精度递推残差漂移；
- `plots/residual-minimization/`：完整/重启 GMRES、对称不定 MINRES 与重启维数—正交成本权衡；
- `plots/sparse-computing/`：CSR/COO 存储交叉、二维网格消元填充与并行负载分配；
- `plots/randomized-low-rank/`：随机 SVD 的过采样分位数、幂步—pass 交换与独立概率证书；
- `plots/error-propagation/`：局部 Jacobian 乘积、一范数条件估计与弱方向的 residual-only 误停；
- `plots/stable-kernels/`：顺序/pairwise/补偿归约、点积消去与 FP16/FP32 accumulator 分层；
- `plots/iterative-refinement/`：binary16 LU、残差精度地板、classical IR/GMRES-IR 与奇异因子边界；
- `figures/determinant/`：单位正方形在线性映射下的体积缩放示意图；
- `figures/duality/`：协向量等值线、Riesz 表示向量与逆转置坐标配对。
- `figures/eigen/`：代数/几何重数对照、Jordan 链—Jordan 块—核空间增长，以及 Schur 三角结构—不变子空间—数值路线的统一示意。
- `figures/matrix-functions/`：主矩阵函数的等价定义、完整矩阵/作用量/Fréchet 导数算法分流与 AI 接口。
- `figures/polar-decomposition/`：SVD 到方向/伸缩因子、满秩/秩亏唯一性、最近点、迭代、微分与 Muon 的统一路线。
- `figures/matrix-sign/`：从虚轴谱分割到对合、互补谱投影、Newton/Schur、条件性和 AI 稳定模态的统一路线。
- `figures/information-theory/`：自信息—二元熵—码树、joint/conditional chain rule，以及 cross-entropy—KL—logits 稳定计算三组教学图。
