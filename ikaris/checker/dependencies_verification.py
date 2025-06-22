import requests
from ikaris.helpers.logging import get_logger
from colorama import Fore, Style

logging = get_logger("SecondLayer")

DEPS_DEV_API = "https://api.deps.dev/v3/systems/pypi/packages"

def check_dependencies(package_name, version_package):
    """
    Check dependencies and potential issues using deps.dev API.

    Args:
        package_name (str): Name of the PyPI package.
        version_package (str): Specific version or 'latest'.

    Returns:
        dict: Dictionary with categorized messages: 'Critical', 'Warning', 'Info'.
    """
    try:
        if version_package == 'latest':
            version_url = f"{DEPS_DEV_API}/{package_name}"
            version_response = requests.get(version_url)
            version_data = version_response.json()

            for v in version_data.get('versions', []):
                if v.get('isDefault'):
                    version_package = v['versionKey']['version']
                    break
            else:
                return {'Critical': [f"Could not determine default version for package '{package_name}'."], 'Warning': [], 'Info': []}

        deps_url = f"{DEPS_DEV_API}/{package_name}/versions/{version_package}:dependencies"
        
        deps_response = requests.get(deps_url)
        deps_data = deps_response.json()
        
        result = {'Critical': [], 'Warning': [], 'Info': []}

        if deps_data.get('error'):
            result['Critical'].append(
                f"This package '{package_name}' with version '{version_package}' has an error: {deps_data['error']}"
            )

        for node in deps_data.get('nodes', []):
            dep_name = node['versionKey']['name']
            dep_version = node['versionKey']['version']
            if node.get('errors'):
                result['Critical'].append(
                    f"Critical dependency issue: {dep_name} ({dep_version})"
                )
            else:
                result['Info'].append(
                    f"Dependency found: {dep_name} ({dep_version})"
                )

        return result

    except requests.RequestException as e:
        logging.critical(f"Network error while checking {package_name}: {str(e)}")
        return {'Critical': [f"Network error while checking package '{package_name}'."], 'Warning': [], 'Info': []}
    except Exception as e:
        logging.critical(f"Unexpected error while checking {package_name}: {str(e)}")
        return {'Critical': [f"Unexpected error: {str(e)}"], 'Warning': [], 'Info': []}

def dependencies_verification(package_name, info_count=0, warning_count=0, critical_count=0):
    """
    Verifies dependencies of a given PyPI package and logs categorized messages.

    Args:
        package_name (str): Package name (can include version, e.g., 'requests==2.31.0').
        info_count (int): Initial count of info logs.
        warning_count (int): Initial count of warning logs.
        critical_count (int): Initial count of critical logs.

    Returns:
        tuple: (info_dict, updated_info_count, updated_warning_count, updated_critical_count)
    """
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    print("Dependencies Verification")
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    if '==' in package_name:
        package_name, version_package = package_name.split('==', 1)
    else:
        version_package = 'latest'
    
    info = check_dependencies(package_name.strip(), version_package.strip())

    for level, messages in info.items():
        for message in messages:
            if level == "Critical":
                critical_count += 1
                logging.critical(message)
            elif level == "Warning":
                warning_count += 1
                logging.warning(message)
            else:
                info_count += 1
                logging.info(message)

    return info, info_count, warning_count, critical_count
