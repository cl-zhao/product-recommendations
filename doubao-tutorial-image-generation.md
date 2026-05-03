# 豆包AI教程 - 文生图篇

> 整理日期：2025年4月17日 | 资料总数：25+篇 | Prompt模板：25+个

---

## 一、豆包/即梦（Dreamina）图片生成功能介绍

### 1.1 产品定位

| 产品 | 定位 | 特点 |
|------|------|------|
| **豆包** | 字节跳动AI助手 | 集成文生图、图像编辑功能，支持对话式生图 |
| **即梦AI（Dreamina）** | 剪映旗下AI创作平台 | 图片生成、智能画布、视频生成一站式服务 |
| **Seedream 4.0** | 最新图像创作模型 | 文生图、图像编辑、组图生成一体化，支持2K原生分辨率 |

### 1.2 核心功能

- **文生图**：输入文字描述生成图片
- **图生图**：基于已有图片进行创意改造
- **智能画布**：一站式AI创作
- **主体一致性**：可保持角色一致性生成多图

### 1.3 资料来源

1. [豆包生图4.0大更新](https://zhuanlan.zhihu.com/p/1949529395917205641) - 知乎 | 2025年9月 | ⭐⭐⭐⭐⭐
2. [即梦Dreamina官网](https://www.aigc.cn/sites/28567.html) - AIGC工具导航 | ⭐⭐⭐⭐
3. [豆包图像生成又更新了](https://cloud.tencent.com/developer/news/2490565) - 腾讯云 | 2025年4月 | ⭐⭐⭐⭐
4. [即梦3.0：真正可用的AI生图](https://zhuanlan.zhihu.com/p/1894520984377198439) - 知乎 | ⭐⭐⭐⭐

---

## 二、如何进入和使用图片生成功能

### 2.1 豆包入口

1. **网页版**：访问 [doubao.com](https://www.doubao.com/chat/create-image)，点击「AI创作」或「文字生成图」按钮
2. **电脑版**：下载豆包桌面版，安装后进入「生成图像」界面
3. **APP端**：豆包APP已开启内测，可一次直出10张图像

### 2.2 即梦AI入口

1. 访问 [即梦AI官网](https://dreamina.jianying.com/)
2. 选择「图片生成」功能
3. 输入提示词，选择模型、图片比例、尺寸
4. 点击「立即生成」

### 2.3 使用技巧

- 使用内置「DeepSeek」帮写提示词功能
- 点击技能中的「图像生成」，保持技能使用状态
- 多次对话修改时可直接在技能内完成

### 2.4 资料来源

1. [豆包AI怎么画图 豆包AI以图生图新手指南](https://cj.sina.com.cn/articles/view/7879848900/1d5acf3c401902uuc2) - 新浪财经 | ⭐⭐⭐⭐
2. [国内最好用的生成图片方式：豆包告诉我们了](https://zhuanlan.zhihu.com/p/6709825892) - 知乎 | ⭐⭐⭐⭐
3. [想让想象力"变现"：豆包AI图像生成教程](http://ziyuan.bianji.com/a/26.html) - 互联网资源 | ⭐⭐⭐⭐

---

## 三、什么是Prompt（提示词）

### 3.1 Prompt定义

Prompt（提示词）是AI生成图像的短文本描述，AI会将Prompt中提到的单词和短语分解成更小的部分（token），与其训练数据比较后生成图像。

### 3.2 Prompt公式

```
Prompt = 风格词 + 主体 + 描述 + 效果提示词
```

或更详细的结构：
```
[主体] + [场景/环境] + [动作/姿态] + [风格] + [光线] + [色调] + [构图] + [画质修饰]
```

### 3.3 资料来源

1. [超详细的AI绘画Prompt文字教程](https://js.design/special/article/text-to-ai-image.html) - 即时设计 | 2023年8月 | ⭐⭐⭐⭐⭐
2. [通用文生图提示词（Prompt）：7步教你用AI创作让人惊艳的绝美图片](https://blog.csdn.net/m0_71746299/article/details/145288853) - CSDN | 2025年1月 | ⭐⭐⭐⭐⭐
3. [关于AI绘画的关键词Prompt知识](https://developer.aliyun.com/article/1189956) - 阿里云开发者社区 | 2024年10月 | ⭐⭐⭐⭐

---

## 四、好的绘图Prompt示例（20+可直接用的模板）

### 4.1 通用咒语公式

```
[主体描述] + [场景/环境] + [动作/表情] + [风格] + [光线] + [画质修饰]
```

### 4.2 模板集合

#### 📸 写实风格

| 序号 | Prompt模板 | 适用场景 |
|------|-----------|---------|
| 1 | 一位穿着汉服的东方美女站在古色古香的庭院中，手持团扇，回眸微笑，自然光，电影质感，8K超高清，景深感强 | 古风人像 |
| 2 | 金发碧眼的欧洲少女站在海边，阳光灿烂，海风轻拂发丝，湿身效果，逆光拍摄，杂志封面风格，顶级摄影师作品 | 时尚大片 |
| 3 | 老年工匠在传统作坊专注打磨陶瓷，暖色调灯光，侧光拍摄，纪实摄影风格，National Geographic风格 | 纪实摄影 |
| 4 | 赛博朋克城市夜景，霓虹灯光，雨湿街道，全息广告牌，车水马龙，的未来城市，戏剧性灯光，8K渲染 | 城市场景 |
| 5 | 浩瀚星空下的雪山，银河清晰可见，星空摄影，壮阔风景，超广角镜头，空气感，影视级画质 | 自然风光 |

#### 🎨 插画/艺术风格

| 序号 | Prompt模板 | 适用场景 |
|------|-----------|---------|
| 6 | 梦幻森林中的小精灵，森林仙子题材，柔和光影，魔法氛围，童话书插画风格，治愈系，柔和色调 | 童话插画 |
| 7 | 中国传统水墨画，锦鲤在荷塘中游动，写意风格，留白意境，水墨晕染，大师级作品 | 国风艺术 |
| 8 | 蒸汽朋克风格的飞行器，机械细节，铜黄配色，复古未来主义，概念艺术，复杂细节，轴测图 | 概念设计 |
| 9 | 迪士尼公主风格的角色设计，勇敢的探险家少女，彩色铅笔质感，温暖色调，儿童绘本风格 | 角色设计 |
| 10 | 浮世绘风格的日本街景，樱花飘落，葛饰北斋风格，传统木版画，经典配色 | 日式风格 |

#### 🏮 动漫风格

| 序号 | Prompt模板 | 适用场景 |
|------|-----------|---------|
| 11 | 蓝发双马尾少女，身穿JK制服，手持魔法杖，站在教室窗边，日系二次元动漫风格，参考《辉夜大小姐》的人物比例，黄昏教室，夕阳透过窗户洒在课桌上 | 二次元角色 |
| 12 | 银发剑客少年，站立在雪山之巅，白色长袍飘动，寒风中坚毅眼神，日系动漫风格，战斗姿态，冰雪场景 | 游戏角色 |
| 13 | Q版可爱猫咪，胖乎乎的身体，大眼睛，毛茸茸的尾巴，卡通形象，治愈系，简笔画风格 | 卡通形象 |
| 14 | 机甲战士，红色装甲，金属光泽，细节丰富，变形金刚风格，机甲设计稿，硬表面建模 | 机甲设计 |
| 15 | 日系少女站在樱花树下，花瓣飘落，逆光氛围，B站风格插画，清新唯美 | 动漫场景 |

#### 🇨🇳 国风/传统

| 序号 | Prompt模板 | 适用场景 |
|------|-----------|---------|
| 16 | 中国古代仕女图，唐代妆容，雍容华贵，牡丹花纹饰，国画工笔技法，古典美 | 传统仕女 |
| 17 | 水墨山水画，远山云雾，近处松林，隐士幽居，留白意境，宋代山水画风格 | 山水意境 |
| 18 | 年画风格的胖娃娃抱着大锦鲤，喜庆氛围，红色主调，传统年画，民间艺术 | 传统年画 |
| 19 | 汉服少年在竹林中练剑，轻盈飘逸，剑气竹林，国风武侠，古风美少年 | 武侠风格 |
| 20 | 青花瓷风格的花瓶，蓝色图案，景德镇瓷器风格，精细纹饰，传统工艺 | 器物设计 |

#### 🏙️ 建筑/产品设计

| 序号 | Prompt模板 | 适用场景 |
|------|-----------|---------|
| 21 | 未来科技感别墅，玻璃幕墙，绿色屋顶，太阳能板，环保设计，建筑杂志照片，建筑摄影 | 建筑设计 |
| 22 | 复古相机设计，黄铜机身，皮革纹理，徕卡风格，精致细节，产品摄影，广告风格 | 产品设计 |
| 23 | 未来主义汽车概念设计，流畅线条，电动汽车，贯穿式尾灯，展厅级渲染，汽车广告 | 概念汽车 |
| 24 | 极简主义北欧风客厅，大面积白色，原木家具，落地窗，自然光，室内设计杂志 | 室内设计 |
| 25 | 游戏场景原画，废弃都市废墟，苔藓覆盖，生锈金属，末世氛围，塞尔达风格游戏概念画 | 游戏场景 |

### 4.3 资料来源

1. [120个GPT-4o文生图核心提示词精选](https://blog.csdn.net/qq_41176800/article/details/146894674) - CSDN | 2025年4月 | ⭐⭐⭐⭐⭐
2. [16个很火的画风提示词](https://zhuanlan.zhihu.com/p/1963991157412466759) - 知乎 | 2025年10月 | ⭐⭐⭐⭐⭐
3. [豆包AI绘图提示词技巧](https://blog.csdn.net/dreamer23/article/details/145455598) - CSDN | 2025年2月 | ⭐⭐⭐⭐

---

## 五、不同风格的绘图提示词

### 5.1 风格词汇汇总

| 风格类型 | 关键词 |
|---------|-------|
| 写实 | realistic, photorealistic, 8K, HD, professional photography |
| 动漫 | anime, manga,二次元, 日本动画风格 |
| 国风 | Chinese ink painting, 国画, 水墨画, 工笔画, Painted in traditional Chinese style |
| 油画 | oil painting, impasto, classical painting |
| 赛博朋克 | cyberpunk, neon, futuristic, dystopia |
| 极简 | minimalist, clean, simple |
| 蒸汽朋克 | steampunk, Victorian, mechanical |
| 概念艺术 | concept art, sci-fi, fantasy art |

### 5.2 资料来源

1. [AI绘画常用提示词](https://www.uied.cn/24177.html) - UIED用户体验学习平台 | ⭐⭐⭐⭐⭐
2. [AI绘画Midjourney绘画提示词Prompt大全](https://zhuanlan.zhihu.com/p/676955175) - 知乎 | ⭐⭐⭐⭐

---

## 六、画面构图和镜头语言提示词

### 6.1 景别提示词

| 景别 | 英文 | 效果 |
|------|------|------|
| 特写 | close-up, closeup | 突出主体细节 |
| 近景 | medium shot | 人物胸部以上 |
| 中景 | medium close-up | 人物膝盖以上 |
| 远景 | wide shot | 展现环境 |
| 全景 | full shot | 完整展现主体 |
| 极远景 | extreme wide shot | 壮阔氛围 |

### 6.2 视角提示词

| 视角 | 英文 | 说明 |
|------|------|------|
| 俯视 | top view, aerial view | 展现规模 |
| 仰视 | low angle, upward view | 显得高大 |
| 平视 | eye level | 客观视角 |
| 斜侧 | three-quarter view | 增加立体感 |
| 顶视 | overhead shot | 俯拍 |

### 6.3 镜头提示词

- 50mm lens（标准镜头）
- wide angle lens（广角）
- telephoto lens（长焦）
- macro lens（微距）
- cinematic lighting（电影光感）
- shallow depth of field（浅景深）

### 6.4 资料来源

1. [AI视觉创作指南：镜头提示词全解析](https://blog.csdn.net/gogoMark/article/details/148164719) - CSDN | 2026年1月 | ⭐⭐⭐⭐
2. [超全总结！13个AI摄影景别提示词与效果展示](https://zhuanlan.zhihu.com/p/1895103713372271401) - 知乎 | 2025年4月 | ⭐⭐⭐⭐⭐
3. [AI绘画提示词详解](https://zhuanlan.zhihu.com/p/686808403) - 知乎 | 2024年3月 | ⭐⭐⭐⭐

---

## 七、负面提示词（不要在画面中出现什么）

### 7.1 通用负面提示词

```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, 
fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, 
signature, watermark, username, blurry, deformed, disfigured, mutation, mutated
```

### 7.2 人物专用负面提示词

```
ugly, mutilated, distorted face, malformed limbs, extra limbs, extra fingers, 
too many fingers, fused fingers, bad fingers, missing limbs, floating limbs, 
disconnected limbs, ugly face, distorted face, extra hands
```

### 7.3 避免变形问题的关键词

- `mutated hands and fingers` - 变异的手和手指
- `deformed` - 畸形的
- `bad anatomy` - 解剖不良
- `disfigured` - 毁容
- `poorly drawn hands` - 手部画得很差
- `missing limb` - 缺少的肢体
- `malformed hands` - 畸形的手
- `out of focus` - 脱离焦点
- `long neck` - 长颈
- `long body` - 身体过长

### 7.4 资料来源

1. [Stable Diffusion教学——负向提示词汇总](https://blog.csdn.net/m0_58477260/article/details/142334993) - CSDN | 2026年1月 | ⭐⭐⭐⭐⭐
2. [AI不会画手？加点负面描述试试](https://www.wujiebantu.com/article/6765675) - 无界版图 | 2023年3月 | ⭐⭐⭐⭐
3. [Stable Diffusion提示词与负面提示词](https://www.stablediffusion-cn.com/sd/sd-use/807.html) - Stable Diffusion中文网 | ⭐⭐⭐⭐

---

## 八、生成的图片版权归属问题

### 8.1 各平台版权政策对比

| 平台 | 版权归属 | 商业使用 |
|------|---------|---------|
| 豆包 | 用户所有 | 可商用 |
| 即梦AI | 用户所有 | 可商用 |
| Midjourney（免费版） | 平台所有 | 不可商用 |
| Midjourney（付费版） | 用户所有 | 可商用，需保留部分权利 |
| 百度文心一格 | 百度公司所有 | 需获授权 |

### 8.2 版权注意事项

1. **豆包/即梦**：用户上传内容归用户所有，输出内容版权归用户，平台对生成内容享有免费、可转让的使用权（用于模型优化等）
2. **避免侵权**：不要生成与现有版权作品相似度过高的图像
3. **标识要求**：部分平台会在生成图片右下角添加水印标识
4. **商用建议**：查看各平台服务条款，确认商业使用权限

### 8.3 资料来源

1. [AI生成图像版权归谁？一文搞懂各大平台规则](https://www.shejidaren.com/ai-sheng-cheng-tu-xiang-ban-quan-gui-shui.html) - 设计达人 | ⭐⭐⭐⭐⭐
2. [AI绘画版权问题知多少](https://finance.sina.cn/2023-04-24/detail-imyrnqvm4693345.d.html) - 新浪财经 | 2023年4月 | ⭐⭐⭐⭐
3. [商业化使用AI图片生成平台的业务模式与版权风险](https://www.hankunlaw.com/portal/article/index/cid/8/id/13342.html) - 汉坤律师事务所 | 2023年6月 | ⭐⭐⭐⭐⭐

---

## 九、和其他绘图工具的对比

### 9.1 主流AI绘画工具对比

| 工具 | 费用 | 优势 | 劣势 |
|------|------|------|------|
| **豆包** | 免费 | 中文支持好本土化、免费使用 | 功能相对基础 |
| **即梦AI** | 免费 | 字节生态、图生视频能力强 | 相对较新 |
| **Midjourney** | $10+/月 | 艺术性强、社区成熟 | 需翻墙、英文界面 |
| **Stable Diffusion** | 免费（本地） | 可控性强、完全免费 | 需技术门槛、配置要求高 |
| **DALL-E 3** | $20/月 | OpenAI生态、文字生成准 | 艺术性一般 |

### 9.2 选购建议

- **新手/普通用户**：首选豆包或即梦AI，免费且易上手
- **专业设计师**：可考虑Midjourney+Stable Diffusion组合
- **中文创作需求**：豆包/即梦对中文理解和生成更准确

### 9.3 资料来源

1. [国内外AI绘画大模型对比（Midjourney、文心一言、豆包）](https://blog.csdn.net/AI001100/article/details/138473908) - CSDN | 2024年5月 | ⭐⭐⭐⭐
2. [AI绘画工具Midjourney与Stable Diffusion的深度对比](https://www.douban.com/note/872353817/) - 豆瓣 | 2025年4月 | ⭐⭐⭐⭐
3. [Midjourney与Stable Diffusion全面对比](https://cgmi.com/archives/311) - CGMI | ⭐⭐⭐⭐

---

## 十、常见问题和解决

### 10.1 图片生成问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 图片不显示 | 网络问题/格式不兼容 | 检查网络、刷新页面 |
| 文字生成乱码 | AI对文字理解有限 | 避免在画面中生成文字，或使用后处理添加 |
| 手指畸形 | AI手部绘制难点 | 使用负面提示词+局部重绘 |
| 达到生成上限 | 免费次数用完 | 等待次日刷新或使用其他工具 |

### 10.2 生成效果优化

1. **提示词优化**：越详细具体效果越好
2. **使用DeepSeek帮写**：即梦AI内置DeepSeek提示词优化
3. **调整参数**：尝试不同比例、尺寸
4. **迭代优化**：基于满意的作品进行图生图

### 10.3 资料来源

1. [豆包AI生成图片怎么去水印](https://www.stablediffusion-cn.com/aist/9615.html) - Stable Diffusion中文网 | ⭐⭐⭐⭐
2. [豆包支持在图片生成中文](https://zhuanlan.zhihu.com/p/10895706303) - 知乎 | ⭐⭐⭐⭐
3. [AI生成图片中的文字为何总是混乱](https://blog.csdn.net/Z_oioihoii/article/details/146717828) - CSDN | 2025年3月 | ⭐⭐⭐⭐

---

## 十一、视频教程资源

### 11.1 B站教程

1. [Midjourney超详细使用教程](https://www.bilibili.com/video/BV1nN4y1g7bW/) - B站 | ⭐⭐⭐⭐⭐
2. [B站第一套系统的AI绘画课！零基础学会Stable Diffusion](https://www.aigc00.com/book/8513.html) - AIGC起点导航 | ⭐⭐⭐⭐⭐
3. [Midjourney从入门到精通系列教程](https://m.okjike.com/originalPosts/63c7b30b43f939b952a89cad) - 即刻App | ⭐⭐⭐⭐

### 11.2 综合教程

1. [超详细的Midjourney入门教程](https://www.shejidaren.com/midjourney-ru-men-jiao-cheng.html) - 设计达人 | 2023年11月 | ⭐⭐⭐⭐⭐
2. [Midjourney用户手册中文版](https://uiiiuiii.com/aigc/1212610119.html) - 优优教程网 | ⭐⭐⭐⭐⭐

---

## 十二、界面截图描述（用于图文并茂）

### 12.1 豆包网页版

- 入口位置：页面下方「文字生成图」按钮
- 操作区域：输入框输入描述，选择风格和比例
- 输出区域：生成4张图片供选择

### 12.2 即梦AI

- 模型选择：图片3.0（最新）
- 参数设置：图片比例（1:1/16:9/9:16等）、图片尺寸
- DeepSeek帮写：内置智能提示词优化

---

## 📌 总结

### 核心要点

1. **豆包/即梦AI** 是国内免费的AI绘图工具，中文支持好
2. **Prompt公式** = 主体 + 场景 + 风格 + 光线 + 画质
3. **负面提示词** 很重要，可避免常见变形问题
4. **版权问题**：豆包/即梦生成图片可商用
5. **持续迭代**：效果不好就调整提示词重新生成

### 推荐学习路径

1. 先在豆包/即梦AI尝试基础生成
2. 学会写详细的具体描述
3. 掌握负面提示词使用
4. 了解不同风格关键词
5. 学习构图和镜头语言

---

*资料整理：小亮 | 来源：知乎、CSDN、阿里云、腾讯云、设计达人等 | 可靠性：⭐⭐⭐⭐（大多数为2024-2025年新资料）*
