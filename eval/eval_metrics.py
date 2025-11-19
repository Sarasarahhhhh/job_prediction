#!/usr/bin/env python3
"""
evaluation_metrics.py

Utility functions to compute:
- Exact Match Accuracy (AccEM)
- Semantic Accuracy (AccRM, a related-occupation match score)

Assumed data format per sample:
{
    "ground_truth_occupation": {
        "onet_title": "<GROUND_TRUTH_TITLE>",
        ...
    },
    "predictions": {
        "<predictor_name>": "<PREDICTED_TITLE>",
        ...
    }
}

related_titles format (same as in your original script):
{
    "<GROUND_TRUTH_TITLE>": {
        "1": "<RELATED_TITLE_RANK2>",
        "2": "<RELATED_TITLE_RANK3>",
        ...
    },
    ...
}
"""

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


def _get_predicted_occupation(item: Dict[str, Any], predictor: str) -> str:
    """
    Safely extract predicted occupation title for a given predictor.
    Returns "None" if predictor key is missing.
    """
    if "predictions" not in item:
        return "None"
    return item["predictions"].get(predictor, "None")


def _compute_rm_score(
    predicted_occupation: str,
    gt_title: str,
    related_titles: Optional[Dict[str, Dict[str, str]]] = None,
) -> float:
    """
    Compute Related Occupation Match score (rm_score) for a single sample.

    - If predicted_occupation == gt_title => rm_score = 1.0
    - Else if predicted_occupation matches a related title at rank (k+1)
      (where related_titles[gt_title]["1"] is rank 2, etc.),
      then rm_score = 1.0 / (k + 1)
    - Else rm_score = 0.0
    """
    if not related_titles or gt_title not in related_titles:
        # No related info, fall back to exact match only
        return 1.0 if predicted_occupation == gt_title else 0.0

    # Exact match (rank 1)
    if predicted_occupation == gt_title:
        return 1.0

    # Related titles: keys are "1", "2", ... where "1" -> rank 2, etc.
    related_list = related_titles[gt_title]
    for rank_str, related_title in related_list.items():
        if predicted_occupation == related_title:
            k = int(rank_str) + 1  # ground truth is rank 1
            return 1.0 / k

    return 0.0


def _calculate_accuracy(correct: int, total: int) -> float:
    """
    Calculate accuracy in percentage.
    """
    return (correct / total * 100.0) if total > 0 else 0.0


def compute_em_and_semantic_accuracy(
    data: List[Dict[str, Any]],
    predictor: str,
    related_titles: Optional[Dict[str, Dict[str, str]]] = None,
) -> Dict[str, float]:
    """
    Compute Exact Match Accuracy (AccEM) and Semantic Accuracy (AccRM).

    Args:
        data: list of samples.
        predictor: key in item["predictions"] to use.
        related_titles: mapping for semantic similarity (see module docstring).

    Returns:
        {
            "AccEM": <float, percentage>,
            "AccRM": <float, percentage>,
            "total": <int, number of evaluated samples>
        }
    """
    stats = defaultdict(int)
    rm_sum = 0.0

    for item in data:
        # Ground-truth title
        gt_title = item["ground_truth_occupation"]["onet_title"]

        # Predicted title
        predicted_occupation = _get_predicted_occupation(item, predictor)

        # Exact match
        is_correct = predicted_occupation == gt_title
        stats["total"] += 1
        if is_correct:
            stats["correct"] += 1

        # Semantic score (AccRM numerator)
        rm_score = _compute_rm_score(predicted_occupation, gt_title, related_titles)
        rm_sum += rm_score

    total = stats["total"]
    acc_em = _calculate_accuracy(stats["correct"], total)
    acc_rm = (rm_sum / total * 100.0) if total > 0 else 0.0

    return {
        "AccEM": acc_em,
        "AccRM": acc_rm,
        "total": total,
    }
