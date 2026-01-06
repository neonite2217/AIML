# BUILD_LOG.md

## What Was Built

A multimodal AI pipeline using OpenAI's CLIP (`clip-vit-base-patch32`) via HuggingFace `transformers`. The script:

1. Loads a local image (creates a 224×224 red square if none exists)
2. Extracts a 512-dim image embedding using CLIP's vision encoder + projection head
3. Encodes 5 candidate text captions into 512-dim text embeddings using CLIP's text encoder + projection head
4. Computes cosine similarity between the image embedding and each text embedding
5. Ranks and prints captions from most to least similar

All embeddings live in the same shared CLIP vector space, enabling direct image↔text comparison.

## How to Run

Dependencies are available system-wide (`torch`, `transformers`, `Pillow`). No paid APIs used.

```bash
cd 02_Building_a_Multimodal_AI_Model_CLIP
python3 clip.py
```

To use a venv instead:
```bash
python3 -m venv venv
venv/bin/pip install torch Pillow transformers
venv/bin/python clip.py
```

## Sample Output

```
Image: dummy_image.png (a solid red square)

Candidate Captions & Cosine Similarities:
  1. [0.3186] a bright red colored image
  2. [0.2901] a photo of a red square
  3. [0.2359] a photo of a blue circle
  4. [0.1995] a green forest landscape
  5. [0.1793] a cat sitting on a couch

Top match: 'a bright red colored image'
```

CLIP correctly ranks both red-related captions at the top, with the most semantically accurate description ("bright red colored image") scoring highest.

## Key Implementation Notes

- Used `model(**inputs)` to get `image_embeds` and `text_embeds` — these are already projected to the shared 512-dim space via CLIP's linear projection heads. Calling `model.get_image_features()` / `model.get_text_features()` returned `BaseModelOutputWithPooling` (768-dim, unprojected) in this version of transformers, so the full forward pass was used instead.
- Embeddings are L2-normalized before dot product to get proper cosine similarity in [-1, 1].
- The `UNEXPECTED` keys warning (`position_ids`) in the load report is benign — it's a known artifact of how this version of transformers handles CLIP weight loading.

## Issues Encountered

| Issue | Resolution |
|---|---|
| `get_image_features()` returned `BaseModelOutputWithPooling` instead of a tensor | Used `model(**inputs).image_embeds` instead |
| Vision encoder outputs 768-dim, text encoder 512-dim | Fixed by using projected embeddings from full forward pass (both 512-dim) |
| `torch` pip install failed (network issue, 915 MB wheel) | All deps already installed system-wide; venv skipped |
