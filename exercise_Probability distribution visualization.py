import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_bernoulli():
    p = 0.7
    x = np.array([0,1])
    y = np.array([1-p, p])
    plt.bar(x, y, color=['#1f77b4'],alpha=0.7)
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title('Bernoulli Distribution')
    plt.xticks([0, 1])
    plt.show()

def plot_gaussian():
    x = np.linspace(-10, 10, 100)
    y = norm.pdf(x, 0, 2)
    plt.plot(x, y, color='#1f77b4')
    plt.fill_between(x, y, color="#e5360f", alpha=0.3)
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.title('Gaussian Distribution')
    plt.show()

def plot_multinomial():
    p = np.array([0.1,0.4,0.3,0.2])
    x = np.arange(len(p))
    x_values = np.array(['面1','面2','面3','面4'])
    plt.bar(x, p, color=['#1f77b4'],alpha=0.7)
    plt.xticks(x, x_values)
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title('Multinomial Distribution')
    plt.show()

if __name__ == "__main__":
    plot_bernoulli()
    plot_gaussian()
    plot_multinomial()