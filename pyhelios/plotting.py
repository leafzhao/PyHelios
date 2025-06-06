"""
绘图与风格模块
"""
import matplotlib.pyplot as plt
import os

class HeliosPlotter:
    def __init__(self, config=None):
        self.config = config or {}
        self._apply_style()

    def _apply_style(self):
        """设置matplotlib全局风格"""
        import matplotlib as mpl
        mpl.rcParams['font.size'] = self.config.get('font_size', 7)
        mpl.rcParams['font.family'] = self.config.get('font_family', 'Arial')
        mpl.rcParams['axes.linewidth'] = self.config.get('border_width', 0.5)
        mpl.rcParams['xtick.major.size'] = self.config.get('tick_length', 3)
        mpl.rcParams['ytick.major.size'] = self.config.get('tick_length', 3)
        mpl.rcParams['xtick.major.width'] = self.config.get('tick_width', 0.5)
        mpl.rcParams['ytick.major.width'] = self.config.get('tick_width', 0.5)

    def plot_radius(self, helios_data, **kwargs):
        """绘制半径演化图"""
        data = helios_data.data
        time = data['time_whole']
        radius = data['zone_boundaries']
        file_path = getattr(helios_data, 'file_path', None)
        if file_path:
            fname = os.path.splitext(os.path.basename(file_path))[0]
        else:
            fname = ''
        title = f"{fname} Trajectory"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        line_width = kwargs.get('line_width', 0.5)
        line_color = kwargs.get('line_color', 'black')
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')

        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        for i in range(radius.shape[1]):
            ax.plot(time, radius[:, i], color=line_color, lw=line_width)

        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        return ax

    def plot_density(self, helios_data, **kwargs):
        """绘制密度图"""
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        density = data['mass_density']
        file_path = getattr(helios_data, 'file_path', None)
        if file_path:
            fname = os.path.splitext(os.path.basename(file_path))[0]
        else:
            fname = ''
        title = f"{fname} Mass Density"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')

        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, density.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"$\rho$ (g/cc)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom',
                     fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        return ax
