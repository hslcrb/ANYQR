import sys
from cli_logic import run_cli, LONG_HELP

if __name__ == "__main__":
    if not run_cli():
        # If no arguments provided for CLI-only version, just show help
        print(LONG_HELP)
    sys.exit(0)
