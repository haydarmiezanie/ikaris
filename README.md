# Ikaris

[![PyPI version](https://img.shields.io/pypi/v/ikaris.svg)](https://pypi.org/project/ikaris/)
[![Total Download](https://img.shields.io/pypi/dm/ikaris)]
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

**Ikaris** is an open-source CLI tool for verifying the security of machine learning models from [Hugging Face](https://huggingface.co) and PyPI(https://pypi.org/). Ikaris performs multi-layer checks to help users assess risks before deploying models and package in production environments.

## ✨ Main Feature

Ikaris performs model verification based on three methods:

🔍 **Source Verification**

Identifies the model/package creator and publisher, as well as basic metadata.

📁 **File and Folder Safety Review**

Review the structure and contents of the model repository for suspicious or non-standard content.

📄 **Model Card and Metadata Review** 

Validate model documentation and metadata.

🧩 **Dependencies Review**

Check package dependency

🛡️ **Vulnerability Review**

Check package vulnerability

## 📦 Installation

Make sure you are using Python `>=3.8`, then install Ikaris via pip:

Using `pip`:
```bash
pip install ikaris
```

## 🚀 Usage

Basic usage example for checking models:
```bash
ikaris check hf-model tensorblock/Llama-3-ELYZA-JP-8B-GGUF
```
Another example :
```bash
ikaris check package pandas
```

### Output Sample
```bash
----------------------------------------
Source Verification
----------------------------------------
INFO: Source: https://huggingface.co/tensorblock/Llama-3-ELYZA-JP-8B-GGUF
INFO: Creator: tensorblock
WARNING: Model Publisher: Unknown
INFO: Tags: [...]
INFO: Downloads: 196
----------------------------------------
File & Folder Review
----------------------------------------
INFO: README.md is Safe
... (file lainnya)
----------------------------------------
Model Card Review
----------------------------------------
INFO: This model contains clear documentation.
INFO: This model contains clear metadata.

Summary: 20 Info, 1 Warning, 0 Critical
```

```bash
----------------------------------------
Source Verification
----------------------------------------
INFO: Source: https://pypi.org/project/imbalanced-learn/
INFO: Version: 0.13.0
WARNING: License: Unknown
INFO: Open Source: Yes
INFO: Project URL: https://github.com/scikit-learn-contrib/imbalanced-learn
INFO: Active Developers: 30
INFO: Last Maintenance (GitHub Commit): 2025-06-06 18:56:11
----------------------------------------
Dependencies Verification
----------------------------------------
INFO: Dependency found: imbalanced-learn (0.13.0)
INFO: Dependency found: joblib (1.5.1)
INFO: Dependency found: numpy (2.3.1)
INFO: Dependency found: scikit-learn (1.6.1)
INFO: Dependency found: scipy (1.15.3)
INFO: Dependency found: sklearn-compat (0.1.3)
INFO: Dependency found: threadpoolctl (3.6.0)
----------------------------------------
OSV Vulnerability Verification
----------------------------------------
INFO: No known vulnerabilities found in 'imbalanced-learn==latest'.

Summary: 15 Info, 1 Warning, 0 Critical
```

## 📁 Project Structure

```bash
Ikaris 
├── checker 
│   ├── __init__.py 
|   ├── dependencies_verification.py 
│   ├── file_verification.py 
│   ├── model_card_verification.py 
|   ├── source_verification.py
│   └── vulnerability_verification.py
├── helpers 
│   ├── __init__.py 
│   └── logging.py
├── __init__.py
└── main.py
```

## 🔧 Prerequisite

- `Python >= 3.8`
- `huggingface_hub`
- `colorama`
- `requests`

## 📝 License

Distribution under license: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## 👤 Contributor

- [Haydar Miezanie Abdul Jamil](https://www.linkedin.com/in/haydar-miezanie-abdul-jamil-916302162/) (haydarsaja@gmail.com)

## ⚠️ Disclaimer

Ikaris is not a substitute for a full security audit. Use Ikaris results as an initial analysis, and combine them with manual checks for model usage on sensitive production systems.