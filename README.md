# Sivence Studio

Production source for https://sivencestudio.com. Human psychology artwork and customer-signal interactions are developed on `human-algorithm`.

## Local preview

Run `python3 restore_large_media.py` once after cloning, then `python3 -m http.server 8080 --directory dist` and open http://localhost:8080/. No dependencies or build step are required. `.openai/hosting.json` declares `dist` as the deployed output.

## Editing

`dist/index.html` is the homepage; `homepage.html` is its authoring template. Update both when editing homepage markup. New interaction code is isolated in `dist/assets/human-algorithm.js` and `human-algorithm.css`. The original sculpture lives in `dist/lab/spatial-studio/index.html` and is embedded in Customer Signals. All portfolio pages and media remain in `dist`. Root-level files from the older editable prototype are retained for reference and are not deployed.

## Validation

`python3 verify_portfolio.py` checks all canonical routes, navigation, assets, metadata and media. `python3 verify_human_algorithm.py` checks preserved homepage copy, section order, the relocated sculpture, accessibility and source integrity. Use `qa/responsive.html` temporarily inside `dist` to check 375, 390, 768 and 1440 pixel viewports; remove it before publication.

## Interaction behaviour

Nine glass fragments assemble once on arrival. Mouse, touch and keyboard reveal individual insights. Sounds are silent until explicitly enabled and synthesized locally through Web Audio. Motion respects the operating system preference and the pause control. The image fallback remains visible when scripting is disabled. The original sculpture is loaded when its section enters view, including its non-WebGL fallback.

The large original catalogue is stored as lossless binary parts in the GitHub branch to fit the connector transfer limit. `restore_large_media.py` reassembles it and verifies its SHA-256 before use. The live website serves the unchanged, complete PDF.
