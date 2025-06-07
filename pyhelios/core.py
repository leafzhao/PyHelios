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

    def plot_eletemp(self, **kwargs):
        return self.plotter.plot_eletemp(self.data, **kwargs)

    def plot_iontemp(self, **kwargs):
        return self.plotter.plot_iontemp(self.data, **kwargs)

    def plot_radtemp(self, **kwargs):
        return self.plotter.plot_radtemp(self.data, **kwargs)

    def plot_pressure(self, **kwargs):
        return self.plotter.plot_pressure(self.data, **kwargs)

    def plot_fluidvel(self, **kwargs):
        return self.plotter.plot_fluidvel(self.data, **kwargs)

    def plot_shocktrack(self, **kwargs):
        return self.plotter.plot_shocktrack(self.data, **kwargs)

    def get(self, key):
        return self.data.get(key)
