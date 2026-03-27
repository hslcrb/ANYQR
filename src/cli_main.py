import sys
from cli_logic import run_cli, LONG_HELP

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # If no arguments provided for CLI-only version, show help and wait for user to read
        print(LONG_HELP)
        input("\nPress Enter to exit...")
    else:
        if not run_cli():
            print(LONG_HELP)
    sys.exit(0)
