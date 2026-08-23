import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# 设置中文字体，防止图表显示乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]   
plt.rcParams["axes.unicode_minus"] = False

# 1. 先验分布 Beta(1, 1)
a_prior = 1
b_prior = 1
x = np.linspace(0, 1, 100)
y_prior = beta.pdf(x, a_prior, b_prior)

# 2. 后验分布 Beta(8, 4)
a_posterior = 8
b_posterior = 4
y_posterior = beta.pdf(x, a_posterior, b_posterior)

# 3. 画图
plt.plot(x, y_prior, "b--", label="先验 Beta(1,1)", linewidth=2)
plt.plot(x, y_posterior, "r-", label="后验 Beta(8,4)", linewidth=2)

# 4. 添加标题、图例和坐标轴标签
plt.title("贝叶斯推断：从先验到后验", fontsize=15)
plt.xlabel("硬币正面朝上的概率 (p)", fontsize=12)
plt.ylabel("概率密度", fontsize=12)
plt.legend(fontsize=12)

# 5. 显示图表
plt.show()
