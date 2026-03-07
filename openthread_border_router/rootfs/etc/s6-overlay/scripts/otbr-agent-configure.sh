#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
# ==============================================================================
# Configure OTBR depending on add-on settings
# ==============================================================================

# Read the thread interface name that was selected during startup
thread_if="wpan0" # Default fallback
if [ -f /tmp/otbr-thread-interface ]; then
  thread_if=$(cat /tmp/otbr-thread-interface)
fi

# Set the socket path for ot-ctl to connect to the correct instance
export OT_CLI_CONNECT_SOCKET="/run/openthread-${thread_if}.sock"

# If border routing is disabled, we run minimal configuration
if bashio::config.true 'disable_border_routing'; then
  bashio::log.info "Border routing is disabled - running as Thread router"
  bashio::log.info "Web UI will be available for manual network configuration"

  # Wait for socket with a shorter timeout since we expect it might not fully work
  count=0
  while [ ! -S "${OT_CLI_CONNECT_SOCKET}" ]; do
    sleep 0.5
    count=$((count + 1))
    if [ $count -ge 20 ]; then
      bashio::log.warning "OpenThread socket not available"
      bashio::log.info "Web UI may have limited functionality"
      exit 0
    fi
  done

  bashio::log.info "OpenThread socket available at ${OT_CLI_CONNECT_SOCKET}"
  bashio::log.info "Use the web UI to manually configure Thread network"
  exit 0
fi

# Full border router configuration (when border routing is enabled)
bashio::log.info "Waiting for OpenThread socket to be created..."
timeout=30
count=0
while [ ! -S "${OT_CLI_CONNECT_SOCKET}" ]; do
  sleep 0.5
  count=$((count + 1))
  if [ $count -ge $((timeout * 2)) ]; then
    bashio::log.error "Timeout waiting for OpenThread socket: ${OT_CLI_CONNECT_SOCKET}"
    bashio::log.error "The socket was not created within ${timeout} seconds."
    exit 1
  fi
done

bashio::log.info "OpenThread socket created successfully"

# Configure TREL (Thread Radio Encapsulation Link)
ot-ctl trel enable

if bashio::config.true 'nat64'; then
  bashio::log.info "Enabling NAT64."
  ot-ctl nat64 enable
  ot-ctl dns server upstream enable
fi

# To avoid asymmetric link quality the TX power from the controller should not
# exceed that of what other Thread routers devices typically use.
ot-ctl txpower 6
