# PyHelios

高能物理辐射流体动力学数据分析与可视化工具。

## 特性
- 支持HELIOS等辐射流体动力学仿真数据的读取、分析与可视化
- 冲击波界面自动检测与后处理
- 各类物理量（密度、温度、压力等）可视化
- 支持批量后处理、平滑、最大值轨迹分析等

## 安装
```bash
# 推荐使用conda环境
conda create -n pyhelios python=3.10 matplotlib numpy scipy
pip install -r requirements.txt
```

## 用法示例
```python
from pyhelios import PyHelios
helios = PyHelios('yourfile.exo')
helios.load_and_process()
helios.plot_max_pressure()
helios.plot_max_density()
shock_pos = helios.get('shock_pos')
```

## 目录结构
```
PyHelios/
  pyhelios/         # 主包
    analysis.py     # 数据分析
    plotting.py     # 绘图
    dataio.py       # 数据IO
    core.py         # 高层接口
    ...
  examples/         # 示例脚本
  tests/            # 单元测试
  testdata/         # 测试数据
  README.md         # 项目说明
  requirements.txt  # 依赖
```

## 贡献
欢迎issue和PR！

## 许可证
MIT 