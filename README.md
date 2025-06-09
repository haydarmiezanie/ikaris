# Ikaris

[![PyPI version](https://img.shields.io/pypi/v/ikaris.svg)](https://pypi.org/project/ikaris/)
[![Python version](https://img.shields.io/pypi/pyversions/ikaris)](https://pypi.org/project/ikaris/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

**Ikaris** is an open-source CLI tool for verifying the security of machine learning models from [Hugging Face](https://huggingface.co). Ikaris performs multi-layer checks to help users assess risks before deploying models in production environments.

## ✨ Main Feature

Ikaris performs model verification based on three methods:

🔍 **Source Verification**

Identifies the model creator and publisher, as well as basic metadata.

📁 **File and Folder Safety Review**

Review the structure and contents of the model repository for suspicious or non-standard content.

📄 **Model Card and Metadata Review** 

Validate model documentation and metadata.

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
ikaris check hf-model tencent/HunyuanVideo-Avatar
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

## 📁 Project Structure

```bash
Ikaris 
├── checker 
│   ├── __init__.py 
│   ├── file_verification.py 
│   ├── model_card_verification.py 
│   └── source_verification.py
├── helpers 
│   ├── __init__.py 
│   └── logging.py
├── __init__.py
└── main.py
```

## 🔧 Prerequisite

- `Python >= 3.8`
- `huggingface_hub >= 0.32.4`
- `colorama >= 0.4.6`

## 📝 License

Distribution under license: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## 👤 Contributor

- [Haydar Miezanie Abdul Jamil](https://www.linkedin.com/in/haydar-miezanie-abdul-jamil-916302162/) (haydarsaja@gmail.com)

## ⚠️ Disclaimer

Ikaris is not a substitute for a full security audit. Use Ikaris results as an initial analysis, and combine them with manual checks for model usage on sensitive production systems.