# Local VPN Server

A free, local VPN proxy server that provides privacy protection by:

1. **🎭 IP Address Masking** - Masks your IP in server logs for privacy
2. **🚫 Search History Protection** - Blocks tracking of your browsing habits
3. **🛡️ Tracker Blocking** - Blocks common ad and tracking domains
4. **🔒 Ad Blocking** - Filters out advertisements automatically
5. **💰 Completely Free** - No subscriptions or external services required

## VPN Features

- 🔐 **Local Privacy Proxy**: Runs entirely on your machine
- 🚫 **Ad & Tracker Blocking**: Blocks 50+ common ad/tracker domains
- 🔒 **Privacy Headers**: Adds DNT and privacy protection headers
- 🎭 **IP Masking**: Masks real IP addresses in logs
- 📝 **Custom Blocklists**: Supports custom domain blocking
- 🌐 **HTTP/HTTPS Support**: Handles both secure and regular traffic
- ⚡ **Fast & Lightweight**: Minimal resource usage

## Quick VPN Setup

1. **Start the VPN server:**
   ```bash
   python3 vpn_runner.py start
   ```

2. **Configure your browser:**
   ```bash
   python3 vpn_client.py setup
   ```

3. **Test privacy protection:**
   ```bash
   python3 vpn_client.py test
   ```

## VPN Usage

### Starting the VPN Server

```bash
# Start with default settings (port 8888)
python3 vpn_runner.py start

# Start on custom port
python3 vpn_runner.py start 9999

# Start directly with server script
python3 vpn_server.py [port]
```

### Browser Configuration

**Quick Setup:**
```bash
python3 vpn_client.py setup
```

**Manual Chrome/Edge Setup:**
1. Go to Settings → Advanced → System
2. Click "Open your computer's proxy settings"
3. Enable "Use a proxy server"
4. Set Address: `127.0.0.1`, Port: `8888`

**Manual Firefox Setup:**
1. Go to Settings → General → Network Settings
2. Select "Manual proxy configuration"
3. Set HTTP Proxy: `127.0.0.1`, Port: `8888`
4. Set HTTPS Proxy: `127.0.0.1`, Port: `8888`

### VPN Client Commands

```bash
# Show browser setup instructions
python3 vpn_client.py setup

# Generate PAC file for automatic configuration
python3 vpn_client.py pac

# Test VPN server connection
python3 vpn_client.py test

# Show privacy testing guide
python3 vpn_client.py privacy

# Show how to disable proxy
python3 vpn_client.py disable

# Check VPN status
python3 vpn_client.py status
```

## Privacy Protection Details

**What Gets Blocked:**
- Google Analytics, DoubleClick, Facebook trackers
- Amazon, Yahoo, Microsoft ad networks
- Social media tracking pixels
- Common malware and suspicious domains

**Privacy Features:**
- Adds `DNT: 1` (Do Not Track) header
- Adds `X-Privacy-Protected: true` header
- Masks real IP addresses in server logs
- Blocks requests to known tracker domains

**Testing Your Protection:**
After configuring your browser proxy:
1. Visit news websites - ads should be blocked
2. Check `https://httpbin.org/headers` - should show privacy headers
3. Browse normally - trackers and ads will be filtered

## Custom Blocklists

Edit `blocklist.txt` to add your own blocked domains:
```
# Add domains to block (one per line)
annoying-ads.com
tracking-site.net
unwanted-domain.org
```

## VPN Limitations

This is a **local privacy proxy**, not a full VPN service:
- ✅ Blocks ads and trackers locally
- ✅ Adds privacy headers
- ✅ Masks IP in server logs
- ❌ Does not change your external IP address
- ❌ Does not encrypt traffic beyond your machine
- ❌ Does not route through external servers

For complete anonymity, consider using Tor or a commercial VPN service in addition to this tool.

## Technical Implementation

### Files Overview

- **`vpn_server.py`** - Main VPN proxy server with HTTP/HTTPS support and privacy filtering
- **`vpn_client.py`** - Client configuration tool for easy browser setup
- **`vpn_runner.py`** - Simple startup script with user-friendly interface
- **`blocklist.txt`** - Customizable blocklist with 40+ ad/tracker domains

### Architecture

- **HTTP/HTTPS Proxy Server**: Handles all web traffic with privacy filtering
- **Domain Blocklist**: Pre-configured ad/tracker domains (easily customizable)
- **Privacy Headers**: Automatically adds DNT (Do Not Track) headers
- **IP Masking**: Replaces real IPs with private range IPs in logs
- **Custom Block Page**: Shows friendly "🛡️ Content Blocked" message
- **Zero Dependencies**: Uses only built-in Python libraries

## Testing Results

Successfully tested blocking of major tracking networks:
- ✅ DoubleClick advertising network
- ✅ Facebook tracking pixels  
- ✅ Google Analytics tracking
- ✅ Amazon advertising system
- ✅ 36+ other tracker/ad domains

## Browser Support

The VPN provides multiple setup options:
- Manual proxy configuration with step-by-step guides
- PAC (Proxy Auto-Config) file generation
- Support for Chrome, Firefox, Safari, and Edge

## Requirements

- Python 3.6 or higher
- No additional dependencies required (uses built-in libraries)

## License

This project is open source and available under the MIT License.