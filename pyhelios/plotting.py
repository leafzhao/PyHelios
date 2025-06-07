"""
绘图与风格模块
"""
import os
try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - optional dependency
    plt = None
try:
    import numpy as np
except Exception:  # pragma: no cover - optional dependency
    np = None
from .analysis import detect_shock_front, max_pressure, smoothed_mass_density

class HeliosPlotter:
    def __init__(self, config=None):
        self.config = config or {}
        self._apply_style()

    def _apply_style(self):
        """设置matplotlib全局风格"""
        if plt is None:
            return
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
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
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
        '''
        绘制密度图,支持shocktrack叠加主冲击波界面，负梯度最大密度梯度法
        '''
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
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
        shocktrack = kwargs.get('shocktrack', False)
        density_threshold = kwargs.get('density_threshold', 1.1)
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, density.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"$\rho$ (g/cc)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
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
        if shocktrack:
            shock_pos = detect_shock_front(density, radius_edges, time_edges, density_threshold)
            ax.plot(time_edges[:-1], shock_pos, 'w--', lw=1)
        return ax

    def plot_eletemp(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        elec_temperature = data['elec_temperature']
        file_path = getattr(helios_data, 'file_path', None)
        fname = os.path.splitext(os.path.basename(file_path))[0] if file_path else ''
        title = f"{fname} Electron Temperature"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, elec_temperature.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"$T_e$ (keV)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        return ax

    def plot_iontemp(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        ion_temperature = data['ion_temperature']
        file_path = getattr(helios_data, 'file_path', None)
        fname = os.path.splitext(os.path.basename(file_path))[0] if file_path else ''
        title = f"{fname} Ion Temperature"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, ion_temperature.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"$T_i$ (keV)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        return ax

    def plot_radtemp(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        rad_temperature = data['rad_temperature']
        file_path = getattr(helios_data, 'file_path', None)
        fname = os.path.splitext(os.path.basename(file_path))[0] if file_path else ''
        title = f"{fname} Radiation Temperature"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, rad_temperature.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"$T_r$ (keV)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        return ax

    def plot_pressure(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        pressure = data['pressure']
        file_path = getattr(helios_data, 'file_path', None)
        fname = os.path.splitext(os.path.basename(file_path))[0] if file_path else ''
        title = f"{fname} Pressure"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, pressure.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"P (Mbar)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        return ax

    def plot_fluidvel(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        fluid_velocity = data['fluid_velocity']
        file_path = getattr(helios_data, 'file_path', None)
        fname = os.path.splitext(os.path.basename(file_path))[0] if file_path else ''
        title = f"{fname} Fluid Velocity"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        cmap = kwargs.get('cmap', self.config.get('cmap'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, fluid_velocity.T, shading='auto', cmap=cmap)
        cbar = fig.colorbar(cmesh, ax=ax)
        cbar.ax.tick_params(labelsize=font_size, length=tick_length, width=tick_width)
        cbar.outline.set_linewidth(border_width)
        cbar_label = r"Fluid Velocity (km/s)"
        cbar.ax.text(0.5, 1.02, cbar_label, ha='center', va='bottom', fontsize=font_size, fontfamily=font_family, transform=cbar.ax.transAxes)
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(font_family)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        plt.show()
        return ax

    def plot_shocktrack(self, helios_data, **kwargs):
        '''独立可视化主冲击波界面随时间的演化，返回shock_pos数组'''
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        density = data['mass_density']
        density_threshold = kwargs.get('density_threshold', 1.1)
        shock_pos = detect_shock_front(density, radius_edges, time_edges, density_threshold)
        file_path = getattr(helios_data, 'file_path', None)
        if file_path:
            fname = os.path.splitext(os.path.basename(file_path))[0]
        else:
            fname = ''
        title = f"{fname} Shock Front Trajectory"
        figsize = kwargs.get('figsize', self.config.get('figsize'))
        font_size = self.config.get('font_size')
        font_family = self.config.get('font_family')
        dpi = self.config.get('dpi')
        border_width = self.config.get('border_width')
        tick_length = self.config.get('tick_length')
        tick_width = self.config.get('tick_width')
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        ax.plot(time_edges[:-1], shock_pos, 'r-', lw=2, label='Shock Front')
        ax.set_xlabel("Time (ns)", fontsize=font_size, fontfamily=font_family)
        ax.set_ylabel(r"Radius ($\mu$m)", fontsize=font_size, fontfamily=font_family)
        ax.set_title(title, fontsize=font_size, fontfamily=font_family)
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])
        ax.legend(fontsize=font_size)
        ax.tick_params(axis='both', which='major', labelsize=font_size, length=tick_length, width=tick_width)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        plt.show()
        return ax

    def plot_max_pressure(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time = data['time'] if 'time' in data else data['time_whole']
        pressure = data['pressure']
        max_p = max_pressure(pressure)
        fig, ax = plt.subplots(figsize=kwargs.get('figsize', self.config.get('figsize')))
        ax.plot(time, max_p, label='Max Pressure (smoothed)')
        ax.set_xlabel('Time (ns)')
        ax.set_ylabel('Max Pressure (Mbar)')
        ax.legend()
        return ax

    def plot_mass_density_smooth(self, helios_data, **kwargs):
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        data = helios_data.data
        time_edges = data['time_edges']
        radius_edges = data['radius_edges']
        mass_density = data['mass_density']
        mass_density_smooth = smoothed_mass_density(mass_density)
        fig, ax = plt.subplots(figsize=kwargs.get('figsize', self.config.get('figsize')))
        cmesh = ax.pcolormesh(time_edges, radius_edges.T, mass_density_smooth.T, shading='auto')
        ax.set_xlabel('Time (ns)')
        ax.set_ylabel('Radius (um)')
        ax.set_title('Smoothed Mass Density')
        return ax
