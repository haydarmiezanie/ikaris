import argparse
from ikaris.helpers.logging import get_logger
from colorama import init as colorama_init, Fore, Style
from ikaris.checker.source_verification import source_verification
from ikaris.checker.file_verification import file_verification
from ikaris.checker.model_card_verification import model_card_verification

# Initialize color output
colorama_init()
logging = get_logger("Ikaris")


def main():
    description = """
    Ikaris: Hugging Face Model Risk & Safety Checker

    Ikaris is a CLI tool designed to verify and analyze the trustworthiness, origin, and integrity of machine learning models hosted on the Hugging Face platform. 
    It performs multi-layered security and metadata checks to help researchers and developers ensure that models they intend to use do not introduce unexpected risks.
    """
    epilog = """
    Command Layers:
    1. Source Verification: Identifies creator, publisher, and basic metadata.
    2. File Verification: Reviews files and folders inside the model repo for suspicious or non-standard content.
    3. Model Card Review: Validates completeness and clarity of the model card documentation.

    Example Usage:
    ikaris check hf-model tensorblock/Llama-3-ELYZA-JP-8B-GGUF
    ikaris check hf-model tencent/HunyuanVideo-Avatar

    Disclaimer:
    Ikaris does not replace a full security audit. Always combine automated checks with manual review when deploying models in production environments.
    """
    parser = argparse.ArgumentParser(
        prog='ikaris',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: check hf-package
    check_parser = subparsers.add_parser("check", help="Check various resources")
    check_subparsers = check_parser.add_subparsers(dest="subcommand")

    hf_parser = check_subparsers.add_parser("hf-model", help="Check Hugging Face model availability")
    hf_parser.add_argument("model_id", help="ID of the Hugging Face model")

    args = parser.parse_args()

    if args.command == 'check' and args.subcommand == "hf-model":
        model_id = args.model_id
    else:
        parser.print_help()
        return
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
        model_id, info_count, warning_count, critical_count
    )
    if second_layer_result['Critical']:
        logging.critical(f"Security halt: {second_layer_result['Critical']}")
        return
    elif second_layer_result['Warning']:
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
    main()
