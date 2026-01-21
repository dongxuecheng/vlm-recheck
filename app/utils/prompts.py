"""Prompt templates for VLM interaction."""


def build_verification_prompt(task_description: str) -> str:
    """
    Build a prompt for image-task verification.

    Args:
        task_description: Detailed description of the task

    Returns:
        Formatted prompt string for VLM
    """
    prompt = f"""你是一名AI安全审核专家，负责审核图像内容根据特定的任务描述是否出现违章。
    任务描述：{task_description}

请仔细观察图像，判断图像中**是否出现了**任务描述中提到的违章情况或内容。

判断标准：
1. 视觉确认：根据描述，你看到了什么？
2. 逻辑比对：你看到的内容是否符合描述中的违章情况？
3. 最终结论：如果图像中明确出现了任务描述中的违章情况，返回 match = true，如果图像中没有出现任务描述中的违章情况，返回 match = false

请以JSON格式回答，包含以下字段：
- match: 布尔值，true表示图像中出现了描述的违章情况，false表示未出现
- reason: 字符串，简短说明你观察到的内容和判断依据"""

    return prompt
