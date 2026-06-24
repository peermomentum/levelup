# Security

Do not commit secrets to this repository.

This backup intentionally excludes secret values and live runtime state. Before making this repository public or sharing it, review changes with:

```bash
git status --short
git diff --cached
```

If a token was ever pasted into chat or committed by mistake, revoke it immediately in GitHub and generate a new fine-grained token scoped only to this repository.
