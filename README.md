# pyltp-books
人物篇幅分析，故事发生地分析，人物互动情况分析
![结构](https://github.com/gugug/pyltp-books/blob/master/PrtScr/system-structure.png) <br />

## 主要人物（地点）篇幅统计策略
本文对小说主要人物（地点）的衡量指标有两个，第一个是在文中出现的次数（词频），第二这是在文中的覆盖范围（文档频率）。基于这二者，篇幅占比的统计策略如下：
![主要人物地点](https://github.com/gugug/pyltp-books/blob/master/PrtScr/main-peo-local.png) <br />
步骤：
1. 提取小说每一章节，进行命名实体识别
2. 抽取其中的人名（地名），并统计每个章节人名（地名）频率
3. 抽取词频最高的前三个人名（地名）作为章节主要人物
4. 对所有章节的主要人物进行文档频率统计（章节数）
5. 基于文档频率，构建篇幅占比图

## 人物互动关系识别策略
基于依存句法树进行人物互动关系的识别，主要提取特定句子成分（主谓宾），策略如下：
![人物工作关系](https://github.com/gugug/pyltp-books/blob/master/PrtScr/relation-action.png) <br/>
步骤：
1. 对章节正文进行断句
2. 对句子进行分词，词性标注以及依存句法分析
3. 基于SBV，找出主谓关系
4. 基于VOB， 找出动宾关系
5. 基于COO，找出主语和宾语的并列词
6. 将对应的主谓关系和动宾关系整合为主谓宾结构，并构造互动关系图