# Security policy

## Reporting a vulnerability

Report security vulnerabilities privately, through the "Report a vulnerability"
form on this repository's Security tab (GitHub private vulnerability reporting)
or by email to **security@vaif.studio**. Do not open a GitHub issue, pull
request or discussion for a vulnerability, and do not disclose it publicly until
a fix is available.

This address also accepts reports about the VAIF Studio API and platform.

## What to include

- The affected package version (`python -c "import vaifstudio; print(vaifstudio.__version__)"`),
  your Python version and your operating system.
- A description of the vulnerability and the impact you believe it has.
- Steps to reproduce it: a minimal code sample or proof of concept.
- The `request_id` of any failing API call, if you have one.
- How you would like to be credited, if at all.

Do not include live API keys, access tokens, passwords or customer data. Redact
them, or use a project you created for testing.

## What happens next

We acknowledge your report within 2 business days and send an initial
assessment within 5 business days. We then investigate it and keep you informed
of our progress. If we confirm the vulnerability, we prepare a fix, release it,
and describe it in the [changelog](CHANGELOG.md). We coordinate the disclosure
date with you and, if you agree, credit you in the changelog.

## Supported versions

| Version | Supported |
| --- | --- |
| 1.x | Yes |
| `vaif-client` 0.x (the previous package) | No |

Security fixes are released for the latest 1.x version.
