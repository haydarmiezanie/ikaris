import argparse
import sys
from ikaris.helpers.logging import get_logger
from colorama import init as colorama_init, Fore, Style
from ikaris.checker.source_verification import source_verification
from ikaris.checker.file_verification import file_verification
from ikaris.checker.model_card_verification import model_card_verification
from ikaris.checker.dependencies_verification import dependencies_verification
from ikaris.checker.vulnerability_verification import vulnerability_verification

# Initialize color output
colorama_init()
logging = get_logger("Ikaris")


def main():
    description = """
    Ikaris: Hugging Face Model and Package Risk & Safety Checker

    Ikaris is a CLI tool designed to verify and analyze the trustworthiness, origin, and integrity of machine learning models hosted on the Hugging Face platform and python package. 
    It performs multi-layered security and metadata checks to help researchers and developers ensure that models they intend to use do not introduce unexpected risks.
    """
    epilog = """
    Command Layers:
    1. Source Verification: Identifies creator, publisher, and basic metadata.
    2. File Verification: Reviews files and folders inside the model repo for suspicious or non-standard content.
    3. Model Card Review: Validates completeness and clarity of the model card documentation.
    4. Dependencies Verification: Checks for known vulnerabilities in Python packages.
    5. Vulnerability Check: Uses OSV API to identify known vulnerabilities in the package.

    Example Usage:
    ikaris check hf-model tensorblock/Llama-3-ELYZA-JP-8B-GGUF
    ikaris check package requests==2.31.0

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

    # Subcommand: check
    check_parser = subparsers.add_parser("check", help="Check various resources")
    check_subparsers = check_parser.add_subparsers(dest="subcommand")

    hf_parser = check_subparsers.add_parser("hf-model", help="Check Hugging Face model")
    hf_parser.add_argument("model_id", help="ID of the Hugging Face model")

    package_parser = check_subparsers.add_parser("package", help="Check PyPI package")
    package_parser.add_argument("package_name", help="Name of the Python package (e.g., requests==2.31.0)")

    args = parser.parse_args()

    # Determine target
    model_id = args.model_id if args.command == "check" and args.subcommand == "hf-model" else None
    package_name = args.package_name if args.command == "check" and args.subcommand == "package" else None

    if not (model_id or package_name):
        parser.print_help()
        return

    # Initial counts
    info_count = warning_count = critical_count = 0

    # 1st Layer: Source Verification
    first_layer_result, info_count, warning_count = source_verification(
        model_id, package_name, info_count, warning_count
    )

    if model_id:
        if (first_layer_result.get('Creator') == 'Unknown') and (first_layer_result.get('Model Publisher') == 'Unknown'):
            logging.critical('Both Creator and Model Publisher are unknown. This may introduce risks or security issues.')
            sys.exit(1)

        if first_layer_result.get('Tags') == 'Unknown':
            logging.warning('This model does not provide tags which may be critical to determine use cases or risks.')

    # 2nd Layer: File/Dependency Check
    if model_id:
        second_layer_result, info_count, warning_count, critical_count = file_verification(
            model_id, info_count, warning_count, critical_count
        )
    else:
        second_layer_result, info_count, warning_count, critical_count = dependencies_verification(
            package_name, info_count, warning_count, critical_count
        )

    if second_layer_result.get('Critical'):
        logging.critical(f"Security halt due to critical issues: {second_layer_result['Critical']}")
        sys.exit(1)

    if second_layer_result.get('Warning'):
        logging.warning(f"Warnings found: {second_layer_result['Warning']}")

    # 3rd Layer: Model Card or Vulnerability Check
    if model_id:
        third_layer_result, info_count, warning_count, critical_count = model_card_verification(
            model_id, info_count, warning_count, critical_count
        )
    else:
        third_layer_result, info_count, warning_count, critical_count = vulnerability_verification(
            package_name, info_count, warning_count, critical_count
        )

    if third_layer_result.get('Critical'):
        logging.critical(f"Security halt due to documentation/vulnerability issues: {third_layer_result['Critical']}")
        sys.exit(1)

    # Summary Output
    print(f"\nSummary: {Fore.GREEN}{info_count+warning_count+critical_count} Info{Style.RESET_ALL}, "
          f"{Fore.YELLOW}{warning_count} Warning{Style.RESET_ALL}, "
          f"{Fore.RED}{critical_count} Critical{Style.RESET_ALL}")
    
    if warning_count > 10/100*(info_count+warning_count+critical_count):
        print(f"{Fore.RED}Package warning count is more than 10% of tolerance level. This may indicate potential risks or security issues.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Package warning count is within tolerance level.")


if __name__ == '__main__':
    main()
