# Desktop Package

The desktop app packages the web UI with an Electron shell. Desktop changes can
touch `apps/dsa-desktop/`, the web build in `apps/dsa-web/`, and release scripts.

## Build Order

Build the web app first:

```bash
cd apps/dsa-web
npm ci
npm run build
```

Then build the desktop app:

```bash
cd ../dsa-desktop
npm install
npm run build
```

The desktop package consumes the web build output, so a desktop-only build is not
enough after frontend changes.

## Local Development

Use the scripts under `scripts/` for platform-specific packaging helpers. Keep
paths configurable and avoid hard-coded local user directories.

## Release Notes

When packaging behavior changes, document:

- affected operating systems
- build artifact names and paths
- required signing or notarization steps
- whether the web build output changed
- any manual smoke tests performed

## Verification

Run:

```bash
cd apps/dsa-web && npm run build
cd ../dsa-desktop && npm run build
```

If a platform-specific build cannot run locally, state which artifact was
verified and which platform check remains unverified.
