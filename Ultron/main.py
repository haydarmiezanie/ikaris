import argparse
from helpers.logging import get_logger
from colorama import init as colorama_init, Fore, Style
from checker.source_verification import source_verification
from checker.file_verification import file_verification
from checker.model_card_verification import model_card_verification

# Initialize color output
colorama_init()
logging = get_logger("Ultron")


def main(model_id):
    """
    Runs the 3-layer verification process for a given Hugging Face model.

    Parameters:
        model_id (str): The Hugging Face model ID to be validated.

    Returns:
        None
    """
    info_count = 0
    warning_count = 0
    critical_count = 0

    # 1st Layer: Source verification
    first_layer_result, info_count, warning_count = source_verification(model_id, info_count, warning_count)

    if (first_layer_result.get('Creator') == 'Unknown') and (first_layer_result.get('Model Publisher') == 'Unknown'):
        logging.critical('Both Creator and Model Publisher are unknown. This may introduce risks or security issues.')
        return

    if first_layer_result.get('Tags') == 'Unknown':
        logging.warning('This model does not provide tags which may be critical to determine use cases or risks.')

    # 2nd Layer: File & folder safety review
    second_layer_result, info_count, warning_count, critical_count = file_verification(
        model_id, first_layer_result, info_count, warning_count, critical_count
    )

    if 'Critical' in second_layer_result:
        logging.critical(f"Security halt: {second_layer_result['Critical']}")
        return
    elif 'Warning' in second_layer_result:
        logging.warning(f"Remember: {second_layer_result['Warning']}")

    # 3rd Layer: Model card and metadata review
    third_layer_result, info_count, warning_count = model_card_verification(
        model_id, info_count, warning_count
    )

    # Final summary
    print(f"\nSummary: {Fore.GREEN}{info_count} Info{Style.RESET_ALL}, "
          f"{Fore.YELLOW}{warning_count} Warning{Style.RESET_ALL}, "
          f"{Fore.RED}{critical_count} Critical{Style.RESET_ALL}")


if __name__ == '__main__':
    description = """
    Ultron - Open-Source Model Safety Checker

    A security validation tool that examines whether an open-source AI model can be safely
    executed in your environment. Ultron performs comprehensive safety checks including:

    - Malware/payload detection in model files
    - Suspicious code patterns
    - Known vulnerability scanning
    - Resource usage analysis
    - Permission/access requirements
    - Compatibility with your system configuration

    The tool generates a detailed safety report with risk assessment and recommendations
    before you deploy the model in production environments.
    """
    epilog = """
    Examples:
        Basic safety scan:          ultron --model_id author/model

    Notes:
    - Supported formats: Hugging Face only (for now)
    - Run with admin privileges for full system impact analysis

    Security Disclaimer:
    Always verify checksums from official sources. Ultron provides heuristic analysis
    but cannot guarantee complete safety. Report issues at: haydarsaja@gmail.com
    """

    parser = argparse.ArgumentParser(
        prog='ultron',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--model_id',
                        help='Model ID on Hugging Face (e.g., bert-base-uncased)',
                        required=True)

    args = parser.parse_args()
    main(args.model_id)
