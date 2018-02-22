# SrtTranslator
Use google translation to automatically translate subtitle(*.srt file content) from english  into chinese

## README.md
字幕(.srt)文件 英译中
### 效果
#### 翻译前

    1
    00:04:50,098 --> 00:04:51,546
    Your name?
    
    2
    00:04:51,757 --> 00:04:52,905
    Julio Madiaga.
    
    3
    00:04:55,176 --> 00:04:57,139
    I was the one who came to you last week.
    
    4
    00:04:57,477 --> 00:04:59,137
    You told me to come back today.
#### 翻译后

    1
    00:04:50,098 --> 00:04:51,546
    Your name?
    你的名字？
    
    2
    00:04:51,757 --> 00:04:52,905
    Julio Madiaga.
    Julio Madiaga。
    
    3
    00:04:55,176 --> 00:04:57,139
    I was the one who came to you last week.
    我是上周来找你的那个人。
    
    4
    00:04:57,477 --> 00:04:59,137
    You told me to come back today.
    你让我今天回来。
   
### 原因
- 熟悉python
- 一天看到一个机翻字幕自称苦苦做了几小时 干点什么不好呢

### 参考
[请问如何调用谷歌翻译API?](https://www.zhihu.com/question/47239748/answer/147563856/)

### 完成度
- [ ] 其他语言互译(修改url中sl=en和tl=zh-CN)
- [x] 翻译无标点
- [x] 翻译多行无标点
- [ ] 翻译有标点
- [ ] 非utf-8编码
- [ ] 意外处理
- [ ] 文件重名详细逻辑
- [ ] 优化流程(内存 OOP) ~~不存在的~~
## End
