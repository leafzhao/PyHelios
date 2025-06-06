"""
数据加载与处理模块
"""
import xarray as xr
import numpy as np

class HeliosData:
    def __init__(self, file_path, config=None):
        self.file_path = file_path
        self.config = config
        self.raw_data = None
        self.processed = False
        self.data = {}

    def load(self):
        """加载原始数据"""
        self.raw_data = xr.open_dataset(self.file_path)

    def process(self):
        """处理数据"""
        if self.raw_data is None:
            self.load()
        data = self.raw_data
        # Extract variables and convert to numpy arrays
        time_whole = data['time_whole'].values *1e9 # ns
        zone_boundaries = data['zone_boundaries'].values * 1e4 # um
        mass_density = data['mass_density'].values
        elec_density = data['elec_density'].values
        ion_temperature = data['ion_temperature'].values
        elec_temperature = data['elec_temperature'].values
        rad_temperature = data['radiation_temperature'].values
        zone_mass = data['zone_mass'].values
        pressure = data['ion_pressure'].values + data['elec_pressure'].values
        fluid_velocity = data['fluid_velocity'].values / 100000  # Convert to km/s
        volume = zone_mass / mass_density

        # Calculate time edges for pcolormesh
        time_diff = np.diff(time_whole) / 2
        time_edges = np.concatenate(([time_whole[0] - time_diff[0]], time_whole[:-1] + time_diff, [time_whole[-1] + time_diff[-1]]))

        # Calculate radius edges for pcolormesh
        radius_diff = np.diff(zone_boundaries, axis=0) / 2
        radius_edges = np.vstack((zone_boundaries[0, :] - radius_diff[0, :],
                                  zone_boundaries[:-1, :] + radius_diff,
                                  zone_boundaries[-1, :] + radius_diff[-1, :]))

        self.data = {
            "time_whole": time_whole,
            "zone_boundaries": zone_boundaries,
            "mass_density": mass_density,
            "elec_density": elec_density,
            "ion_temperature": ion_temperature,
            "elec_temperature": elec_temperature,
            "rad_temperature": rad_temperature,
            "zone_mass": zone_mass,
            "pressure": pressure,
            "fluid_velocity": fluid_velocity,
            "volume": volume,
            "time_edges": time_edges,
            "radius_edges": radius_edges
        }
        self.processed = True

    def get(self, key):
        """获取处理后的数据"""
        return self.data.get(key)
