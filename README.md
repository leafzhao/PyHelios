# PyHelios

A data analysis and visualization tool for high-energy physics radiation hydrodynamics.

## Features
- Support for reading, analyzing and visualizing radiation hydrodynamics simulation data from HELIOS and similar codes
- Automatic shock front detection and post-processing
- Visualization of various physical quantities (density, temperature, pressure, etc.)
- Support for batch post-processing, smoothing, and maximum value trajectory analysis

## Installation
```bash
# Recommended: use conda environment
conda create -n pyhelios python=3.10 matplotlib numpy scipy xarray
pip install -r requirements.txt
```

## Usage Example
```python
from pyhelios import PyHelios
helios = PyHelios('yourfile.exo')
helios.load_and_process()
helios.plot_max_pressure()
helios.plot_max_density()
shock_pos = helios.get('shock_pos')
```

## Project Structure
```
PyHelios/
  pyhelios/         # Main package
    analysis.py     # Data analysis
    plotting.py     # Plotting
    dataio.py       # Data IO
    core.py         # High-level interface
    ...
  examples/         # Example scripts
  tests/            # Unit tests
  testdata/         # Test data
  README.md         # Project description
  requirements.txt  # Dependencies
```

## Contribution
Issues and PRs are welcome!

## License
MIT 