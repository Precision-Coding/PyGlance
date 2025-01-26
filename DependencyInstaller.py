import subprocess
import sys
import importlib


def read_requirements(file_path="requirements.txt"):
    dependencies = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                # Ignore comments and blank lines
                line = line.strip()
                if line and not line.startswith("#"):
                    if "==" in line:
                        package, version = line.split("==")
                        dependencies[package.strip()] = version.strip()
                    else:
                        # If no version is specified, assume latest
                        dependencies[line.strip()] = None
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please create one.")
        sys.exit(1)
    return dependencies


def check_and_install_dependencies(requirements_file="requirements.txt"):
    dependencies = read_requirements(requirements_file)

    for package, version in dependencies.items():
        try:
            # Try importing the package to check if it's installed
            imported_package = importlib.import_module(package)
            installed_version = getattr(imported_package, '__version__', None)
            if version and installed_version != version:
                print(f"Updating {package} to version {version}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
            else:
                print(f"{package} is already installed and up to date.")
        except ModuleNotFoundError:
            print(f"{package} is not installed. Installing {'latest' if version is None else f'version {version}'}...")
            if version:
                subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"An error occurred while checking {package}: {e}")
            sys.exit(1)