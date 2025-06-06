"""
PyHelios 配置与样式集中管理
"""

def get_default_config():
    """返回默认配置字典，可用于全局和用户自定义覆盖。"""
    return {
        'font_size': 7,
        'font_family': 'Arial',
        'dpi': 200,
        'border_width': 0.5,
        'tick_length': 3,
        'tick_width': 0.5,
        'figsize': (8.5 / 2.54, 8.5 / 1.618 / 2.54),
        'cmap': 'jet',
    }
