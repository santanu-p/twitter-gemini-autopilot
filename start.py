#!/usr/bin/env python3
"""
Startup script that automatically fixes Python 3.13 compatibility
and then runs the main Twitter automation bot.
"""

import sys
import os
import subprocess

def check_and_fix_imghdr():
    """Check if imghdr exists, install if missing"""
    try:
        import imghdr
        print("✓ imghdr module available")
        return True
    except ImportError:
        print("⚠ imghdr not found, installing compatibility fix...")
        
        # Get site-packages directory
        site_packages = None
        for path in sys.path:
            if 'site-packages' in path and os.path.isdir(path):
                site_packages = path
                break
        
        if not site_packages:
            print("✗ Could not find site-packages directory")
            return False
        
        # imghdr compatibility code
        imghdr_code = '''"""Replacement for removed imghdr module in Python 3.13+"""

def what(file, h=None):
    """Determine image type - simplified version"""
    if h is None:
        if isinstance(file, str):
            with open(file, 'rb') as f:
                h = f.read(32)
        else:
            location = file.tell()
            h = file.read(32)
            file.seek(location)
    
    # Check common image formats
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'
    elif h[:8] == b'\\x89PNG\\r\\n\\x1a\\n':
        return 'png'
    elif h[:2] == b'\\xff\\xd8':
        return 'jpeg'
    elif h[:4] == b'RIFF' and h[8:12] == b'WEBP':
        return 'webp'
    
    return None
'''
        
        # Create imghdr.py in site-packages
        imghdr_path = os.path.join(site_packages, 'imghdr.py')
        
        try:
            with open(imghdr_path, 'w') as f:
                f.write(imghdr_code)
            print(f"✓ Created imghdr.py at: {imghdr_path}")
            
            # Test import
            import imghdr
            print("✓ imghdr module successfully installed!")
            return True
            
        except Exception as e:
            print(f"✗ Error creating imghdr.py: {e}")
            return False

def main():
    """Main startup function"""
    print("="*60)
    print("Twitter AI Automation - Startup Script")
    print("="*60)
    print(f"Python version: {sys.version.split()[0]}")
    print()
    
    # Check and fix Python 3.13 compatibility
    if not check_and_fix_imghdr():
        print("\n✗ Failed to fix Python 3.13 compatibility")
        print("Please run: pip install tweepy --upgrade")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Starting Twitter Automation Bot...")
    print("="*60 + "\n")
    
    # Import and run main application
    try:
        from main import TwitterAutomation
        automation = TwitterAutomation()
        automation.run()
    except KeyboardInterrupt:
        print("\n\n✓ Automation stopped by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()