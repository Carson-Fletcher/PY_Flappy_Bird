"""Build the app for the current operating system."""
import PyInstaller.__main__ as pyinstaller


def main() -> None:
    """Main execution"""
    pyinstaller.run([
        "main.py",
        "-F",
        "-w"
    ])


if __name__ == "__main__":
    main()
