# Brand artwork handoff

Use the [visual identity guide](../VISUAL-IDENTITY.md) for placement, colors, clear space, and size.

- **Master logo.** `studio-wordmark-*.svg` and `studio-mark-*.svg` contain self-contained vectors. Dark and light filenames describe the surface the artwork goes on. The wordmark PNGs have transparent backgrounds and are 1284 × 192 px.
- **Icon.** `studio-icon.svg` is the square tile master. Use the 512 px export for a profile image or art board and the 32 px export for a small app or browser icon. The rounded tile has transparent outer corners.
- **Sharing images.** `social-*.svg` are self-contained vector masters with outlined lettering. Corresponding `social-*.png` files are 1200 × 630 px on solid backgrounds. Start with [social-template.svg](social-template.svg) for live editable copy. Change the text inside the message and example groups, update the title and description, and check the fallback type at export size. The guide documents the layout and type hierarchy.
- **Type attribution.** Bricolage Grotesque by Mathieu Triay was used for the outlined artwork. The artwork files contain vector shapes. [Font source and SIL Open Font License](https://github.com/ateliertriay/bricolage)

## Sharing descriptions

Put these descriptions in the destination’s image-alt field when available. Keep the destination and the action in the post or page copy.

- **Studio.** Prompt Chaining Studio. Make the next step better. A dragon gift prompt gets the sample answer “A tiny kite.” The next prompt repeats those words and asks for a story.
- **Classroom Challenges.** Find the clue. Fix the draft. In an adapted rainy recess example, a student follows the stay-at-your-desk clue and chooses to draw a robot. The next prompt uses that correction in an announcement for the class.
- **Workbench.** Pick up where you left off. An illustrated decision workflow compares two choices, saves cost and time as criteria, then uses the same criteria in the next prompt.

## Re-export a PNG

The SVGs are the canonical artwork. Use a vector editor’s PNG export or the following ImageMagick examples from the project root. Keep alpha for the wordmark and icon. Use an opaque background for sharing images.

```sh
magick -background none -density 288 docs/brand/assets/studio-wordmark-dark.svg \
  -resize 1284x192 -strip PNG32:docs/brand/assets/studio-wordmark-dark.png

magick -background none -density 768 docs/brand/assets/studio-icon.svg \
  -resize 512x512 -strip PNG32:docs/brand/assets/studio-icon-512.png

magick docs/brand/assets/studio-icon-512.png \
  -resize 32x32 -strip PNG32:docs/brand/assets/studio-icon-32.png

magick -background none -density 144 docs/brand/assets/social-studio.svg \
  -resize 1200x630 -strip PNG24:docs/brand/assets/social-studio.png
```
