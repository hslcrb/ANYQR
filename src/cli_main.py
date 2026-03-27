import sys
from cli_logic import run_cli, interactive_shell

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # If no arguments provided for CLI-only version, enter interactive shell
        interactive_shell()
    else:
        run_cli(sys.argv[1:])
    sys.exit(0)
