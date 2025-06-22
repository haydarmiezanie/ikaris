from ikaris.helpers.logging import get_logger
from huggingface_hub import ModelCard, HfApi
from colorama import Fore, Style

logging = get_logger("ThirdLayer")

def check_model_card_and_metadata(model_id):
    """
    Checks the Hugging Face model card and metadata for documentation completeness.
    
    Args:
        model_id (str): The model ID on Hugging Face.

    Returns:
        dict: Categorized messages under 'Info', 'Warning', and 'Critical'.
    """
    messages = {
        'Info': [],
        'Warning': [],
        'Critical': []
    }

    # Check for model card content
    try:
        card = ModelCard.load(model_id)
        if not card.content or len(card.content.strip()) == 0:
            messages['Warning'].append("This model does not contain any documentation.")
        else:
            messages['Info'].append("This model contains clear documentation.")
    except Exception as e:
        messages['Warning'].append(f"Failed to load model card: {str(e)}")

    # Check for metadata
    try:
        api = HfApi()
        model_info = api.model_info(model_id)
        if not model_info.cardData:
            messages['Warning'].append(
                f"This model does not contain metadata. Read documentation before executing. "
                f"Check this: https://huggingface.co/{model_id}/blob/main/README.md"
            )
        else:
            messages['Info'].append("This model contains clear metadata.")
    except Exception as e:
        messages['Warning'].append(f"Failed to retrieve model metadata: {str(e)}")

    return messages

def model_card_verification(model_id, info_count=0, warning_count=0, critical_count=0):
    """
    Verifies the Hugging Face model card and metadata, and logs the results.
    
    Args:
        model_id (str): The model identifier.
        info_count (int): Current count of info-level messages.
        warning_count (int): Current count of warning-level messages.
        critical_count (int): Current count of critical-level messages.

    Returns:
        tuple: (messages_dict, updated_info_count, updated_warning_count, updated_critical_count)
    """
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    print("Model Card Review")
    print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    messages = check_model_card_and_metadata(model_id)

    for level, logs in messages.items():
        for msg in logs:
            if level == "Warning":
                warning_count += 1
                logging.warning(msg)
            elif level == "Critical":
                critical_count += 1
                logging.critical(msg)
            else:
                info_count += 1
                logging.info(msg)

    return messages, info_count, warning_count, critical_count
