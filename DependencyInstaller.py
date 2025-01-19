import subprocess
import sys
import importlib
import os
import platform
import tarfile
import zipfile
import urllib.request
import shutil


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


def get_pypy_download_url():
    base_url = "https://downloads.python.org/pypy/"
    system = platform.system().lower()
    arch = platform.architecture()[0]

    if system == "windows":
        extension = "zip"
        os_key = "win32" if arch == "32bit" else "win64"
    elif system == "linux":
        extension = "tar.bz2"
        os_key = "linux64" if "64bit" in arch else "linux32"
    elif system == "darwin":
        extension = "tar.bz2"
        os_key = "macos64"
    else:
        raise Exception(f"Unsupported platform: {system}")

    version = "pypy3.9-v7.3.12"  # Update this to the desired version
    file_name = f"{version}-{os_key}.{extension}"
    return base_url + file_name, file_name


def download_pypy(url, destination):
    print(f"Downloading PyPy from {url}...")
    urllib.request.urlretrieve(url, destination)
    print(f"Downloaded PyPy to {destination}")


def extract_pypy(file_path, extract_to):
    print(f"Extracting PyPy to {extract_to}...")
    if file_path.endswith(".tar.bz2"):
        with tarfile.open(file_path, "r:bz2") as tar:
            tar.extractall(path=extract_to)
    elif file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path=extract_to)
    else:
        raise Exception(f"Unsupported archive format: {file_path}")
    print(f"Extracted PyPy to {extract_to}")


def setup_pypy():
    """Handles the setup and installation of PyPy."""
    libs_dir = os.path.join(os.getcwd(), "libs")
    pypy_dir = os.path.join(libs_dir, "pypy")

    # Check if PyPy is already installed
    if os.path.exists(pypy_dir):
        print(f"PyPy is already installed in {pypy_dir}. Skipping installation.")
        return

    # Create directories
    os.makedirs(libs_dir, exist_ok=True)

    # Get PyPy download URL
    download_url, file_name = get_pypy_download_url()

    # Download PyPy archive
    archive_file_path = os.path.join(libs_dir, file_name)
    download_pypy(download_url, archive_file_path)

    # Extract PyPy
    extract_pypy(archive_file_path, libs_dir)

    # Move extracted folder to a consistent name
    extracted_dir = os.path.join(libs_dir, os.listdir(libs_dir)[0])  # First extracted folder
    shutil.move(extracted_dir, pypy_dir)

    # Clean up the archive
    os.remove(archive_file_path)
    print(f"PyPy installed in {pypy_dir}")

    # Add PyPy to PATH
    pypy_bin = os.path.join(pypy_dir, "bin" if platform.system() != "Windows" else "")
    print(f"To use PyPy, add the following to your PATH:\n{pypy_bin}")


if __name__ == "__main__":
    # Ensure dependencies are checked first
    print("Checking and installing Python dependencies...")
    check_and_install_dependencies()

    # Then handle PyPy installation
    print("\nSetting up PyPy...")
    setup_pypy()

    print("\nAll setup steps completed successfully!")
