#!/usr/bin/env python3
"""
VPN Runner - Easy start script for the local VPN server

This script provides a simple interface to start and manage the VPN server.
"""

import sys
import os
import subprocess
import signal
import time
import threading


def show_banner():
    """Show VPN banner."""
    print("🔐 PowerofCopilot Local VPN")
    print("=" * 40)
    print("Privacy-focused local proxy server")
    print("✅ Blocks ads and trackers")
    print("✅ Masks IP in logs")  
    print("✅ Adds privacy headers")
    print("✅ Completely free")
    print()


def check_dependencies():
    """Check if all dependencies are available."""
    try:
        # Test basic Python modules
        import socket, threading, select, urllib.request
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False


def start_vpn_server(port=8888):
    """Start the VPN server."""
    if not check_dependencies():
        print("❌ Cannot start VPN - missing dependencies")
        return False
    
    if not os.path.exists('vpn_server.py'):
        print("❌ vpn_server.py not found")
        return False
    
    print(f"🚀 Starting VPN server on port {port}...")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        # Start the VPN server
        subprocess.run([sys.executable, 'vpn_server.py', str(port)])
        return True
    except KeyboardInterrupt:
        print("\n🛑 VPN server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting VPN server: {e}")
        return False


def show_help():
    """Show help information."""
    print("VPN Runner - Local Privacy VPN")
    print()
    print("Usage:")
    print("  python3 vpn_runner.py [command] [port]")
    print()
    print("Commands:")
    print("  start [port]  - Start VPN server (default port: 8888)")
    print("  setup         - Show browser setup instructions")
    print("  test          - Test VPN server connection")
    print("  help          - Show this help")
    print()
    print("Examples:")
    print("  python3 vpn_runner.py start")
    print("  python3 vpn_runner.py start 9999")
    print("  python3 vpn_runner.py setup")
    print()


def run_client_command(command):
    """Run a VPN client command."""
    if not os.path.exists('vpn_client.py'):
        print("❌ vpn_client.py not found")
        return False
    
    try:
        subprocess.run([sys.executable, 'vpn_client.py', command])
        return True
    except Exception as e:
        print(f"❌ Error running client command: {e}")
        return False


def main():
    """Main function."""
    show_banner()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        port = 8888
        if len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("❌ Error: Port must be a number")
                return
        
        start_vpn_server(port)
    
    elif command == 'setup':
        run_client_command('setup')
    
    elif command == 'test':
        run_client_command('test')
    
    elif command == 'help':
        show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python3 vpn_runner.py help' for usage information")


if __name__ == "__main__":
    main()