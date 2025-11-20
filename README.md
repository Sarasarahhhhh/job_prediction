# On Reasoning Behind Next Occupation Recommendation
This repository contains code and configurations for training and evaluating language models to predict career trajectories based on education and work history. The dataset used for training and evaluation is proprietary and can be made available for peer review upon request.

## Overview

The project uses large language models (LLMs) to analyze chronological career histories and predict the next logical occupation transition. Models are trained using official O*NET-SOC 2019 occupation titles.

## Directory Structure

```
occp/
├── eval/                  # Evaluation metrics
│   └── eval_metrics.py   # AccEM and AccRM computation
├── prompts/              # Prompt templates
│   ├── llm_as_judge_for_reason.py
│   ├── prompt_for_joint_model_option.py
│   ├── prompt_for_two_model_option.py
│   └── prompt_for_oracle_reason_generation.py
└── training_scripts/     # Model training configurations
    ├── qwen3_8b_full_occp_sft_method2_joint.yaml
    ├── qwen3_8b_full_occp_sft_method2_occupation.yaml
    ├── qwen3_8b_full_occp_sft_method2_reasoning.yaml
    ├── qwen3_8b_full_occp_dpo_method2_joint.yaml
    └── qwen3_8b_full_occp_dpo_method2_reasoning.yaml
```

## Components

### Evaluation (`eval/`)

- **eval_metrics.py**: Computes two key metrics:
  - **AccEM** (Exact Match Accuracy): Percentage of exact occupation title matches
  - **AccRM** (Related Match Accuracy): Semantic accuracy considering related occupations with ranked similarity scoring

### Prompts (`prompts/`)

Four prompt templates for different use cases:
- **Joint Model**: Single model generates reasoning and occupation prediction together
- **Two Model**: Separate models for reasoning generation and occupation prediction
- **Oracle Reasoning**: Generate ground-truth reasoning for training
- **LLM as Judge**: Evaluate quality of generated reasoning

### Training Scripts (`training_scripts/`)

YAML configurations for fine-tuning Qwen3-8B models:
- **SFT** (Supervised Fine-Tuning): Joint, occupation-only, and reasoning-only variants
- **DPO** (Direct Preference Optimization): Joint and reasoning variants

All configurations use:
- Full parameter fine-tuning
- DeepSpeed ZeRO-3 optimization
- Weights & Biases logging

## Training Approaches

1. **Joint Training**: Model learns to generate reasoning and predict occupation simultaneously
2. **Separate Training**: Independent models for reasoning and occupation prediction
3. **DPO Fine-tuning**: Preference-based optimization for improved reasoning quality

## Usage

### Evaluation Example

```python
from eval.eval_metrics import compute_em_and_semantic_accuracy

metrics = compute_em_and_semantic_accuracy(
    data=evaluation_data,
    predictor="model_name",
    related_titles=related_occupations_dict
)
print(f"AccEM: {metrics['AccEM']:.2f}%")
print(f"AccRM: {metrics['AccRM']:.2f}%")
```

### Training

Use the provided YAML configurations with your training framework:

```bash
# Example for SFT joint training
llamafactory-cli train training_scripts/qwen3_8b_full_occp_sft_method2_joint.yaml
```

## Data Format

Expected input format per sample:
```json
{
    "ground_truth_occupation": {
        "onet_title": "Data Scientists"
    },
    "predictions": {
        "model_name": "Computer and Information Research Scientists"
    }
}
```

## Model Output Format

Models generate outputs in tagged format:
```
<think>
[Step-by-step reasoning about career progression]
</think>
<answer>
[O*NET-SOC 2019 occupation title]
</answer>
```

