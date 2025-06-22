import requests
from datetime import datetime
from ikaris.helpers.logging import get_logger
from huggingface_hub import model_info
from colorama import Fore, Style

logging = get_logger("FirstLayer")


def lower_case_keys(data):
    """
    Recursively convert all dictionary keys in a nested structure to lowercase.
    
    Args:
        data (dict or list): The data to process.

    Returns:
        dict or list: The processed data with all keys in lowercase.
    """
    if isinstance(data, dict):
        return {k.lower(): lower_case_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [lower_case_keys(elem) for elem in data]
    return data


def fetch_package_source_info(package_name):
    """
    Retrieve package metadata and source info from PyPI and optionally GitHub.

    Args:
        package_name (str): PyPI package name (optionally with ==version).

    Returns:
        dict: Metadata including version, release date, license, source URL,
              GitHub repo info (if available), etc.
    """
    try:
        DEPS_DEV_API = "https://api.deps.dev/v3/systems/pypi/packages"
        if '==' in package_name:
            package_name, version = package_name.split('==', 1)
        else:
            version_url = f"{DEPS_DEV_API}/{package_name}"
            version_response = requests.get(version_url)
            version_data = version_response.json()

            for v in version_data.get('versions', []):
                if v.get('isDefault'):
                    version = v['versionKey']['version']
                    break
            else:
                return {'Critical': [f"Could not determine default version for package '{package_name}'."], 'Warning': [], 'Info': []}

        pypi_url = f"https://pypi.org/pypi/{package_name}/{version}/json"
        response = requests.get(pypi_url)

        data = lower_case_keys(response.json())
        info = data.get('info', {})

        version = info.get('version', 'Unknown')

        license_type = info.get('license') or "Unknown"
        is_open_source = "Yes" if license_type.lower() != "proprietary" else "No"

        project_urls = info.get('project_urls') or {}
        project_url = (
            project_urls.get('source') or
            project_urls.get('repository') or
            project_urls.get('homepage') or
            info.get('home_page') or
            "Unknown"
        )

        result = {
            "Source": f"https://pypi.org/project/{package_name}/",
            "Version": version,
            "License": license_type[:10],
            "Open Source": is_open_source,
            "Project URL": project_url
        }
        
        # GitHub enrichment
        if "github.com" in project_url.lower():
            try:
                parts = project_url.split("github.com/")[1].split('/')
                owner, repo = parts[0], parts[1].rstrip('.git')
                github_api = f"https://api.github.com/repos/{owner}/{repo}"

                # Use GitHub headers to detect rate limits or issues
                headers = {"Accept": "application/vnd.github+json"}

                repo_data = requests.get(github_api, headers=headers).json()
                commits_data = requests.get(f"{github_api}/commits", headers=headers).json()
                contributors_data = requests.get(f"{github_api}/contributors", headers=headers).json()

                latest_commit_date = commits_data[0]['commit']['committer']['date']
                latest_commit = datetime.fromisoformat(latest_commit_date.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')

                result.update({
                    "Active Developers": len(contributors_data),
                    "Last Maintenance (GitHub Commit)": latest_commit,
                })
            except Exception as e:
                result["GitHub Info"] = f"Failed to fetch GitHub info: {str(e)}"
        else:
            result["GitHub Info"] = "Unknown"

        return result

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error fetching PyPI info for '{package_name}': {e}")
    except Exception as e:
        logging.error(f"Unexpected error in fetch_package_source_info: {e}")

    return {
        "Source": f"https://pypi.org/project/{package_name}/",
        "Version": "Unknown",
        "License": "Unknown",
        "Open Source": "Unknown",
        "Project URL": "Unknown",
        "Active Developers": "Unknown",
        "Last Maintenance (GitHub Commit)": "Unknown",
    }


def fetch_model_source_info(model_id):
    """
    Retrieve source and metadata information from Hugging Face Hub.

    Args:
        model_id (str): Hugging Face model identifier.

    Returns:
        dict: Model repo URL, author, type, tags, and downloads.
    """
    try:
        info = model_info(model_id)

        return {
            "Source": f"https://huggingface.co/{model_id}",
            "Creator": info.author or "Unknown",
            "Model Publisher": info.config.get('model_type', "Unknown") if info.config else "Unknown",
            "Tags": info.tags or [],
            "Downloads": info.downloads or "Unknown"
        }
    except Exception as e:
        logging.error(f"Unexpected error fetching model info for '{model_id}': {e}")

    return {
        "Source": f"https://huggingface.co/{model_id}",
        "Creator": "Unknown",
        "Model Publisher": "Unknown",
        "Tags": "Unknown",
        "Downloads": "Unknown"
    }


def source_verification(model_id, package_name, info_count=0, warning_count=0):
    """
    Verifies the origin of a model or package and logs source metadata.

    Args:
        model_id (str): Hugging Face model ID.
        package_name (str): PyPI package name.
        info_count (int): Count of current 'info' level logs.
        warning_count (int): Count of current 'warning' level logs.

    Returns:
        tuple: (metadata_dict, updated_info_count, updated_warning_count)
    """
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    print("Source Verification")
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    if model_id:
        info = fetch_model_source_info(model_id)
    elif package_name:
        info = fetch_package_source_info(package_name)
    else:
        logging.warning("No model ID or package name provided.")
        return {}, info_count, warning_count + 1

    for key, value in info.items():
        if value == "Unknown" or value == []:
            logging.warning(f"{key}: {value}")
            warning_count += 1
        else:
            logging.info(f"{key}: {value}")
            info_count += 1

    return info, info_count, warning_count
