"""
v1：制度问答助手——配置剥离版本

相比 v0 的变化（仅一处）：
  - 模型 endpoint / api_key / model_name 不再写死在代码里
  - 改为通过 .env 文件 + 环境变量传入
  - 同一份 policy_qa.py 现在可以在不修改代码的前提下切换 DeepSeek / Ollama / OpenAI

架构原则：配置三层
  1. 代码默认值（兜底，比如 base_url 给一个常用默认）
  2. 配置文件（.env，本地开发用，不进代码库）
  3. 环境变量（部署环境注入，最高优先级——会覆盖 .env）

运行方式：
  cd scripts/v1_配置剥离
  cp .env.example .env       # 第一次跑，按需改 .env 里的值
  python policy_qa.py
"""

from agently import Agently, TriggerFlow, TriggerFlowEventData
from congfig.congfig import init_agently

init_agently(Agently)


# ── 制度文档 ───────────────────────────────────────────────────────────────
POLICY_DOC = """
【出差管理制度 · 智创科技】
1. 出差申请须提前 3 个工作日提交。
2. 补贴标准：省内 100 元/天，省外 200 元/天，境外按实际票据报销。
3. 出差申请须直属主管审批后方可出行。
4. 行程变更须在变更后 24 小时内更新申请单。
"""


# ── 流程定义（chunk 函数内 prompt 仍写死——v2 会处理这个）───────────────────
async def analyze_question(data: TriggerFlowEventData):
    question = data.value
    data.set_runtime_data("question", question)

    agent = Agently.create_agent()
    analysis = (
        agent
        .system("你是企业制度助理，负责分析员工问题的类型。")
        .info({"制度范围": "出差申请、补贴标准、审批流程、行程变更。"})
        .input(f"分析以下问题：{question}")
        .output({
            "question_type":   (str,  "policy / general / unclear"),
            "needs_more_info": (bool, "是否需要追问"),
            "missing_info":    (str,  "缺少的信息；不需要则留空"),
        })
        .start(ensure_keys=["question_type", "needs_more_info"])
    )
    data.set_runtime_data("analysis", analysis)
    return analysis


async def ask_for_more_info(data: TriggerFlowEventData):
    missing = data.value.get("missing_info", "更多信息")
    return f"为了准确回答，需要补充以下信息：{missing}"


async def answer_policy_question(data: TriggerFlowEventData):
    question = data.get_runtime_data("question")
    agent = Agently.create_agent()
    return (
        agent
        .system("你是公司制度助理，依据制度文档回答员工问题；制度未明确规定时请告知咨询 HR。")
        .info({"出差管理制度": POLICY_DOC})
        .input(question)
        .get_text()
    )


async def answer_general_question(data: TriggerFlowEventData):
    question = data.get_runtime_data("question")
    agent = Agently.create_agent()
    return agent.system("你是企业内部助理。").input(question).get_text()


async def format_final_answer(data: TriggerFlowEventData):
    answer = data.value
    analysis = data.get_runtime_data("analysis") or {}
    label = {
        "policy":  "[制度依据]",
        "general": "[通用回答]",
        "unclear": "[追问]",
    }.get(str(analysis.get("question_type")), "[回答]")
    formatted = f"{label}\n\n{answer}"
    data.set_runtime_data("final_answer", formatted)
    return formatted


flow = TriggerFlow(name="policy-qa-v1")
(
    flow
    .to(analyze_question)
    .if_condition(lambda data: data.value.get("needs_more_info", False))
    .to(ask_for_more_info)
    .elif_condition(lambda data: data.value.get("question_type") == "policy")
    .to(answer_policy_question)
    .else_condition()
    .to(answer_general_question)
    .end_condition()
    .to(format_final_answer)
)


if __name__ == "__main__":
    test_questions = [
        "我后天要去上海出差，补贴是多少？",
        "公司食堂几点开门？",
        "我想出差",
    ]
    for question in test_questions:
        print("=" * 55)
        print(f"问：{question}")
        print("-" * 55)
        state = flow.start(question)
        print(state["final_answer"])
        print()
