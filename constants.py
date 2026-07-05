"""
物理常数与论文标定参数
对应论文：量子纠缠与量子纠错驱动的时空与规范场涌现
作者：刘双云
"""

import math

# ==================== 基本物理常数 (CODATA) ====================
PLANCK_LENGTH = 1.616255e-35      # 米, ℓ_p
SPEED_OF_LIGHT = 2.99792458e8     # 米/秒, c
HBAR = 1.054571817e-34            # J·s, ℏ
PLANCK_MASS = 2.176434e-8         # kg
PLANCK_ENERGY = 1.220890e19       # GeV
G_NEWTON = 6.67430e-11            # m³/(kg·s²)

# ==================== 论文标定常数 ====================
# 特征码距 d₀ ≈ 12, 由潘建伟团队表面码实验数据独立标定
# Λ(3,7) = 1.40 → d₀ = 4/ln(1.40) ≈ 11.89 ≈ 12
LAMBDA_37 = 1.40                  # 实验测得逻辑错误率抑制因子
LAMBDA_37_ERR = 0.06              # 实验误差
D_0_EXACT = 4.0 / math.log(LAMBDA_37)  # ≈ 11.89
D_0 = 12.0                         # 论文采用值（四舍五入）

# ==================== 宇宙学参数 ====================
# GRB 221009A
GRB_REDSHIFT = 0.151
GRB_LUMINOSITY_DISTANCE = 0.745e9 * 3.0857e16  # 0.745 Gpc → 米
GRB_D_EFF = GRB_LUMINOSITY_DISTANCE / PLANCK_LENGTH  # ≈ 1.4 × 10^60

# LHAASO 二阶能标约束
E_LIV2_LIMIT = 7.3e36  # eV

# 暗能量
KAPPA_THEORY = math.pi**4 / 9.0   # ≈ 10.83
KAPPA_OBSERVED = 10.7             # 观测值
KAPPA_DEVIATION = abs(KAPPA_THEORY - KAPPA_OBSERVED) / KAPPA_OBSERVED  # ≈ 1.2%

# 对接常数
C_DOCKING = 32.0 * math.pi / 3.0  # ≈ 33.51

# ==================== 表面码参数 ====================
# 逻辑错误率: ε_L(d) = A(p) · exp(-d/d₀)
# 噪声阈值 (表面码)
P_THRESHOLD = 0.01  # 1% 典型值

# 实验码距范围 (潘建伟团队)
D_EXP_MIN = 3
D_EXP_MAX = 7

# 未来验证目标码距
D_FUTURE_TARGET = 50
