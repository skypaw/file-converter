# File converter POC

### Additional features:

- Security and Content Filtering
- Batch processing and progress tracking in pipeline

### Filter:

Works based on looking for keywords in the string and masking rest of the string with `*`.
Security check is based on argument parser and not allowing accessing directory above project and path traversal.

### Batch processing:

Using GitHub Actions and matrix feature for concurrent run. Creating new PR with files in "input" directory will
automatically process and save files as an artifact.