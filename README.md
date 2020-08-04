![PyPI](https://img.shields.io/pypi/v/auto-pi-lot)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/auto-pi-lot)](https://pypi.org/project/auto-pi-lot/)
[![Documentation Status](https://readthedocs.org/projects/auto-pi-lot/badge/?version=latest)](https://docs.auto-pi-lot.com/en/latest/?badge=latest)
![PyPI - Status](https://img.shields.io/pypi/status/auto-pi-lot)

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md) 


# Autopilot

![Autopilot Banner Logo](docs/_images/autopilot_logo_banner.png)

| [Docs](https://docs.auto-pi-lot.com) | [Paper](https://www.biorxiv.org/content/10.1101/807693v1) | [Forum](https://groups.google.com/forum/#!forum/autopilot-users) | [Hardware](https://auto-pi-lot.com/hardware/) |
| :-: | :-: | :-: | :-: |
| [![Read the Docs](docs/_images/docs_link.png)](https://docs.auto-pi-lot.com) | [![Paper](docs/_images/paper_link.png)](https://www.biorxiv.org/content/10.1101/807693v1)  | [![Forum](docs/_images/discussion_link.png)](https://groups.google.com/forum/#!forum/autopilot-users) | [![Hardware (Coming Soon!)](docs/_images/hardware_link_construction.png)](https://auto-pi-lot.com/hardware)

Autopilot is a Python framework for performing complex, hardware-intensive behavioral experiments with swarms of networked Raspberry Pis. 
It is designed to unify experiments 

* **Flexibility** - Autopilot was designed for any hardware and any experiment -- 
  its hardware API is designed to give a structured wrapper around the code you already use, and its task design is
  entirely non-prescriptive. It attempts to eliminate the need for researchers to use a patchwork of mutually incompatible tools to perform complex
  experiments. Autopilot is a hacker's plaything -- rather than a uniform, simplified experience,
  its modular design and complete API-level documentation is meant to encourage users to make and break core Autopilot modules.
* **Efficiency** - Autopilot uses Python as a glue around high-performance, low-level libraries,
  and is fully concurrent across multiple threads, processes, and computers. Its distributed
  design eliminates the hard limits faced by by single-computer
  systems, letting researchers use arbitrary numbers and combinations of hardware components
  to perform complex, hardware-intensive experiments at scale.
* **Reproducibility** - Autopilot obsessively documents data provenance,
  logging the entire history of an Animal's training, including any version and local
  code changes. Any part of an experiment that isn't documented is considered a bug. By integrating experiments and producing data that is
  clean at the time of acquisition, Autopilot makes it easy to do good science -- its goal is to allow
  exact experimental replication from a single file. 

# Distributed Behavior

Autopilot's premise is simple: to scale experiments, *just use more computers*.

Autopilot systems consist of multiple "Agents" -- computers with specialized roles in the swarm.
One user-facing "Terminal" agent allows a researcher to control many "Pilots," or computers that perform experiments (typically the beloved Raspberry Pi).
Each Pilot can coordinate one or many "Children" to offload subsets of an experiment's computational or hardware requirements.
Users can use and misuse Autopilot's flexible modules to make whatever agent topology they need <3. 

![Autopilot System Diagram](docs/_images/whole_system_black.png)

# Getting Started

[**All documentation is hosted at https://docs.auto-pi-lot.com**](https://docs.auto-pi-lot.com)

Installation is simple, just install with pip and use Autopilot's guided setup to configure your environment and preferences.
The initial setup routine uses a CLI interface that is SSH friendly :)

```bash
pip3 install auto-pi-lot
python3 -m autopilot.setup.setup_autopilot
```

![Autopilot Setup Console](docs/_images/installer.png)

All of Autopilot is quite new, so bugs, incomplete documentation, missing features are very much expected! Don't be shy about
[raising issues](https://github.com/wehr-lab/autopilot/issues) or [asking questions in the forum](https://groups.google.com/forum/#!forum/autopilot-users).



# What's new?

**[v0.3.0](https://docs.auto-pi-lot.com/en/latest/changelog/v0.3.0.html#changelog-v030)**

After much ado, we're releasing Autopilot's first major upgrade. Cameras, Continuous data, DeepLabCut, and a lot more!

- Autopilot has moved to Python 3!! (Tested on 3.6-3.8)
- Capturing video with OpenCV and the Spinnaker SDK is now supported (See autopilot.hardware.cameras)
- An I2C_9DOF motion sensor and the MLX90640 temperature sensor are now supported.
- Timestamps from GPIO events are now microsecond-precise thanks to some modifications to the pigpio library
- GPIO output timing is also microsecond-precise thanks to the use of pigpio scripts, so you can deliver exactly the reward volumes you intend <3
- Hardware modules have been refactored into their own module, and have been almost wholly rebuilt to have sensible inheritance structure.
- Networking modules are more efficient and automatically compress arrays (like video frames!) on transmission. Streaming is also easier now, check out Net_Node.get_stream() !
- We now have a detailed development roadmap , so you can see the magnificent future we have planned.
- We have created the autopilot-users discussion board for troubleshooting & coordinating community development :)


# What's next?

[Autopilot Development Todo](https://docs.auto-pi-lot.com/en/latest/todo.html)
