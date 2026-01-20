"""Prompt templates for VLM interaction."""


def build_verification_prompt(task_description: str) -> str:
    """
    Build a prompt for image-task verification.

    Args:
        task_description: Detailed description of the task

    Returns:
        Formatted prompt string for VLM
    """
    prompt = f"""任务描述：{task_description}

请仔细观察图像，判断图像中**是否出现了**任务描述中提到的情况或内容。

判断标准：
1. 如果图像中明确出现了任务描述中的情况，返回 match = true
2. 如果图像中没有出现任务描述中的情况，返回 match = false
3. 确保判断结果与实际观察到的内容一致

请以JSON格式回答，包含以下字段：
- match: 布尔值，true表示图像中出现了描述的情况，false表示未出现
- reason: 字符串，详细说明你观察到的内容和判断依据"""

    return prompt
