<div align="center">
<div align="center">
 <img alt="ASTRA" height="auto" src="../../images/cover2.png">
</div>

<a href="../../README.md"><img alt="README in English" src="https://img.shields.io/badge/English-lightgrey"></a>
<a href=".README-CN.md"><img alt="简体中文" src="https://img.shields.io/badge/简体中文-lightgrey"></a>
<a href=".README-FR.md"><img alt="Français" src="https://img.shields.io/badge/French-lightgrey"></a>


<a href="">
<span>植物工厂自动运营</span>
</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="">
<span>多智能体协同操作</span>
</a>

</div>

* **愿景**：利用植物工厂技术，让人类可以不再看天吃饭，在任何地方包括外太空都可以全年无休地享受，零无污染、无农药的果蔬。

* **挑战**：虽然植物工厂可以基于物联网技术采集许多数据，但是数据的分析和处理过程仍需工程师大量参与，然而其中的许多工作都十分具有重复性。

* **解决方案**：通过大语言模型（LLM）驱动的Multi-Agent自动运营工作流，部署了三个 AI 代理：

    * AI 数据分析师：利用 qwen-max 模型分析历史数据，为 AI 助理农艺师提供分析结果。
    * AI 助理农艺师：结合 RAG 文档和 AI 数据分析师的结果，进行种植建议。使用 moonshot-v1-128k 模型处理长文本。
    * AI 执行工程师：与人类工程师合作，根据分析结果调整植物工厂设备参数。

<div align="center">
<img  alt="植物工厂数智可视化" src="../../images/gif_data.gif">
</div>

# 技术思路

这次项目希望重点测试的是LLM的：  
1. 长文本和数据的处理/分析能力：即它自身的数理理解和使用给定工具的能力
2. 将文本转换成有参考性种植策略的能力：即它了解情况后它如何从知识库提取合适的专业文档，并给出科学的建议。
3. 将策略转换成实际的设备控制参数：具体来说就是有了种植策略后，LLM能不能通过生成具体数值去调控设备。

# 工作流结构

以上三个测试点分别由上下串联的三个AI Agent来代表，之所以不直接放一个完整的Agent来完成，是因为想确保LLM的文本生成范围尽量可控，让一个Agent做一个很具体的事情。

1. **AI 数据分析师**：负责对历史数据进行分析，统计不同种植参数的情况。然后将分析结果传送给 AI 助理农艺师。这里选择调用qwen-max来解析pandas dataframe。

<div align="center">
<img  alt="AI数据分析师" src="../../images/gif_ai_analyst.gif">
</div>

2. **AI 助理农艺师**：其职责是针对人类工程师希望解决的问题，先用标签缩小 RAG 文档的范围，从选定的知识文档中提炼知识，并结合前面的分析结果，对下一步的种植进行浅层分析和建议。为了处理大量内容，这里采用了 moonshot-v1-128k 模型进行长文本缓存工作。
<div align="center">
<img  alt="AI助理农艺师" src="../../images/gif_ai_expert.gif">
</div>

3. **AI 执行工程师**：负责首先根据前面的累积分析更新判断植物的最佳生长状况。当人类工程师批准方案后，执行植物工厂设备参数的调整和控制操作。

<div align="center">
<img  alt="AI执行工程师" src="../../images/gif_ai_engineer.gif">
</div>


**扬长避短**：通过上述工作流程，我们解放了人类工程师的双手，使他们能够将精力集中在判断上。同时，利用专业的多代理种植管理工作流，发挥了 LLM 的长文本处理和总结能力，并利用定制规则和 Moonshot 上下文缓存能力的 RAG 技术来抑制 LLM 的幻觉现象。

<div align="center">
<img  alt="设备控制面板" src="../../images/gif_device_control.gif">
</div>

# AdventureX期间项目启动所学新工具

**LLM大模型**

* Moonshot 上下文长文本缓存
* 通义千问数理统计分析

**RAG检索**

* 【原创】解决问题导向范围可控RAG

**前端&部署**

* Zeabur
* Gamma

**2D 设计**
- Midjourney
- Light Year AI
 
**3D 设计**
- Tripo AI
- HyperHuman
