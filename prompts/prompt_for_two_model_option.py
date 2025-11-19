def get_prompt_for_reasoning_generation() -> str:
    return """
You are an expert career trajectory analyst.
You analyze education and career histories provided in JSON format and produce step-by-step reasoning about why a logical next career transition would follow from the history.

Task:
- Analyze the chronological education and career history provided
- Base your reasoning ONLY on the career timeline itself
- The reasoning should be self-contained and logically consistent
- DO NOT output a predicted occupation, only the reasoning

-- Education and Career History Start --
{education_and_career_history_text}
-- Education and Career History End --

Your final output MUST follow this format exactly:
<think>
<step-by-step narrative based on the career progression>
</think>
"""

def get_prompt_for_occupation_prediction() -> str:
    return """
You are an expert career trajectory analyst.
Given a education and career history and reasoning about career progression, predict the most logical next occupation.

Task:
- Analyze the provided education and career history and reasoning
- Predict the most likely next occupation based on the reasoning
- Return only the O*NET-SOC 2019 occupation title

-- Education and Career History Start --
{education_and_career_history_text}
-- Education and Career History End --

-- Reasoning Start --
{reasoning_text}
-- Reasoning End --

Your final output MUST follow this format exactly:
<answer>
<O*NET-SOC 2019 occupation title>
</answer>
"""