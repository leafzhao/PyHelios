#!/Users/zhaoxu/miniconda3/envs/Exps/bin/python

"""
PyHelios 使用示例
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyhelios import PyHelios
from pyhelios.analysis import detect_shock_front
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg") # 设置matplotlib后端为Qt5Agg

# 示例：初始化并使用PyHelios
file_path = '/Users/zhaoxu/Library/CloudStorage/GoogleDrive-xu.zhao@york.ac.uk/My Drive/2.3- Code/Jupyter/PyHelios/testdata/130PP-15J-2ns.exo'
helios = PyHelios(file_path)

helios.load_and_process()

# 设置xlim和ylim的例子
ax1 = helios.plot_radius(xlim=(0, 5), ylim=(-20, 120),line_width=0.1,line_color='black')

# # 使用修正后的负梯度冲击波追踪算法
ax2 = helios.plot_density(xlim=(0, 5), ylim=(-20, 120), shocktrack=True, density_threshold=2)
ax3 = helios.plot_eletemp(xlim=(0, 5), ylim=(-20, 120))
ax4 = helios.plot_iontemp(xlim=(0, 5), ylim=(-20, 120))
ax5 = helios.plot_radtemp(xlim=(0, 5), ylim=(-20, 120))
ax6 = helios.plot_pressure(xlim=(0, 5), ylim=(-20, 120))
# ax7 = helios.plot_fluidvel(xlim=(0, 5), ylim=(-20, 120))

# # 独立的冲击波轨迹图（使用负梯度算法）
ax8 = helios.plot_shocktrack(density_threshold=2)
ax9 = helios.plot_max_pressure(smooth=True, window_length=11, polyorder=3)
ax10 = helios.plot_max_density(smooth=True, window_length=11, polyorder=3)

# 计算冲击波位置
# shock_pos = detect_shock_front(helios.data.data['mass_density'], helios.data.data['radius_edges'], helios.data.data['time_edges'], density_threshold=2.0)
# print("冲击波位置数组:", shock_pos)
# print("冲击波位置数组长度:", len(shock_pos))
# print("冲击波位置数组形状:", shock_pos.shape)

plt.show()

