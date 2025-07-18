#!/usr/bin/env python3
"""
VPN Client Configuration Tool

This tool helps users configure their browsers and system to use the local VPN server
for privacy protection, ad blocking, and tracker blocking.
"""

import os
import sys
import subprocess
import platform
import json


class VPNClient:
    def __init__(self, server_host='127.0.0.1', server_port=8888):
        """Initialize VPN client configuration."""
        self.server_host = server_host
        self.server_port = server_port
        self.system = platform.system().lower()
    
    def show_manual_setup(self):
        """Show manual proxy setup instructions."""
        print("🔧 Manual Browser Proxy Configuration")
        print("=" * 50)
        print(f"Proxy Server: {self.server_host}")
        print(f"Proxy Port: {self.server_port}")
        print()
        
        print("📋 Chrome/Chromium Setup:")
        print("1. Open Chrome Settings")
        print("2. Go to Advanced > System")
        print("3. Click 'Open your computer's proxy settings'")
        print("4. Enable 'Use a proxy server'")
        print(f"5. Set Address: {self.server_host}")
        print(f"6. Set Port: {self.server_port}")
        print("7. Check 'Use the same proxy server for all protocols'")
        print()
        
        print("📋 Firefox Setup:")
        print("1. Open Firefox Settings")
        print("2. Go to General > Network Settings")
        print("3. Click 'Settings...'")
        print("4. Select 'Manual proxy configuration'")
        print(f"5. HTTP Proxy: {self.server_host} Port: {self.server_port}")
        print(f"6. HTTPS Proxy: {self.server_host} Port: {self.server_port}")
        print("7. Check 'Use this proxy server for all protocols'")
        print()
        
        print("📋 Safari Setup (macOS):")
        print("1. Open Safari Preferences")
        print("2. Go to Advanced tab")
        print("3. Click 'Change Settings...' next to Proxies")
        print("4. Check 'Web Proxy (HTTP)'")
        print(f"5. Set Server: {self.server_host} Port: {self.server_port}")
        print("6. Check 'Secure Web Proxy (HTTPS)'")
        print(f"7. Set Server: {self.server_host} Port: {self.server_port}")
        print()
    
    def generate_pac_file(self):
        """Generate a PAC (Proxy Auto-Config) file."""
        pac_content = f"""
function FindProxyForURL(url, host) {{
    // Use VPN proxy for all HTTP and HTTPS traffic
    if (url.substring(0, 4) == 'http' || url.substring(0, 5) == 'https') {{
        return "PROXY {self.server_host}:{self.server_port}";
    }}
    
    // Direct connection for local addresses
    if (isInNet(host, "192.168.0.0", "255.255.0.0") ||
        isInNet(host, "10.0.0.0", "255.0.0.0") ||
        isInNet(host, "172.16.0.0", "255.240.0.0") ||
        host == "localhost" ||
        host == "127.0.0.1") {{
        return "DIRECT";
    }}
    
    return "PROXY {self.server_host}:{self.server_port}";
}}
"""
        
        pac_file = 'vpn_proxy.pac'
        try:
            with open(pac_file, 'w') as f:
                f.write(pac_content.strip())
            
            pac_url = f"file://{os.path.abspath(pac_file)}"
            print(f"✅ Generated PAC file: {pac_file}")
            print(f"📁 PAC URL: {pac_url}")
            print()
            print("🔧 To use PAC file:")
            print("1. In browser proxy settings, select 'Automatic proxy configuration'")
            print(f"2. Enter PAC URL: {pac_url}")
            print()
            return pac_file
        except Exception as e:
            print(f"❌ Error generating PAC file: {e}")
            return None
    
    def test_connection(self):
        """Test connection to VPN server."""
        print("🔍 Testing VPN server connection...")
        
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.server_host, self.server_port))
            sock.close()
            
            if result == 0:
                print("✅ VPN server is running and accessible")
                return True
            else:
                print("❌ Cannot connect to VPN server")
                print(f"   Make sure vpn_server.py is running on {self.server_host}:{self.server_port}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def show_privacy_test(self):
        """Show how to test privacy protection."""
        print("🧪 Testing Your Privacy Protection")
        print("=" * 50)
        print("After configuring your browser proxy, test these sites:")
        print()
        print("📍 IP Address Test:")
        print("   Visit: https://whatismyipaddress.com")
        print("   Should show your real IP (local VPN doesn't change external IP)")
        print("   But provides privacy protection and ad blocking")
        print()
        print("🚫 Ad Blocking Test:")
        print("   Visit any news website with ads")
        print("   Ads and trackers should be blocked")
        print("   You'll see '🛡️ Content Blocked' messages")
        print()
        print("🔒 Privacy Headers Test:")
        print("   Visit: https://httpbin.org/headers")
        print("   Should show 'DNT: 1' and 'X-Privacy-Protected: true' headers")
        print()
        print("📊 Tracker Blocking Test:")
        print("   Visit: https://www.ghostery.com/ghostery-ad-blocker/")
        print("   Should detect fewer trackers when VPN is active")
        print()
    
    def disable_proxy(self):
        """Provide instructions to disable proxy."""
        print("🔧 To Disable VPN Proxy")
        print("=" * 30)
        print("Chrome/Edge:")
        print("1. Go to proxy settings")
        print("2. Uncheck 'Use a proxy server'")
        print()
        print("Firefox:")
        print("1. Go to Network Settings")
        print("2. Select 'No proxy'")
        print()
        print("Safari:")
        print("1. Go to proxy settings")
        print("2. Uncheck all proxy options")
        print()
    
    def show_status(self):
        """Show current VPN status and configuration."""
        print("📊 VPN Status")
        print("=" * 20)
        print(f"Server: {self.server_host}:{self.server_port}")
        
        if self.test_connection():
            print("Status: ✅ Online")
        else:
            print("Status: ❌ Offline")
        
        # Check if PAC file exists
        if os.path.exists('vpn_proxy.pac'):
            print("PAC File: ✅ Available")
        else:
            print("PAC File: ❌ Not generated")
        
        print()


def main():
    """Main function for VPN client configuration."""
    print("🔐 VPN Client Configuration Tool")
    print("=" * 40)
    
    client = VPNClient()
    
    if len(sys.argv) < 2:
        print("Usage: python3 vpn_client.py <command>")
        print()
        print("Commands:")
        print("  setup    - Show manual proxy setup instructions")
        print("  pac      - Generate PAC file for automatic configuration")
        print("  test     - Test connection to VPN server")
        print("  privacy  - Show privacy testing instructions")
        print("  disable  - Show how to disable proxy")
        print("  status   - Show VPN status")
        print()
        print("Example:")
        print("  python3 vpn_client.py setup")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'setup':
        client.show_manual_setup()
    elif command == 'pac':
        client.generate_pac_file()
    elif command == 'test':
        client.test_connection()
    elif command == 'privacy':
        client.show_privacy_test()
    elif command == 'disable':
        client.disable_proxy()
    elif command == 'status':
        client.show_status()
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()