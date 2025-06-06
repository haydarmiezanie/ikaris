from helpers.logging import get_logger
from huggingface_hub import list_repo_files
from colorama import Fore, Style

logging = get_logger("FirstLayer")


def check_hugging_face(model_id):
    """
    Checks the files in a Hugging Face model repository for potentially harmful files.
    
    Parameters:
        model_id (str): The identifier of the Hugging Face model.

    Returns:
        dict: Categorized messages under 'Critical', 'Warning', and 'Info'.
    """
    repo_files = list_repo_files(model_id)
    list_info = {
        'Critical': [],
        'Warning': [],
        'Info': []
    }

    for file in repo_files:
        if file.endswith("model.py") or file.endswith("setup.py"):
            list_info['Critical'].append(
                f"This model contains '{file}' which might execute code during loading."
            )
        elif file.endswith(".py"):
            # Note: Author check removed as 'author' is not part of list_repo_files
            list_info['Warning'].append(
                f"This model contains '{file}', which may include executable code."
            )
        else:
            list_info['Info'].append(
                "No suspicious Python files found in the model repository."
            )

    return list_info


def file_verification(model_id, info_count=0, warning_count=0, critical_count=0):
    """
    Verifies files in the Hugging Face model repo and logs categorized messages.

    Parameters:
        model_id (str): Hugging Face model ID.
        info_count (int): Existing info count.
        warning_count (int): Existing warning count.
        critical_count (int): Existing critical count.

    Returns:
        tuple: (info_dict, info_count, warning_count, critical_count)
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
