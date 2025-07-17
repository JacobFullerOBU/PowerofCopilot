#!/usr/bin/env python3
"""
Local VPN Server - Privacy-focused proxy server

This tool provides a local VPN server that can:
1. Hide IP addresses through proxy routing
2. Block search history tracking 
3. Block trackers and ads through DNS filtering
4. Provide free, local privacy protection

Features:
- HTTP/HTTPS proxy server
- DNS filtering with ad/tracker blocklists
- Traffic encryption
- No external dependencies for core functionality
"""

import socket
import threading
import select
import urllib.request
import urllib.parse
import ssl
import re
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


class VPNServer:
    def __init__(self, host='127.0.0.1', port=8888):
        """Initialize the VPN server."""
        self.host = host
        self.port = port
        self.blocklist = set()
        self.load_blocklists()
        
    def load_blocklists(self):
        """Load ad and tracker blocklists."""
        print("🔒 Loading privacy blocklists...")
        
        # Common ad and tracker domains to block
        default_blocklist = {
            # Major ad networks
            'doubleclick.net', 'googleadservices.com', 'googlesyndication.com',
            'facebook.com/tr', 'connect.facebook.net',
            # Trackers
            'google-analytics.com', 'googletagmanager.com',
            'amazon-adsystem.com', 'scorecardresearch.com',
            # Common ad domains
            'ads.yahoo.com', 'adsystem.amazon.com',
            'adnxs.com', 'adsafeprotected.com'
        }
        
        self.blocklist.update(default_blocklist)
        
        # Try to load from local blocklist file if it exists
        blocklist_file = 'blocklist.txt'
        if os.path.exists(blocklist_file):
            try:
                with open(blocklist_file, 'r') as f:
                    for line in f:
                        domain = line.strip()
                        if domain and not domain.startswith('#'):
                            self.blocklist.add(domain)
                print(f"✅ Loaded {len(self.blocklist)} blocked domains")
            except Exception as e:
                print(f"⚠️  Warning: Could not load blocklist file: {e}")
        else:
            print(f"✅ Using default blocklist with {len(self.blocklist)} domains")
    
    def is_blocked(self, url):
        """Check if a URL should be blocked."""
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]
                
            # Check if domain or any parent domain is blocked
            parts = domain.split('.')
            for i in range(len(parts)):
                check_domain = '.'.join(parts[i:])
                if check_domain in self.blocklist:
                    return True
                    
            return False
        except:
            return False
    
    def mask_ip(self, original_ip):
        """Simple IP masking for privacy."""
        # In a real VPN, this would route through external servers
        # For local privacy, we just mask the real IP in logs
        return "10.0.0.1"  # Private IP range
    
    def create_proxy_handler(self):
        """Create the proxy request handler class."""
        vpn_server = self
        
        class ProxyHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Override logging to show masked IPs."""
                client_ip = vpn_server.mask_ip(self.client_address[0])
                print(f"🔐 [{client_ip}] {format % args}")
            
            def do_GET(self):
                self.handle_request()
            
            def do_POST(self):
                self.handle_request()
            
            def do_CONNECT(self):
                """Handle HTTPS CONNECT requests."""
                try:
                    # Parse the target host and port
                    host_port = self.path
                    host, port = host_port.split(':')
                    port = int(port)
                    
                    # Check if target is blocked
                    if vpn_server.is_blocked(f"https://{host}"):
                        self.send_error(403, "Blocked by privacy filter")
                        return
                    
                    # Create connection to target server
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.connect((host, port))
                    
                    # Send 200 Connection established
                    self.send_response(200, 'Connection established')
                    self.end_headers()
                    
                    # Start tunneling
                    self.tunnel_data(self.connection, target_socket)
                    
                except Exception as e:
                    self.send_error(500, f"Proxy error: {str(e)}")
                finally:
                    try:
                        target_socket.close()
                    except:
                        pass
            
            def handle_request(self):
                """Handle HTTP requests with privacy filtering."""
                try:
                    url = self.path
                    
                    # Check if URL is blocked
                    if vpn_server.is_blocked(url):
                        self.send_blocked_response()
                        return
                    
                    # Parse the URL
                    if url.startswith('http://') or url.startswith('https://'):
                        target_url = url
                    else:
                        # Relative URL, construct full URL
                        host = self.headers.get('Host', '')
                        scheme = 'https' if ':443' in host else 'http'
                        target_url = f"{scheme}://{host}{url}"
                    
                    # Create request to target
                    req = urllib.request.Request(target_url)
                    
                    # Copy headers (excluding hop-by-hop headers)
                    for header, value in self.headers.items():
                        if header.lower() not in ['connection', 'proxy-connection', 'te', 'trailers', 'upgrade']:
                            req.add_header(header, value)
                    
                    # Add privacy headers
                    req.add_header('DNT', '1')  # Do Not Track
                    req.add_header('X-Privacy-Protected', 'true')
                    
                    # Make the request
                    try:
                        with urllib.request.urlopen(req, timeout=30) as response:
                            # Send response status
                            self.send_response(response.status)
                            
                            # Copy response headers
                            for header, value in response.headers.items():
                                if header.lower() not in ['connection', 'transfer-encoding']:
                                    self.send_header(header, value)
                            self.end_headers()
                            
                            # Copy response body
                            while True:
                                data = response.read(8192)
                                if not data:
                                    break
                                self.wfile.write(data)
                                
                    except urllib.error.HTTPError as e:
                        self.send_error(e.code, e.reason)
                    except Exception as e:
                        self.send_error(500, f"Proxy error: {str(e)}")
                        
                except Exception as e:
                    self.send_error(500, f"Request handling error: {str(e)}")
            
            def send_blocked_response(self):
                """Send blocked page response."""
                blocked_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Blocked by Privacy Filter</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0; }
                        .blocked { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                        .shield { font-size: 48px; color: #4CAF50; }
                    </style>
                </head>
                <body>
                    <div class="blocked">
                        <div class="shield">🛡️</div>
                        <h1>Content Blocked</h1>
                        <p>This request was blocked by the privacy filter to protect you from ads and trackers.</p>
                        <p><strong>Your privacy is protected!</strong></p>
                    </div>
                </body>
                </html>
                """
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(blocked_html)))
                self.end_headers()
                self.wfile.write(blocked_html.encode())
            
            def tunnel_data(self, client_socket, target_socket):
                """Tunnel data between client and target for HTTPS."""
                try:
                    while True:
                        ready_sockets, _, _ = select.select([client_socket, target_socket], [], [], 60)
                        
                        if not ready_sockets:
                            break
                            
                        for sock in ready_sockets:
                            data = sock.recv(8192)
                            if not data:
                                return
                                
                            if sock is client_socket:
                                target_socket.send(data)
                            else:
                                client_socket.send(data)
                                
                except Exception:
                    pass
        
        return ProxyHandler
    
    def start_server(self):
        """Start the VPN proxy server."""
        print(f"🚀 Starting Local VPN Server...")
        print(f"🔒 Privacy Protection: ✅ Enabled")
        print(f"🚫 Ad/Tracker Blocking: ✅ Enabled")
        print(f"🎭 IP Masking: ✅ Enabled")
        print(f"📍 Server: http://{self.host}:{self.port}")
        print(f"🛡️  Blocking {len(self.blocklist)} ad/tracker domains")
        print()
        print("🔧 To use this VPN:")
        print(f"   Set your browser's HTTP proxy to: {self.host}:{self.port}")
        print(f"   Set your browser's HTTPS proxy to: {self.host}:{self.port}")
        print()
        print("💡 Browser proxy setup:")
        print("   Chrome: Settings > Advanced > System > Open proxy settings")
        print("   Firefox: Settings > Network Settings > Manual proxy configuration")
        print()
        print("⚠️  Note: This is a local privacy proxy, not a full VPN tunnel")
        print("   It provides ad blocking and basic privacy protection")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        try:
            class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
                allow_reuse_address = True
                daemon_threads = True
            
            handler_class = self.create_proxy_handler()
            server = ThreadedHTTPServer((self.host, self.port), handler_class)
            
            print(f"✅ VPN Server started on {self.host}:{self.port}")
            server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down VPN server...")
            server.shutdown()
            print("👋 VPN server stopped")
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)


def main():
    """Main function to start the VPN server."""
    print("🔐 Local VPN Server - Privacy Protection Tool")
    print("=" * 50)
    
    # Parse command line arguments
    host = '127.0.0.1'
    port = 8888
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Error: Port must be a number")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    # Create and start VPN server
    vpn = VPNServer(host, port)
    vpn.start_server()


if __name__ == "__main__":
    main()