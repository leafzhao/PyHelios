#!/Users/zhaoxu/miniconda3/envs/Exps/bin/python

"""
PyHelios 使用示例
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyhelios import PyHelios
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg") # 设置matplotlib后端为Qt5Agg

# 示例：初始化并使用PyHelios
file_path = '/Users/zhaoxu/Library/CloudStorage/GoogleDrive-xu.zhao@york.ac.uk/My Drive/2.3- Code/Jupyter/PyHelios/testdata/130PP-15J-2ns.exo'
helios = PyHelios(file_path)
helios.load_and_process()
# 设置xlim和ylim的例子
ax1 = helios.plot_radius(xlim=(0, 5), ylim=(-20, 120),line_width=0.1,line_color='black')
ax2 = helios.plot_density(xlim=(0, 5), ylim=(-20, 120))

# 同时显示所有图
plt.show()
