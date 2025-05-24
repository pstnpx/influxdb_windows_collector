# InfluxDB Windows Collector

**Custom InfluxDB Collector for Windows**

This project provides a custom collector designed to gather system metrics on Windows machines and send them to an InfluxDB instance. It's particularly useful for monitoring Windows-based systems in environments where native support is limited.

## Features (Current)

- Collects detailed hardware metrics using OpenHardwareMonitorLib:
  - CPU temperature and load
  - GPU temperature and usage
  - Fan speeds and voltages
  - System and component temperatures
- Sends collected data to InfluxDB for storage and analysis
- Lightweight and easily extendable

> 📌 Note: Current data sources are limited to OpenHardwareMonitor. WMI and psutil will be integrated in future releases to provide additional system metrics such as memory usage, disk I/O, and network statistics.

## Prerequisites

- Python 3.12 or higher
- An accessible InfluxDB instance (local or remote)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pstnpx/influxdb_windows_collector.git
   cd influxdb_windows_collector
   ```

2. **Install required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Navigate to working directory (src)**

   ```bash
   cd src
   ```
## Configuration

Before running the collector, configure the InfluxDB connection settings:

1. **Update a `config.ini` file in the project directory with the following content:**

   ```ini
   [influxdb]
   url = http://localhost:8086
   token = your_influxdb_token
   org = your_organization
   bucket = your_bucket
   ```

   Replace the placeholders with your actual InfluxDB details.

## Usage

Run the collector using the following command:

```bash
python app.py
```

## Background

This project was inspired by limitations encountered with Telegraf on Windows systems. While Telegraf is a powerful tool for metric collection, it was unable to correctly retrieve certain hardware-specific data on Windows platforms, such as:

- GPU metrics (usage, temperature)
- Fan speeds
- Voltage levels

To address these gaps, this custom Python-based collector was developed using libraries such as OpenHardwareMonitor. Future versions will include WMI and psutil to provide a more complete and accurate set of system metrics for Windows environments.

This tool complements or replaces Telegraf in scenarios where detailed Windows hardware telemetry is critical.

## Why Not Just Use Telegraf?

While [Telegraf](https://github.com/influxdata/telegraf) is a widely used tool for collecting system metrics, it has known limitations on Windows—particularly when it comes to accessing detailed hardware sensor data.

### ❌ Metrics Telegraf Often Fails to Collect on Windows

#### 1. GPU Metrics
- GPU core usage (per GPU)
- GPU memory usage
- GPU temperature
- GPU power draw
- Fan speed (per GPU)
- VRAM clock speed

> ⚠️ The default `inputs.win_perf_counters` plugin does not expose most GPU-level stats. NVML (NVIDIA Management Library) isn’t used by Telegraf natively.

#### 2. Motherboard and System Sensors
- Fan speeds (case, CPU, GPU, chipset)
- Voltage readings (Vcore, 3.3V, 5V, 12V, etc.)
- Temperature sensors (CPU socket, motherboard, VRMs)
- Power consumption (total system or component-specific)

> ⚠️ These require low-level access via OpenHardwareMonitor or LibreHardwareMonitor, which Telegraf does not integrate with by default.

#### 3. Battery Metrics
- Battery charge/discharge rate
- Battery health or cycle count
- Battery temperature

#### 4. Drive and Storage Metrics
- SMART attributes (e.g., power-on hours, temperature, reallocated sectors)
- Disk serial number, model info
- Per-physical-drive stats (if software RAID or Storage Spaces are used)

#### 5. Network Interface Metrics
- Per-process network usage
- Network adapter temperature or link status
- WiFi signal strength

#### 6. PCI/Peripheral Hardware
- Sensor info from sound cards, RAID controllers, USB hubs, etc.
- Thermal or voltage telemetry for peripheral cards

#### 7. CPU Deep Metrics
- CPU Package Power (e.g., from Intel RAPL)
- Individual CPU core voltage or frequency (beyond average load)

---

This collector addresses these limitations by leveraging:
- **OpenHardwareMonitorLib.dll**
- Planned: **Windows Management Instrumentation (WMI)**
- Planned: **psutil**

to provide a more accurate and comprehensive set of metrics on Windows systems.

## Future Enhancements

Currently, this collector retrieves metrics primarily through **OpenHardwareMonitorLib**, which provides rich access to hardware sensor data like GPU usage, fan speeds, voltages, and temperatures.

However, additional support is planned to further enhance metric coverage using:

- **WMI (Windows Management Instrumentation)**: for querying system-level data such as process information, battery status, network configurations, and device details.
- **psutil**: for dynamic process, memory, disk I/O, and network interface monitoring.

These integrations will improve flexibility and completeness, allowing for more granular and customizable monitoring tailored to each system's configuration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.