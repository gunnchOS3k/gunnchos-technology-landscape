# Negative fixtures — accessibility / visual mismatch

These fixtures document failure modes validators must catch.

## figure_claims_arrows_without_arrows.svg

Accessibility text claims arrows exist, but the SVG contains only rectangles/text.

## figure_claims_dashed_without_dash.svg

Accessibility text claims a dashed optional branch, but no `stroke-dasharray` is present.

## figure_claims_stacked_bar_without_bar.svg

Accessibility text claims a stacked latency bar, but only a text list is present.

## figure_claims_exploded_but_list_only.svg

Accessibility text claims an exploded device view, but the asset is a vertical text checklist.
