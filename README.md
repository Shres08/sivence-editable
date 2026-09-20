# Sivence editable website

This repository is the editable copy of Sivence. The current live website remains separate until this copy is approved.

## Edit content

1. Open [Pages CMS](https://app.pagescms.org/) and sign in with GitHub.
2. Select this repository.
3. Use **Homepage, About & Contact** for the principal copy and **Work projects** for project cards.
4. Use the Media area to replace images, videos or documents.
5. Save. Each save creates a versioned GitHub commit and triggers the connected site preview.

## Preview locally

Run a local static server from the repository root. For example:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Publishing

The repository is ready for a static host such as Cloudflare Pages. No build command is required; publish the repository root.

Do not point `sivencestudio.com` at this copy until the preview has been reviewed and approved.
