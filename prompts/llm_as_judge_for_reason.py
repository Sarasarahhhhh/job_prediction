# ============================================================================
# FACTUALITY JUDGE PROMPT
# ============================================================================

FACTUALITY_JUDGE_PROMPT = """You are an expert judge evaluating the FACTUAL ACCURACY of career reasoning.

**Career History (JSON format):**
```json
{education_and_career_history_text}
```

**Reasoning Text:**
{reasoning}

---

Please evaluate this reasoning along three dimensions (**1–5 scale**).  
For each dimension, briefly describe your step-by-step reasoning.

---

### 1. Factuality (1–5)
**Definition:**  
Checks whether the factual claims in the reasoning are supported by the given career history.  
All mentioned education, company, job title, dates, or skills should be traceable to and consistent with the provided history.

**Evaluation Steps:**  
1. Identify each factual claim in the reasoning.
2. Mark each as *Supported* (found and accurate in history) or *Unsupported* (fabricated, wrong, or inconsistent).  
3. Judge the overall factual accuracy level:  

| Score | Description |
|--------|--------------|
| 5 | All statements accurate and well-grounded |
| 4 | Mostly accurate; 1–2 minor inaccuracies |
| 3 | Several factural inaccuracies |
| 2 | Many factual mistakes |
| 1 | Mostly fabricated or irrelevant to history |

Provide a short justification mentioning which parts were correct or incorrect.

**Output Format (JSON only, no extra text):**
```json
{{
  "factuality_score": <1-5>,
  "factuality_justification": "<List specific errors found or confirm all facts are accurate>",
  "error_count": <number>,
  "errors_identified": ["<error 1>", "<error 2>", ...]
}}
```"""

# ============================================================================
# COHERENCE JUDGE PROMPT
# ============================================================================

COHERENCE_JUDGE_PROMPT = """You are an expert judge evaluating the LOGICAL COHERENCE of career reasoning text.

**Reasoning Text:**
{reasoning}

---

**Your Task:** Evaluate the coherence of this reasoning on a 1-5 scale.

**Definition:**  
Evaluates whether the reasoning forms a clear and logically consistent narrative according to the user history.  
A coherent reasoning should have correct temporal flow and causal logic.

**Evaluation Steps:**  
1. Check whether the reasoning follows a logical timeline.  
2. Assess whether the cause-effect links are consistent and non-contradictory.  
3. Rate based on clarity and structure:  

| Score | Description |
|--------|--------------|
| 5 | Fully logical, well-organized, clear progression |
| 4 | Mostly logical, minor inconsistencies |
| 3 | Partially logical but lacks smooth consistency |
| 2 | Disjointed with noticeable logical gaps or unclear reasoning steps |
| 1 | Illogical, inconsistent, or confusing narrative |

Briefly explain your reasoning, citing specific coherence strengths or problems.

**Output Format (JSON only, no extra text):**
```json
{{
  "coherence_score": <1-5>,
  "coherence_justification": "<Explain logical flow issues or strengths>",
  "temporal_order": "<good/problematic/broken>",
  "logical_issues_count": <number>
}}
```"""

# ============================================================================
# UTILITY JUDGE PROMPT
# ============================================================================

UTILITY_JUDGE_PROMPT = """You are an expert judge evaluating the UTILITY of career reasoning.

**Ground-Truth Next Occupation:**
{ground_truth_occupation}

**Reasoning Text:**
{reasoning}

---

**Your Task:** Evaluate how well this reasoning supports the transition to the ground-truth occupation (1-5 scale).

**Definition:**  
Measures how effectively the reasoning supports the **ground-truth next occupation** —  
It considers whether the reasoning provides relevant evidence and contributes directly to justifying the ground-truth next occupation.

**Evaluation Steps:**  
1. Identify concrete justifications (education, career growth, salary, etc.).  
2. Check whether these directly relate to the next occupation.  
3. Assign score based on relevance and support strength:  

| Score | Description |
|--------|--------------|
| 5 | Strongly and clearly justifies the next occupation |
| 4 | Mostly relevant, provides good but incomplete justification |
| 3 | Some relevance but vague or incomplete |
| 2 | Weak justification with little connection |
| 1 | No meaningful relation to next occupation |

Briefly explain what evidence supports or weakens the reasoning’s utility.

**Output Format (JSON only, no extra text):**
```json
{{
  "utility_score": <1-5>,
  "utility_justification": "<Explain how well reasoning supports the occupation>",
  "relevance_level": "<strong/moderate/weak/none>",
  "occupation_match": "<reasoning clearly supports this occupation / reasoning supports different occupation>"
}}
```"""