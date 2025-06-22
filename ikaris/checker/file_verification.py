from ikaris.helpers.logging import get_logger
from huggingface_hub import list_repo_files
from colorama import Fore, Style

logging = get_logger("SecondLayer")

# File patterns to flag
CRITICAL_PATTERNS = ("model.py", "setup.py")
WARNING_PATTERNS = (".py",)

def check_hugging_face(model_id):
    """
    Checks the files in a Hugging Face model repository for potentially harmful files.

    Args:
        model_id (str): The identifier of the Hugging Face model.

    Returns:
        dict: Messages categorized as 'Critical', 'Warning', or 'Info'.
    """
    list_info = {
        'Critical': [],
        'Warning': [],
        'Info': []
    }

    try:
        repo_files = list_repo_files(model_id)
    except Exception as e:
        list_info['Critical'].append(f"Unexpected error while checking '{model_id}': {str(e)}")
        return list_info

    for file in repo_files:
        if file.endswith(CRITICAL_PATTERNS):
            list_info['Critical'].append(
                f"This model contains '{file}' which might execute code during loading."
            )
        elif file.endswith(WARNING_PATTERNS):
            list_info['Warning'].append(
                f"This model contains '{file}', which may include executable code."
            )
        else:
            list_info['Info'].append(f"{file} is considered safe.")

    return list_info

def file_verification(model_id, info_count=0, warning_count=0, critical_count=0):
    """
    Logs categorized review of files in a Hugging Face model repo.

    Args:
        model_id (str): Hugging Face model ID.
        info_count (int): Initial info counter.
        warning_count (int): Initial warning counter.
        critical_count (int): Initial critical counter.

    Returns:
        tuple: (info_dict, updated_info_count, warning_count, critical_count)
    """
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    print("File & Folder Review")
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    info = check_hugging_face(model_id)

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
