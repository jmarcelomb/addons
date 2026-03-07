# Home Assistant App: OpenThread Border Router

## Installation

Follow these steps to get the app (formerly knowon as add-on) installed on your system:

1. In Home Assistant, go to **Settings** > **Apps** > **Install app**.
2. Select the top right menu and **Repository**.
3. Add "https://github.com/home-assistant/addons" to add the **Home Assistant App Repository for Development** repository.
4. Find the **OpenThread Border Router** app and select it.
5. Select the **Install** button.

## How to use

You will need a 802.15.4 capable radio supported by OpenThread flashed with OpenThread
RCP firmware:
- Home Assistant Yellow
- Home Assistant SkyConnect/Connect ZBT-1
- Home Assistant Connect ZBT-2

These devices are all capable to run OpenThread and will be flashed with the correct
firmware by Home Assistant Core.

If you are using Home Assistant Yellow, choose `/dev/ttyAMA1` as device.

### Alternative radios

The website [openthread.io maintains a list of supported platforms][openthread-platforms]
lists other Thread capable radios. A well documented Radio for development is the
Nordic Semiconductor [nRF52840 Dongle][nordic-nrf52840-dongle]. The Dongle needs
a recent version of the OpenThread RCP firmware.
[This article][nordic-nrf52840-dongle-install] outlines the steps to install the
RCP firmware for the nRF52840 Dongle.

Once the firmware is loaded follow the following steps:

1. Select the correct `device` in the app configuration tab and press `Save`.
2. Start the app.

### OpenThread Border Router

This app makes your Home Assistant installation an OpenThread Border Router
(OTBR). The border router can be used to comission Matter devices which connect
through Thread. Home Assistant Core will automatically detect this app and
create a new integration named "Open Thread Border Router". With Home Assistant
Core 2023.3 and newer the OTBR will get configured automatically. The Thread
integration allows to inspect the network configuration.

### Web interface (advanced)

There is also a web interface provided by the OTBR. However, the web
interface has caveats (e.g. forming a network does not generate an off-mesh
routable IPv6 prefix which causes changing IPv6 addressing on first app
restart). It is still possible to enable the web interface for debugging
purpose. Make sure to expose both the Web UI port and REST API port (the
latter needs to be on port 8081) on the host interface. To do so, click on
"Show disabled ports" and enter a port (e.g. 8080) in the OpenThread Web UI
and 8081 in the OpenThread REST API port field).

## Configuration

App configuration:

| Configuration      | Description                                            |
|--------------------|--------------------------------------------------------|
| device (mandatory) | Serial port where the OpenThread RCP Radio is attached |
| baudrate           | Serial port baudrate (depends on firmware)   |
| flow_control       | If hardware flow control should be enabled (depends on firmware) |
| otbr_log_level     | Set the log level of the OpenThread BorderRouter Agent     |
| firewall           | Enable OpenThread Border Router firewall to block unnecessary traffic |
| nat64              | Enable NAT64 to allow Thread devices accessing IPv4 addresses |
| network_device     | IP address and port to connect to a network-based RCP (see below) |
| beta               | Enable beta mode with Thread 1.4 and native OpenThread mDNS |
| thread_interface   | Thread interface name (wpan0-wpan9). **Default: wpan1** (to avoid conflict with Home Assistant's wpan0) |
| disable_border_routing | Disable border routing to avoid conflicts. **Default: true** (recommended for multi-instance setups) |

### Multi-Instance Configuration

This add-on is specifically designed to run **alongside Home Assistant's built-in Thread support**. The defaults are pre-configured for this use case:
- `thread_interface: wpan1` - Uses wpan1 instead of wpan0 (which Home Assistant uses)
- `disable_border_routing: true` - Prevents UDP port conflicts with Home Assistant's border router

#### Default Configuration (Running Alongside Home Assistant)

With the default settings, configure the add-on:
```yaml
device: /dev/ttyUSB1  # Your second Thread radio device
```

The add-on will automatically:
- ✅ Use wpan1 interface (avoiding Home Assistant's wpan0)
- ✅ Run without border routing (avoiding UDP port conflicts)
- ✅ Start the Web UI for manual network configuration

**To join your existing Thread network:**

1. **Get your Thread network credentials from Home Assistant:**
   - Go to **Settings** > **Devices & Services** > **Thread**
   - Click on your Thread network
   - Copy the **Active dataset TLVs**

2. **Extract the Network Key (Master Key) from TLVs:**
   
   The Active dataset TLVs contain all network credentials encoded in TLV (Type-Length-Value) format. To extract the Network Key:
   
   - Look for Type `05` (Network Key) with Length `10` (16 bytes)
   - Example TLV string: `...05 10 aabbccddeeff00112233445566778899...`
     - `05` = Type (Network Key)
     - `10` = Length (0x10 = 16 bytes)
     - `aabbccddeeff00112233445566778899` = Your Network Key
   
   **Quick extraction script:**
   ```python
   # Find Network Key in your dataset TLVs
   dataset = "YOUR_DATASET_TLVS_HERE"
   pos = dataset.find("0510")  # Find Type 05, Length 10
   if pos != -1:
       network_key = dataset[pos+4:pos+36]  # Extract 32 hex chars (16 bytes)
       print(f"Network Key: {network_key}")
   ```

3. **Access the OTBR Web UI:**
   - Navigate to `http://homeassistant.local:8090` (or your configured Web UI port)

4. **Join the network using one of these methods:**

   **Method A: Using Dataset TLVs (Easiest)**
   - Click **"Join"** in the Web UI
   - Paste your Active dataset TLVs (from step 1)
   - Click **"Join"** to connect
   
   **Method B: Using Network Key (Manual)**
   - Click **"Form"** or **"Join"** in the Web UI
   - Enter the Network Key you extracted in step 2
   - Configure other parameters (Channel, PAN ID, Extended PAN ID) from HA's Thread integration
   - Click **"Form"** or **"Join"**

The second OTBR instance will now join Home Assistant's Thread network as an additional router, extending your Thread coverage.

> **Tip:** Method A (Dataset TLVs) is recommended as it automatically configures all network parameters correctly.

#### Running as a Standalone Border Router

If you want to use this as your **only** border router (without Home Assistant's Thread):

```yaml
device: /dev/ttyUSB0  # Your Thread radio
thread_interface: wpan0  # Can use wpan0 since no conflict
disable_border_routing: false  # Enable full border router functionality
```

> [!WARNING]
> The OTBR expects the RCP connected radio to be on a reliable link such as
> UART or SPI. Using TCP/IP to reach a remote RCP radio breaks this assumption.
> If the TCP/IP connection fails, the OTBR will not shutdown cleanly and leave
> stale routes in your network. This will lead to Thread devices to be
> potentially unreachable for up to 30 minutes (route lifetime) even when other
> routers are available.
>
> The RCP protocol is not designed to be transferred over an IP network: It is
> a timing-sensitive protocol. You might experience Thread issues if your
> network link has excessive latencies. As Thread is networking capable,
> running a Thread border router on the system the RCP radio is plugged in is
> recommended.

> [!NOTE]
> When using a network device, you still need to set a dummy serial port device, e.g. `/dev/ttyS3`.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Discord Chat Server][discord].
- The Home Assistant [Community Forum][forum].
- Join the [Reddit subreddit][reddit] in [/r/homeassistant][reddit]

In case you've found a bug, please [open an issue on our GitHub][issue].

[discord]: https://discord.gg/c5DvZ4e
[forum]: https://community.home-assistant.io
[reddit]: https://reddit.com/r/homeassistant
[issue]: https://github.com/home-assistant/addons/issues
[openthread-platforms]: https://openthread.io/platforms
[nordic-nrf52840-dongle]: https://www.nordicsemi.com/Products/Development-hardware/nrf52840-dongle
[nordic-nrf52840-dongle-install]: https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/protocols/thread/tools.html#configuring_a_radio_co-processor
