# RKLLM vs GLM 5.1 ToolSandbox 对比实验

## 1. 实验目标

在完全相同的 ToolSandbox 场景、工具定义和评分逻辑下，对比 **RKLLM**（本地部署，端侧推理）与 **GLM-5.1**（火山引擎，云端推理）的工具调用能力差异。

重点评估维度：
- 通过率（Pass Rate）
- 平均得分（Average Score）
- 工具调用准确率（Tool Call Accuracy）
- 工具参数准确率（Tool Args Accuracy）
- 平均响应延迟（Average Latency）
- 分场景类别表现
- 失败场景归因

## 2. 评分体系

每个测试用例 0-1 分：

| 维度 | 权重 | 描述 |
|------|------|------|
| 工具调用正确 | 0.5 | 所有预期工具调用均被调用且顺序正确 |
| 工具参数正确 | 0.3 | 工具参数包含预期参数的子集 |
| 响应相关 | 0.2 | 最终回复非空且相关 |

**通过标准**：得分 >= 0.5

## 3. 场景分类

| 类别 | 说明 | 测试数量 |
|------|------|----------|
| Single Tool Call - Settings | 设备开关设置（蜂窝、WiFi、定位、低电量） | 4 |
| Single Tool Call - Contacts | 联系人搜索与添加 | 4 |
| Single Tool Call - Messaging | 短信发送与搜索 | 2 |
| Single Tool Call - Search | 天气、股票、货币转换 | 3 |
| Canonicalization | 输入规范化（"$2.048k" → 2048） | 2 |
| 3 Distraction Tools | 目标工具 + 3 个干扰工具 | 2 |
| 10 Distraction Tools | 目标工具 + 10 个干扰工具 | 2 |
| All Tools Available | 全部工具可用（压力测试） | 2 |
| Multi-Tool / State Dependency | 多工具调用与状态依赖 | 2 |
| No Tool Required | 无需工具（baseline） | 1 |

共 **24 个测试用例**

## 4. 运行方法

### 4.1 环境准备

依赖（同 `pyproject.toml`）：

```bash
pip install openai requests
```

### 4.2 RKLLM 评测

使用默认配置，直接运行：

```powershell
cd "d:\Og\papers\paper\agent benchmark\ToolSandbox"
python rkllm_toolsandbox_eval.py
```

环境变量默认值：
- `MODEL_BASE_URL=http://172.31.18.39:8080/v1`
- `MODEL_API_KEY=EMPTY`
- `MODEL_NAME=rkllm-model`
- `REPORT_NAME=rkllm_toolsandbox_report.md`

### 4.3 GLM 5.1 评测

设置火山引擎环境变量后运行同一脚本：

```powershell
cd "d:\Og\papers\paper\agent benchmark\ToolSandbox"

# 设置 GLM 5.1 配置（VolcEngine Ark 兼容 OpenAI 接口）
$env:MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/coding/v3"
$env:MODEL_API_KEY="ark-5fd96c60-2295-4d2d-9f31-1c73e841022b-eef05"
$env:MODEL_NAME="glm-5.1"
$env:REPORT_NAME="glm51_toolsandbox_report.md"

python rkllm_toolsandbox_eval.py
```

输出文件：
- `rkllm_toolsandbox_report.md` — RKLLM 评测报告
- `glm51_toolsandbox_report.md` — GLM 5.1 评测报告

### 4.4 报告解读

两份报告结构完全一致，每份包含：

1. **Overview** — 关键指标总览（通过率、平均分、延迟等）
2. **Scoring Methodology** — 评分说明
3. **Results by Category** — 分类别通过率与平均分
4. **Detailed Test Results** — 24 项测试的通过/失败一览表
5. **Detailed Per-Test Analysis** — 每项测试的具体分析（含工具调用、参数、回复内容）
6. **Test Environment** — 测试环境信息

## 5. 对比结论格式

两份报告生成后，参照以下格式输出结论：

```
## RKLLM vs GLM 5.1 对比结论

### 整体指标对比

| 指标 | RKLLM | GLM 5.1 | 胜者 |
|------|-------|---------|------|
| 通过率 | XX.X% | XX.X% | RKLLM / GLM / 平局 |
| 平均得分 | X.XXX | X.XXX | ... |
| 工具调用准确率 | XX.X% | XX.X% | ... |
| 工具参数准确率 | XX.X% | XX.X% | ... |
| 平均延迟 | XXXXXms | XXXXms | ... |

### 分场景对比

| 场景类别 | RKLLM | GLM 5.1 | 胜者 |
|----------|-------|---------|------|
| Single Tool Call - Settings | X/X (XX%) | X/X (XX%) | ... |
| Single Tool Call - Contacts | X/X (XX%) | X/X (XX%) | ... |
| ... | ... | ... | ... |

### 关键发现

1. **整体表现**：...
2. **优势场景**：RKLLM 在 XXX 场景更强；GLM 5.1 在 XXX 场景更强
3. **延迟对比**：...
4. **失败模式分析**：...
   - RKLLM 主要失败于：...
   - GLM 5.1 主要失败于：...
5. **结论与建议**：...
```

## 6. 注意事项

- 两次评测使用的工具定义、测试用例、评分逻辑完全相同，确保可比性
- RKLLM 评测依赖内网环境（`http://172.31.18.39:8080`）
- GLM 5.1 依赖火山引擎外网访问，需确保网络连通性
- 每次运行之间建议间隔 1 秒，避免 API 限流
- API Key 已硬编码于脚本（如改用环境变量传递，生产环境应从配置文件或环境变量读取）