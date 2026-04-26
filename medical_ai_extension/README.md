# 面向医疗 AI 应用的接口自动化测试扩展

本目录是在原有 `Python + Pytest` 通用接口自动化测试框架基础上，结合智慧医疗与疾病预测模型服务场景补充的场景化扩展内容。

> 说明：该扩展用于个人学习、简历项目展示与面试讲解，不代表已经接入真实医院生产系统。设计目标是把通用接口测试框架迁移到医疗 AI 模型服务、医疗数据处理接口和自动化回归测试场景中。

## 1. 扩展目标

- 将通用接口测试框架映射到医疗 AI 应用场景；
- 使用 YAML 管理疾病预测 API 的测试数据；
- 对模型接口返回值进行多维度断言，而不是只校验状态码；
- 设计医疗多源数据在测试前置准备、结果校验、数据清理中的使用方案；
- 为 Jenkins CI/CD 中的模型服务回归测试提供基础示例。

## 2. 目录结构

```text
medical_ai_extension/
├── README.md
├── resume_project.md
├── config/
│   └── medical_env.yaml
├── testcases/
│   └── disease_predict_cases.yaml
├── utils/
│   ├── __init__.py
│   └── medical_assertions.py
├── tests/
│   ├── __init__.py
│   └── test_disease_predict_api.py
└── docs/
    └── multi_datasource_design.md
```

## 3. 核心测试场景

以疾病风险预测接口 `/api/v1/predict/disease-risk` 为例，测试用例覆盖：

1. 正常患者数据输入；
2. 缺失必填字段；
3. 字段类型错误；
4. 年龄、检验指标等边界值；
5. 模型返回结构完整性；
6. 预测概率范围校验；
7. 风险等级枚举值校验；
8. 模型版本号和 request_id 可追溯性校验。

## 4. 和原框架的关系

原框架提供通用接口自动化测试能力，例如：

- 多环境配置；
- YAML 数据驱动；
- 统一请求封装；
- Pytest 用例组织；
- 测试报告生成；
- Jenkins CI/CD 集成。

本扩展不推翻原框架，而是在其基础上补充医疗 AI 场景相关的测试数据、断言规则和项目说明，使简历项目表达更贴近 AI 应用工程师岗位。

## 5. 建议运行方式

如果本地已经安装 `pytest`、`requests`、`PyYAML`，可以在项目根目录执行：

```bash
pytest medical_ai_extension/tests -q
```

由于示例接口地址默认指向本地模拟服务，若没有启动对应后端服务，接口调用类用例会失败。面试展示时重点说明该目录体现的是医疗 AI 场景的测试设计、YAML 数据组织和断言机制。
