"""
draw functions or graphs for AP Calculus BC
"""

from matplotlib import pyplot as plt
import numpy as np
import os

if __name__ == "__main__":

    fig_save_dir: str = os.path.join(
        "../..", "resource/sungheeyun.github.io/posts/2026-03-01-PST - ap calculus bc problems"
    )

    # logistic function

    a_coef: float = 1.0
    b_coef: float = 10.0
    y_init: float = 1.0

    c_coef: float = np.log(y_init / (b_coef - y_init))

    t_array_1d: np.ndarray = np.linspace(0.0, 0.75, 1000)
    y_array_1d: np.ndarray = b_coef / (1.0 + np.exp(-a_coef * b_coef * t_array_1d - c_coef))

    half_point: float = -c_coef / a_coef / b_coef

    fig, ax = plt.subplots()
    ax.plot(t_array_1d, y_array_1d)
    ax.set_ylim(0.0, 11.0)
    ax.set_xlim(0.0, t_array_1d.max())
    x_min, x_max = ax.get_xlim()
    ax.plot([x_min, half_point, half_point], [b_coef / 2.0, b_coef / 2.0, 0.0], "r:")
    ax.plot(half_point, b_coef / 2.0, marker="o", color="red", markersize=10)
    ax.plot([x_min, x_max], b_coef * np.ones(2), "k:")
    ax.set_xlim(x_min, x_max)

    print(half_point)

    # fig.savefig(os.path.join(fig_save_dir, "logistic_fcn_01.png"))

    fig.show()

    plt.show()
