import os
import sys
from pathlib import Path

# Add the project root to the path so we can import the modules
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_centralized_output_directory():
    """Test that all applications use the same centralized output directory."""
    
    # Import the output directory from config
    from config import OUTPUT_DIR
    
    # Import output paths from all applications
    from apps.cli.main import OUTPUT_PATH as CLI_OUTPUT
    from apps.gui.gui import OUTPUT_PATH as GUI_OUTPUT
    from apps.telegram_bot.telegram_bot import OUTPUT_DIR_PATH as TELEGRAM_OUTPUT
    from core.export_pdf import OUTDIR as CORE_EXPORT_OUTPUT
    from core.io import OUTPUT_DIR as CORE_IO_OUTPUT
    
    # Convert all paths to strings for comparison
    config_output = str(OUTPUT_DIR)
    cli_output = str(CLI_OUTPUT)
    gui_output = str(GUI_OUTPUT)
    telegram_output = str(TELEGRAM_OUTPUT)
    core_export_output = str(CORE_EXPORT_OUTPUT)
    core_io_output = str(CORE_IO_OUTPUT)
    
    # Print all output directories for verification
    print(f"Config output directory: {config_output}")
    print(f"CLI output directory: {cli_output}")
    print(f"GUI output directory: {gui_output}")
    print(f"Telegram output directory: {telegram_output}")
    print(f"Core export output directory: {core_export_output}")
    print(f"Core IO output directory: {core_io_output}")
    
    # Verify all applications use the same output directory
    assert config_output == cli_output, f"CLI output directory {cli_output} does not match config {config_output}"
    assert config_output == gui_output, f"GUI output directory {gui_output} does not match config {config_output}"
    assert config_output == telegram_output, f"Telegram output directory {telegram_output} does not match config {config_output}"
    assert config_output == core_export_output, f"Core export output directory {core_export_output} does not match config {config_output}"
    assert config_output == core_io_output, f"Core IO output directory {core_io_output} does not match config {config_output}"
    
    print("\n✅ All applications are using the same centralized output directory!")
    
    # Verify the directory exists
    output_path = Path(OUTPUT_DIR)
    assert output_path.exists(), f"Output directory {output_path} does not exist"
    print(f"✅ Output directory {output_path} exists!")

if __name__ == "__main__":
    test_centralized_output_directory()