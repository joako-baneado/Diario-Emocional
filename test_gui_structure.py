#!/usr/bin/env python3
# test_gui_structure.py - Test the GUI structure without running it
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_gui_structure():
    """Test that the GUI module structure is correct"""
    print("Testing GUI structure...")
    
    # Test import of simple_gui module
    try:
        from app.simple_gui import SimpleEmotionalDiaryGUI
        print("✓ SimpleEmotionalDiaryGUI class can be imported")
    except Exception as e:
        print(f"✗ Error importing SimpleEmotionalDiaryGUI: {e}")
        return False
    
    # Test that we can create an instance (without initializing the GUI)
    try:
        # We'll just test that the class exists and has the right methods
        methods = ['setup_window', 'setup_ui', 'process_emotions', 'clear_all', 'save_session', 'run']
        
        for method in methods:
            if hasattr(SimpleEmotionalDiaryGUI, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
                return False
        
        print("✓ All required methods exist")
        
    except Exception as e:
        print(f"✗ Error testing GUI class: {e}")
        return False
    
    print("✓ GUI structure test passed!")
    return True

if __name__ == "__main__":
    success = test_gui_structure()
    if success:
        print("\nAll GUI structure tests passed!")
    else:
        print("\nSome GUI structure tests failed!")
        sys.exit(1)