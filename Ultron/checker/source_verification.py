from helpers.logging import get_logger
from huggingface_hub import model_info
from colorama import Fore, Style

logging = get_logger("FirstLayer")


def fetch_model_source_info(model_id):
    """
    Fetches source and metadata information for a Hugging Face model.

    Parameters:
        model_id (str): The Hugging Face model ID.

    Returns:
        dict: Contains model source URL, creator, model type, tags, and download count.
    """
    try:
        info = model_info(model_id)
        repo_url = f"https://huggingface.co/{model_id}"

        creator = info.author or "Unknown"
        model_publisher = info.config.get('model_type', "Unknown") if info.config else "Unknown"
        tags = info.tags or "Unknown"
        downloads = info.downloads or "Unknown"

        return {
            "Source": repo_url,
            "Creator": creator,
            "Model Publisher": model_publisher,
            "Tags": tags,
            "Downloads": downloads
        }
    except Exception as e:
        logging.error(f"Error fetching model info from HuggingFace: {e}")
        return {
            "Source": f"https://huggingface.co/{model_id}",
            "Creator": "Unknown",
            "Model Publisher": "Unknown",
            "Tags": "Unknown",
            "Downloads": "Unknown"
        }


def source_verification(model_id, info_count=0, warning_count=0):
    """
    Logs the verification result of the model's source information.

    Parameters:
        model_id (str): The Hugging Face model ID.
        info_count (int): Existing count of info logs.
        warning_count (int): Existing count of warning logs.

    Returns:
        tuple: (model_info_dict, updated_info_count, updated_warning_count)
    """
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    print("Source Verification")
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    info = fetch_model_source_info(model_id)

    for key, value in info.items():
        if value == "Unknown":
            logging.warning(f"{key}: {value}")
            warning_count += 1
        else:
            logging.info(f"{key}: {value}")
            info_count += 1

    return info, info_count, warning_count
