## 作业要求

1. 参考 《GitHubSentinel 高级功能与生产级发布》 章节，在 Language Mentor v0.4 基础上实现：
    - 新增单元测试（覆盖率 80%）与自动化测试脚本；
    - 新增 Dockerfile，实现镜像构建与容器化部署；
2. （可选）将 LanguageMentor 发布到 HuggingFace Space，便于学术交流和分享。

## 作业提交

### 作业一

测试用例覆盖率：

```
--------- coverage: platform darwin, python 3.10.15-final-0 ----------
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
src/agents/__init__.py                 0      0   100%
src/agents/agent_base.py              41      1    98%   43
src/agents/conversation_agent.py       7      0   100%
src/agents/scenario_agent.py          20      0   100%
src/agents/session_history.py          6      0   100%
src/agents/vocab_agent.py             14      0   100%
src/main.py                           13     13     0%   1-17
src/utils/logger.py                   10      0   100%
----------------------------------------------------------------
TOTAL                                111     14    87%
```

相关代码：
- [测试代码路径跳转 tests/](../tests)
- [Dockerfile 文件跳转 <----](../Dockerfile)

### 作业二（可选）

TODO：：


