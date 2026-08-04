# Home Assistant App: OpenThread Border Router App (No USB - Marcelo's fork)

OpenThread Border Router app (formerly known as add-on). The app uses the upstream OpenThread
Border Router implementation and wraps it as an app for Home Assistant.

**This is Marcelo's personal fork.** It patches the `device` option to be optional so the
app can run using only `network_device` (a network-connected RCP radio), without requiring
a USB serial device to be configured.

**NOTE:** This requires a supported 802.15.4 capable radio with OpenThread
RCP firmware. If you are using [Home Assistant Yellow](https://www.home-assistant.io/yellow/) or [Home Assistant Connect ZBT-1](https://www.home-assistant.io/connectzbt1/) (previously called SkyConnect) then
the correct firmware is automatically installed.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

## About

This app allows you to form or join a Thread network and make Home Assistant
a Thread Border Router.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
