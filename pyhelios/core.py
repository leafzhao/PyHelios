"""
PyHelios 高级接口
"""

from .config import get_default_config
from .dataio import HeliosData
from .plotting import HeliosPlotter

class PyHelios:
    def __init__(self, file_path, config=None):
        self.config = config or get_default_config()
        self.data = HeliosData(file_path, self.config)
        self.plotter = HeliosPlotter(self.config)

    def load_and_process(self):
        self.data.load()
        self.data.process()

    def plot_radius(self, **kwargs):
        return self.plotter.plot_radius(self.data, **kwargs)

    def plot_density(self, **kwargs):
        return self.plotter.plot_density(self.data, **kwargs)
