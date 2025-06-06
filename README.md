# Ikaris - Open-Source Model Safety Checker

A security validation tool that examines whether an open-source AI model can be safely
executed in your environment. Ikaris performs comprehensive safety checks including:

- Malware/payload detection in model files
- Suspicious code patterns
- Known vulnerability scanning
- Resource usage analysis
- Permission/access requirements
- Compatibility with your system configuration

The tool generates a detailed safety report with risk assessment and recommendations
before you deploy the model in production environments.

Examples:
```bash
ikaris --model_id author/model
```
Notes:
- Supported formats: Hugging Face only (for now)
- Run with admin privileges for full system impact analysis

Security Disclaimer:
Always verify checksums from official sources. Ikaris provides heuristic analysis
but cannot guarantee complete safety. Report issues at: haydarsaja@gmail.com