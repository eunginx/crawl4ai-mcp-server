#!/usr/bin/env python3
"""
Test script to verify SSL certificate fix for Supabase connection
"""
import ssl
import socket
import os
import sys

def test_ssl_connection():
    """Test SSL connection to Supabase database"""
    
    # Set SSL certificate file
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    print(f"SSL_CERT_FILE set to: {os.environ['SSL_CERT_FILE']}")
    
    try:
        # Test SSL context creation
        ctx = ssl.create_default_context()
        print("✅ SSL context created successfully")
        
        # Test connection to Supabase
        hostname = "db.tcoowuyddxbvmlcpnjsq.supabase.co"
        port = 5432
        
        print(f"Testing connection to {hostname}:{port}")
        
        with ctx.wrap_socket(
            socket.socket(),
            server_hostname=hostname
        ) as s:
            s.connect((hostname, port))
            print("✅ SSL connection to Supabase successful")
            return True
            
    except Exception as e:
        print(f"❌ SSL connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ssl_connection()
    sys.exit(0 if success else 1)
