# Fix for Python 3.13 compatibility with tweepy
# Run this ONCE before running main.py: python fix_python313.py

import sys
import os

# Add imghdr module for Python 3.13+ compatibility
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

def install_imghdr_fix():
    """Install imghdr compatibility module"""
    try:
        import imghdr
        print("✓ imghdr module already available, no fix needed!")
        return True
    except ImportError:
        print("Installing imghdr compatibility fix...")
        
        # Get site-packages directory
        site_packages = None
        for path in sys.path:
            if 'site-packages' in path and os.path.isdir(path):
                site_packages = path
                break
        
        if not site_packages:
            print("✗ Could not find site-packages directory")
            return False
        
        # Create imghdr.py in site-packages
        imghdr_path = os.path.join(site_packages, 'imghdr.py')
        
        try:
            with open(imghdr_path, 'w') as f:
                f.write(imghdr_code)
            print(f"✓ Created imghdr.py at: {imghdr_path}")
            
            # Test import
            import imghdr
            print("✓ imghdr module successfully installed!")
            print("\nYou can now run: python main.py")
            return True
            
        except Exception as e:
            print(f"✗ Error creating imghdr.py: {e}")
            return False

if __name__ == "__main__":
    print("="*60)
    print("Python 3.13+ Compatibility Fix for Tweepy")
    print("="*60)
    print(f"\nPython version: {sys.version}")
    print(f"Python executable: {sys.executable}\n")
    
    success = install_imghdr_fix()
    
    if not success:
        print("\n" + "="*60)
        print("ALTERNATIVE SOLUTION:")
        print("="*60)
        print("If the automatic fix didn't work, try:")
        print("1. Uninstall tweepy: pip uninstall tweepy")
        print("2. Install latest version: pip install tweepy --upgrade")
        print("3. Or downgrade Python to 3.12 or earlier")