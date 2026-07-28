
---

*文档整理完成于 2026-04-13*
---
# 十周年按钮控件设计规范
> 来源: Figma文档"十周年--交互设计规范", 页面"--按钮控件-规范"
> 提取日期: 2026-04-13

---

## 消耗按钮

### 1. 概述
**标题**: 消耗按钮规则
**字体**: FZShengShiKaiShuS-B-GB, 100px

**说明文字**:
- 99999
- 99999
- 99999
- 开始游戏
- 99999

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 4304 | FRAME | 180px | 35px |
| Frame 4312 | FRAME | 180px | 22px |
| Frame 4304 | FRAME | 180px | 35px |
| Frame 4303 | FRAME | 193px | 50px |
| 折扣价格 | FRAME | 152px | 22px |
| Frame 4311 | FRAME | 152px | 35px |
| Frame 4312 | FRAME | 152px | 22px |
| Frame 4304 | FRAME | 128px | 35px |
| Frame 4312 | FRAME | 152px | 22px |
| Frame 4304 | FRAME | 128px | 35px |
| Frame 4312 | FRAME | 152px | 22px |
| Frame 4303 | FRAME | 193px | 50px |
| 折扣价格 | FRAME | 152px | 22px |
| Frame 4303 | FRAME | 193px | 50px |
| 折扣价格 | FRAME | 152px | 22px |
| Frame 4312 | FRAME | 180px | 22px |
| Frame 4304 | FRAME | 200px | 31px |
| 消耗购买类按钮 | FRAME | 180px | 54px |
| 一级 | FRAME | 200px | 54px |
| Frame 4304 | FRAME | 200px | 31px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 消耗购买类按钮 | 180px | 54px |
| 一级 | 180px | 54px |
| 货币栏 | 48px | 35px |
| 消耗购买类按钮 | 180px | 54px |
| 一级 | 180px | 54px |
| 货币栏 | 48px | 35px |
| 消耗购买类按钮 | 254px | 107px |
| 特殊活动大 | 264px | 107px |
| 货币栏 | 50px | 50px |
| 货币栏 | 34px | 26px |
| 消耗购买类按钮 | 155px | 70px |
| 二级 | 155px | 70px |
| 二级按钮 | 155px | 48px |
| 九宫-一级按钮/Group 38 | 87.6973648071289px | 27px |
| 货币栏 | 48px | 35px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 消耗按钮规则 | 消耗按钮规则 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 原价加分隔符“，” 三位加一个：000,000 | 原价加分隔符“，”
三位加一个：000, | 96px | FZShengShiKaiShuS-DB-GB | #fda4a4 |
| 购买类 | 购买类 | 64px | FZShengShiKaiShuS-B-GB | #454545 |
| 门票类 | 门票类 | 64px | FZShengShiKaiShuS-B-GB | #454545 |
| 部分特殊消耗条件显示 | 部分特殊消耗条件显示 | 64px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 用于 有资源类消耗的操作指令处， 状态: 当前页面配置消耗类操作时均 须在页面货币栏显示对应消耗货币的当前拥有数量，并配置点击icon查看 使用方式+获取途径 交互: 满足消耗条件后，点击即可消耗对资源完成操作指令。否则需表示未满足条件下的货币的状态，点击弹出对应提示（自动补足消耗提示、引导购买） | 情境: 用于 有资源类消耗的操作指令处， | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 可购买状态 | 可购买状态 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 常用消耗 | 常用消耗 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 双消耗 | 双消耗 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 折扣类信息页签+说明类文字 | 折扣类信息页签+说明类文字 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 货币不足 | 货币不足 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 已售罄 | 已售罄 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 已拥有 | 已拥有 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 已领取 | 已领取 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 其他特殊状态 | 其他特殊状态 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 折扣信息 | 折扣信息 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 在直接购买类界面中，消耗按钮直接显示所需消耗的货币 根据购买物品在当前页面的内容 配置对应的级别按钮 | 在直接购买类界面中，消耗按钮直接显示所需 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 在玩法或者活动界面，需要显示消耗数量及对应操作信息的按钮（界面主体按钮，一般为第一优先级视觉落点） | 在玩法或者活动界面，需要显示消耗数量及对 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 按钮尺寸;高度=54，宽度根据场景，可自适应调整 （参考值：220以内） | 按钮尺寸;高度=54，宽度根据场景，可自 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 资源位数：十周年特色1-5位，最高5位。 | 资源位数：十周年特色1-5位，最高5位。 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 文字命名规范：招募类按钮上的数字均用文字 不用阿拉伯数字了，避免按钮上数字的数量太密集。 | 文字命名规范：招募类按钮上的数字均用文字 | 40px | FZBeiWeiKaiShu-S19S | #ff1212 |
| 在玩法或者活动界面，对应操作需要消耗的资源需要特殊文字显示时 | 在玩法或者活动界面，对应操作需要消耗的资 | 40px | FZBeiWeiKaiShu-S19S | #454545 |
| 购买操作类 | 购买操作类 | 40px | FZShengShiKaiShuS-B-GB | #ffffff |
| 门票类 |  门票类 | 40px | FZShengShiKaiShuS-B-GB | #ffffff |
| 部分特殊消耗条件 | 部分特殊消耗条件 | 40px | FZShengShiKaiShuS-B-GB | #ffffff |
| 99999 | 99999 | 32px | FZBeiWeiKaiShu-S19_GBK | #61351b |
| 99999 | 99999 | 32px | FZBeiWeiKaiShu-S19_GBK | #61351b |
| 99999 | 99999 | 32px | FZBeiWeiKaiShu-S19_GBK | #ff0404 |
| 对齐方式： 按钮与价格、说明文字自适应居中对齐 折扣价签，贴图位置对齐 | 对齐方式：
按钮与价格、说明文字自适应居 | 32px | FZBeiWeiKaiShu-S19_GBK | #454545 |
| 99999 | 99999 | 28px | FZShengShiKaiShuS-DB-GB | #6a3c22 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #6a3c22 | 99999 | 出现16次 |
| #d92d15 | 99999 | 出现4次 |
| #61351b | 99999 | 出现2次 |
| #af936c | 原价:30000元宝 | 出现3次 |
| #ffc983 | 数量 | 出现4次 |
| #663d20 | 按钮名字 | 出现4次 |
| #ff0404 | 99999 | 出现1次 |
| #ffffff | 已售罄 | 出现7次 |
| #deba89 | 原价:30000元宝 | 出现5次 |
| #734d1f | 38888 | 出现4次 |

---

## 操作按钮

### 1. 概述
**标题**: 按钮Button
**字体**: FZShengShiKaiShuS-B-GB, 100px

**说明文字**:
- 金色一级通用按钮；在同一张界面内，仅可出现一个，用作画面中最重要的按钮。
- 一级通用按钮统一使用文字+方形按钮的样式，缺一不可
- 通用三级按钮使用规范
- 文字字号；28px
- 棕色二级通用按钮；多用于弹窗或浮层中

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 526 | FRAME | 94px | 40px |
| Frame 4304 | FRAME | 180px | 35px |
| Frame 4312 | FRAME | 180px | 22px |
| Component 214 | FRAME | 33px | 33px |
| 空白 2 | FRAME | 33px | 33px |
| 弹窗 | FRAME | 1145px | 771px |
| Frame 2431 | FRAME | 430px | 54px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 二级按钮 | 152px | 48px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 一级按钮 | 180px | 54px |
| 九宫-一级按钮/Group 38 | 86px | 27px |
| 一级按钮 | 182px | 58px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 按钮Button | 按钮Button | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 十周年按钮 | 十周年按钮 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 有更新 | 有更新 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 热区规范 | 热区规范 | 60px | FZShengShiKaiShuS-B-GB | #000000 |
| 长文本按钮 | 长文本按钮 | 60px | FZShengShiKaiShuS-B-GB | #000000 |
| 单选多选控件 | 单选多选控件 | 60px | FZShengShiKaiShuS-B-GB | #000000 |
| switcher | switcher | 60px | FZShengShiKaiShuS-B-GB | #000000 |
| 通用一级按钮 | 通用一级按钮 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 通用二级按钮 | 通用二级按钮 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 通用三级按钮 | 通用三级按钮 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 金色一级通用按钮；在同一张界面内，仅可出现一个，用作画面中最重要的按钮。 | 金色一级通用按钮；在同一张界面内，仅可出 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 一级通用按钮统一使用文字+方形按钮的样式，缺一不可 | 一级通用按钮统一使用文字+方形按钮的样式 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 通用三级按钮使用规范 | 通用三级按钮使用规范 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 文字字号；28px | 文字字号；28px | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 棕色二级通用按钮；多用于弹窗或浮层中 | 棕色二级通用按钮；多用于弹窗或浮层中 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 金色二级通用按钮；多用于弹窗或浮层中，重要等级高于棕色 | 金色二级通用按钮；多用于弹窗或浮层中，重 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 金色、棕色二级按钮使用具体根据界面功能等级和颜色确定。 | 金色、棕色二级按钮使用具体根据界面功能等 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 用于一些不太重要的功能，也可以去掉文字，仅按钮单独使用 | 用于一些不太重要的功能，也可以去掉文字， | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 通用二级按钮状态规范 | 通用二级按钮状态规范 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 通用二级按钮样式规范 | 通用二级按钮样式规范 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 文字字号24px，文字在底板中心居中 | 文字字号24px，文字在底板中心居中 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 一级按钮整个按钮为点击热区 | 一级按钮整个按钮为点击热区 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 一级按钮目前最多支持七个字 | 一级按钮目前最多支持七个字 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 开关 | 开关 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 其他内容 | 其他内容 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 注:最多支持三个选项的切换，但是目前还没有在十周年中使用 | 注:最多支持三个选项的切换，但是目前还没 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 二级按钮目前字数最多四个字 | 二级按钮目前字数最多四个字 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 按钮长度按照文字长度自动适配 | 按钮长度按照文字长度自动适配 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 三级按钮目前没有按钮字数限制，但是一般不会超过七个字 | 三级按钮目前没有按钮字数限制，但是一般不 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 单选: | 单选: | 40px | FZShengShiKaiShuS-B-GB | #454545 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #454545 | 按钮Button | 出现51次 |
| #000000 | 热区规范 | 出现8次 |
| #ead0a3 | 按钮名字 | 出现4次 |
| #3c271c | 查看 | 出现4次 |
| #6a3c22 | 按钮名字 | 出现9次 |
| #ffffff | 十周年按钮 | 出现5次 |
| #663d20 | 按钮名字 | 出现4次 |
| #7d7d7d | 按钮名字 | 出现1次 |
| #deba89 | 按钮名字 | 出现4次 |
| #b8b8b8 | 按钮名字 | 出现1次 |

---

## 控件规范-筛选

### 1. 概述
**标题**: 向上
**字体**: FZBeiWeiKaiShu-S19S, 101.72106170654297px

**说明文字**:
- 界面标题
- i
- 按钮名字
- 99
- 二级按钮

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 502 | FRAME | 1351.4072265625px | 759.78662109375px |
| Component 184 | FRAME | 226.5721893310547px | 51.567081451416016px |
| Frame 2419 | FRAME | 224.16184997558594px | 144.62054443359375px |
| Frame 2417 | FRAME | 224.16184997558594px | 144.62054443359375px |
| Frame 2419 | FRAME | 224.16184997558594px | 144.62054443359375px |
| Frame 2417 | FRAME | 224.16184997558594px | 144.62054443359375px |
| Component 184 | FRAME | 226.5721893310547px | 51.567081451416016px |
| Frame 24 | FRAME | 147.3333282470703px | 42px |
| Frame 24 | FRAME | 147.3333282470703px | 42px |
| Frame 4462 | FRAME | 73.4991455078125px | 13.1663818359375px |
| Frame 2430 | FRAME | 430px | 54px |
| Frame 2430 | FRAME | 430px | 54px |
| Frame 2431 | FRAME | 430px | 54px |
| Frame 5013 | FRAME | 741.8536376953125px | 96px |
| Frame 5014 | FRAME | 811.8536376953125px | 96px |
| Component 184 | FRAME | 453.1443786621094px | 103.13416290283203px |
| Frame 2419 | FRAME | 448.3236999511719px | 289.2410888671875px |
| Frame 2417 | FRAME | 448.3236999511719px | 289.2410888671875px |
| Component 184 | FRAME | 453.1443786621094px | 103.13416290283203px |
| Frame 2419 | FRAME | 448.3236999511719px | 289.2410888671875px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 下拉栏 | 227.77735900878906px | 486.8891906738281px |
| Component 183 | 224.16184997558594px | 72.31027221679688px |
| Component 186 | 224.16184997558594px | 72.31027221679688px |
| Component 187 | 224.16184997558594px | 72.31027221679688px |
| Component 188 | 224.16184997558594px | 72.31027221679688px |
| Component 189 | 224.16184997558594px | 72.31027221679688px |
| Component 190 | 224.16184997558594px | 72.31027221679688px |
| Component 185 | 224.16184997558594px | 72.31027221679688px |
| Component 186 | 224.16184997558594px | 72.31027221679688px |
| Component 187 | 224.16184997558594px | 72.31027221679688px |
| Component 188 | 224.16184997558594px | 72.31027221679688px |
| Component 189 | 224.16184997558594px | 72.31027221679688px |
| Component 190 | 224.16184997558594px | 72.31027221679688px |
| 翻页 | 360.6666564941406px | 42px |
| 翻页 | 360.6666564941406px | 44px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 向上 | 向上 | 101.72106170654297px | FZBeiWeiKaiShu-S19S | #4b4b4b |
| 向上 | 向上 | 101.72106170654297px | FZBeiWeiKaiShu-S19S | #4b4b4b |
| 向下 | 向下 | 101.72106170654297px | FZBeiWeiKaiShu-S19S | #4b4b4b |
| 向下 | 向下 | 101.72106170654297px | FZBeiWeiKaiShu-S19S | #4b4b4b |
| 十周年通用控件规范展示 | 十周年通用控件规范展示 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 下拉菜单 | 下拉菜单 | 80px | FZBeiWeiKaiShu-S19_GBK | #000000 |
| list | list | 80px | FZBeiWeiKaiShu-S19_GBK | #ff0000 |
| 关闭规则 | 关闭规则 | 80px | FZBeiWeiKaiShu-S19_GBK | #000000 |
| 翻页 | 翻页 | 80px | FZBeiWeiKaiShu-S19_GBK | #ff0000 |
| Switcher | Switcher | 80px | FZBeiWeiKaiShu-S19_GBK | #ff0000 |
| 名字内容 | 类型： 全部 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #e6c18b |
| 武将升阶 | 稀有度 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #61351b |
| 武将升阶 | 武将 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #d1c19a |
| 名字内容 | 类型： 全部 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #e6c18b |
| 武将升阶 | 稀有度 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #61351b |
| 武将升阶 | 武将 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #d1c19a |
| 名字内容 | 稀有度 | 48.20684814453125px | FZShengShiKaiShuS-DB-GB | #d1c19a |
| 名字内容 | 稀有度 | 48.20684814453125px | FZShengShiKaiShuS-DB-GB | #d1c19a |
| 类型：全部 | 类型：全部 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #e6c18b |
| 武将升阶 | 稀有度 | 48.20684814453125px | FZShengShiKaiShuS-DB-GB | #61351b |
| 武将升阶 | 武将 | 48.20684814453125px | FZShengShiKaiShuS-DB-GB | #d1c19a |
| 名字内容 | 稀有度 | 48.20684814453125px | FZBeiWeiKaiShu-S19_GBK | #d1c19a |
| 最通用的翻页控件组 | 最通用的翻页控件组 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #00a310 |
| 翻页切换按钮 | 翻页切换按钮 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #00a310 |
| 圆点位置跟随翻页页码进行切换，且圆点可点击并定位对应页面 | 圆点位置跟随翻页页码进行切换，且圆点可点 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #353535 |
| 快捷翻页 | 快捷翻页 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #00a310 |
| 增加翻至末尾/首页（暂未在游戏中使用） | 增加翻至末尾/首页（暂未在游戏中使用） | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #353535 |
| 弹窗关闭 | 弹窗关闭 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #353535 |
| 通常情况下，点击”x”直接关闭弹窗 | 通常情况下，点击”x”直接关闭弹窗 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #353535 |
| 有取消按钮的时候没有“x”按钮，点击取消直接关闭弹窗 | 有取消按钮的时候没有“x”按钮，点击取消 | 42.54847717285156px | FZShengShiKaiShuS-B-GB | #353535 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #3c271c | 界面标题 | 出现4次 |
| #ffffff | i | 出现15次 |
| #b6b6b6 | 99 | 出现1次 |
| #4b4b4b | 向上 | 出现4次 |
| #e6c18b | 名字内容 | 出现4次 |
| #61351b | 武将升阶 | 出现5次 |
| #d1c19a | 武将升阶 | 出现9次 |
| #000000 | 下拉菜单 | 出现2次 |
| #ff0000 | list | 出现3次 |
| #00a310 | 最通用的翻页控件组 | 出现3次 |

---

## 功能按钮

### 1. 概述
**标题**: 勾选按钮
**字体**: FZShengShiKaiShuS-B-GB, 100px

**说明文字**:
- 创建房间
- 模式选择：
- 自由
- 演武
- ≤2%

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 2431 | FRAME | 430px | 54px |
| Frame 4439 | FRAME | 1008px | 266.3055419921875px |
| Frame 4329 | FRAME | 423px | 33px |
| Frame 4321 | FRAME | 287px | 33px |
| Frame 4330 | FRAME | 752px | 33.30555725097656px |
| Frame 4321 | FRAME | 616px | 33.30555725097656px |
| Frame 2526 | FRAME | 1008px | 47px |
| Component 199 | FRAME | 228.67869567871094px | 44px |
| Component 200 | FRAME | 201px | 44px |
| Component 201 | FRAME | 201px | 44px |
| Component 203 | FRAME | 201px | 44px |
| Frame 2528 | FRAME | 582px | 36px |
| Frame 4438 | FRAME | 856px | 50px |
| Component 214 | FRAME | 33px | 33px |
| 空白 2 | FRAME | 33px | 33px |
| Component 214 | FRAME | 33px | 33px |
| 空白 2 | FRAME | 33px | 33px |
| Component 214 | FRAME | 33px | 33px |
| 空白 2 | FRAME | 33px | 33px |
| 身份场-八人 自由至尊演武 | FRAME | 1334px | 750px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 中弹窗 | 1084.1759033203125px | 582px |
| 弹窗一级副按钮 | 180px | 54px |
| 弹窗一级主按钮 | 180px | 54px |
| 三级图标 | 31.284542083740234px | 33px |
| 三级图标 | 31.903654098510742px | 33px |
| 三级图标 | 44px | 44px |
| 三级图标 | 44px | 44px |
| 三级图标 | 31.284542083740234px | 33px |
| 三级图标 | 32.199058532714844px | 33.30555725097656px |
| 三级图标 | 33px | 33px |
| 三级图标 | 30px | 30px |
| 底 4 | 200px | 44px |
| 底 4 | 200px | 44px |
| 底 4 | 200px | 44px |
| 底 4 | 200px | 44px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 勾选按钮 | 勾选按钮 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| switcher | switcher | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 滑块 | 滑块 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 十周年按钮 | 十周年按钮 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 菜单按钮 | 菜单按钮 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 单选 | 单选 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 样式一 | 样式一 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 样式二 | 样式二 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 多选 | 多选 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 局内 | 局内 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 大厅 | 大厅 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 数值调整情境 | 数值调整情境 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 快捷浏览长页面或内容 | 快捷浏览长页面或内容 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 目前移动 游戏内暂无 | 目前移动 游戏内暂无 | 60px | FZShengShiKaiShuS-B-GB | #ff1919 |
| 个人信息页 | 个人信息页 | 60px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 用于对内容进行开启/关闭的操作， 状态: 开启与关闭需有明确对比区分 交互: 点击即可进行切换,不区分左右区域 | 情境: 用于对内容进行开启/关闭的操作， | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 用于在内容上 有两种模式可切换的情境 状态: 左右两个模式选中态按钮需有区分，对于推荐玩家去选择的选项放置在右侧，用明亮的主色调;相反则用次级色调 交互: 点击即可 进行切换,不区分左右区域 | 情境: 用于在内容上  有两种模式可切换 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 用于仅可选择一项的情境 状态: 有选中/未选中状态 交互: 点击即可选中，同一标题命令下，每个单选项操作互斥，点击其他选项，当前已选中的变为未选中态 | 情境: 用于仅可选择一项的情境
状态:  | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 用于可进行多项选择的情境 状态: 有选中/未选中状态 交互: 点击即可选中，再次点击则取消选中。所有选项之间互不干扰，不互斥。 | 情境: 用于可进行多项选择的情境
状态: | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 一般用于 需“快捷浏览长页面或内容”的需求场景中， 或者对某个设置数值进行 无极调节时 状态: 数值调整情境下 需有：关闭状态 和 已开启状态 交互: 支持拖动 任意调节数值大小; 支持点击滑动条任意位置 立即生效当前位置数值 | 情境: 一般用于 需“快捷浏览长页面或内 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 情境: 一般用于需要收纳多个功能入口的场景，如，当前界面存在多个功能入口，需要被隐藏时 样式: 根据当前页面场景 进行样式设定，状态为:点击展开 点击收起 交互: 点击后展开所包含的 功能入口（菜单按钮不隐藏）再点击，功能入口收纳至菜单按钮中，根据页面布局设定菜单展开方向 | 情境: 一般用于需要收纳多个功能入口的场 | 40px | FZShengShiKaiShuS-B-GB | #454545 |
| 位六 | 位六 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位六 | 位六 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位八 | 位八 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位一 | 位一 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位二 | 位二 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位三 | 位三 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 位四 | 位四 | 32px | FZShengShiKaiShuS-DB-GB | #cba065 |
| 文字内容 | 创建房间 | 30px | FZShengShiKaiShuS-DB-GB | #c8a176 |
| 按钮文字 | 确定 | 30px | FZShengShiKaiShuS-DB-GB | #6a3c22 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #454545 | 勾选按钮 | 出现19次 |
| #ffffff | 十周年按钮 | 出现1次 |
| #c8a176 | 文字内容 | 出现1次 |
| #443128 | 模式选择： | 出现26次 |
| #d1c19a | 自由 | 出现4次 |
| #6a3c22 | 按钮文字 | 出现2次 |
| #c2a99d | 欢乐成双·自由 | 出现2次 |
| #e1c99f | 旧版 | 出现2次 |
| #512f00 | 开 | 出现2次 |
| #f0cf98 | 新版 | 出现2次 |

---

## 货币

### 1. 概述
**标题**: 货币栏规则
**字体**: FZShengShiKaiShuS-B-GB, 100px

**说明文字**:
- 界面标题七个字
- 内容
- 界面标题七个字
- 内容
- 按钮名字

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 510 | FRAME | 1334px | 750px |
| Frame 525 | FRAME | 856px | 53.400001525878906px |
| Frame 512 | FRAME | 1334px | 750px |
| Frame 526 | FRAME | 856px | 53.400001525878906px |
| Frame 511 | FRAME | 1334px | 750px |
| Frame 525 | FRAME | 856px | 53.400001525878906px |
| Frame 513 | FRAME | 1334px | 750px |
| Frame 523 | FRAME | 1334px | 750px |
| Frame 524 | FRAME | 218px | 67px |
| Frame 525 | FRAME | 856px | 53.400001525878906px |
| Frame 526 | FRAME | 1334px | 750px |
| Frame 525 | FRAME | 1334px | 750px |
| Frame 527 | FRAME | 192px | 506px |
| Frame 526 | FRAME | 856px | 53.400001525878906px |
| Frame 527 | FRAME | 1334px | 750px |
| Frame 522 | FRAME | 1334px | 750px |
| Frame 526 | FRAME | 856px | 53.400001525878906px |
| Frame 2 | FRAME | 1334px | 750px |
| Frame 3 | FRAME | 139px | 2207px |
| Frame 528 | FRAME | 856px | 53.400001525878906px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 大弹窗 | 1084px | 584px |
| 大弹窗 | 1084px | 584px |
| 边栏弹窗 | 1084px | 584px |
| Component 66 | 177px | 58px |
| Component 233 | 192px | 66px |
| Component 68 | 192px | 66px |
| Component 234 | 177px | 58px |
| Component 67 | 177px | 58px |
| Component 235 | 177px | 58px |
| Component 67 | 177px | 58px |
| Component 236 | 177px | 58px |
| Component 67 | 177px | 58px |
| Component 237 | 177px | 58px |
| Component 67 | 177px | 58px |
| Component 238 | 177px | 58px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 货币栏规则 | 货币栏规则 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 常规弹窗中的货币栏 | 常规弹窗中的货币栏 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 特殊弹窗中的货币栏（后续将迭代掉） | 特殊弹窗中的货币栏（后续将迭代掉） | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 货币书写规则 | 货币书写规则 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 亿和万可以用汉字 | 亿和万可以用汉字 | 100px | FZShengShiKaiShuS-B-GB | #454545 |
| 十周年货币栏位置 | 十周年货币栏位置 | 100px | FZShengShiKaiShuS-B-GB | #ffffff |
| 1位 | 1位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 2位 | 2位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 3位 | 3位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 4位 | 4位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 5位 | 5位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 6位 | 6位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 7位 | 7位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 8位 | 8位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 9位 | 9位 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #000000 |
| 9 | 9 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 99 | 99 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 999 | 999 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 9999 | 9999 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 9万 | 9万 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 99万 | 99万 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 999万 | 999万 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 9999万 | 9999万 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 9亿 | 9亿 | 92.63158416748047px | FZShengShiKaiShuS-B-GB | #efd9be |
| 1.位置；从右至左排列，货币根据显示重要程度从右到左依次递减 | 1.位置；从右至左排列，货币根据显示重要 | 60px | FZShengShiKaiShuS-B-GB | #414141 |
| 2.数量；货币最多显示5种。当在一个系统中弹出下一级页面的时候，货币 | 2.数量；货币最多显示5种。当在一个系统 | 60px | FZShengShiKaiShuS-B-GB | #414141 |
| 3.层级; 保持在全屏界面的最上层，在该页面打开了其他页面或弹窗，如果同样和货币相关，那么货币栏不被遮挡，还在最上层显示 | 3.层级; 保持在全屏界面的最上层，在该 | 60px | FZShengShiKaiShuS-B-GB | #414141 |
| 4.货币种类；可以支持对应的策划填表，对应页面显示哪些货币 | 4.货币种类；可以支持对应的策划填表，对 | 60px | FZShengShiKaiShuS-B-GB | #414141 |
| 5.交互热区； ①可直接购买类货币，显示加号，点击直接弹出购买弹窗。 ②不可直接购买类，不显示加号，点击弹出对应tips说明. | 5.交互热区；
 ①可直接购买类货币，显 | 60px | FZShengShiKaiShuS-B-GB | #414141 |
| 取消 | 取消 | 32px | FZShengShiKaiShuS-DB-GB | #e5bb62 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #3c271c | 界面标题七个字 | 出现29次 |
| #000000 | 内容 | 出现15次 |
| #ffffff | i | 出现8次 |
| #efd9be | 9999 | 出现60次 |
| #454545 | 货币栏规则 | 出现5次 |
| #cc9f6c | 标题 | 出现1次 |
| #e5bb62 | 取消 | 出现2次 |
| #b81515 | 15px | 出现4次 |
| #e0ca9f | 标题名字 | 出现8次 |
| #80522c | 内容名字 | 出现1次 |

---

## 货币资源导航

### 1. 概述
**标题**: 获取途径优化
**字体**: Microsoft YaHei, 120px

**说明文字**:
- 2024-05-13
- UE: 
- 王立哲
- 策划: 
- ta的名字

### 2. 尺寸规范

**主要组件尺寸**:
| 组件名称 | 类型 | 宽度 | 高度 |
|----------|------|------|------|
| Frame 4856 | FRAME | 1359px | 723px |
| Frame 4593 | FRAME | 1220px | 449px |
| Frame 4857 | FRAME | 1359px | 573px |
| Frame 4989 | FRAME | 4375px | 317px |
| 纳贤令 | FRAME | 1084.1759033203125px | 582px |
| Frame 4385 | FRAME | 1084.1759033203125px | 582px |
| 中弹窗 | FRAME | 1084.1759033203125px | 582px |
| Frame 2431 | FRAME | 430px | 54px |
| Frame 4304 | FRAME | 180px | 50px |
| Frame 4312 | FRAME | 180px | 22px |
| Frame 4846 | FRAME | 796px | 214.49351501464844px |
| Frame 4589 | FRAME | 169px | 192.917236328125px |
| Frame 4569 | FRAME | 105px | 106px |
| Frame 4322 | FRAME | 105px | 106px |
| Frame 4888 | FRAME | 394.84814453125px | 44px |
| 招募令 | FRAME | 1084.1759033203125px | 582px |
| Frame 4385 | FRAME | 1084.1759033203125px | 582px |
| 中弹窗 | FRAME | 1084.1759033203125px | 582px |
| Frame 2431 | FRAME | 430px | 54px |
| Frame 4304 | FRAME | 180px | 50px |

**实例组件尺寸**:
| 组件名称 | 宽度 | 高度 |
|----------|------|------|
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 数字标/全部注意 | 50px | 59px |
| Component 181 | 50px | 59px |
| 三级图标 | 44px | 44px |
| 弹窗一级副按钮 | 180px | 54px |
| 弹窗一级主按钮 | 180px | 54px |

### 3. 字体规范

**文本元素字体表**:
| 名称 | 内容 | 字号 | 字体 | 颜色 |
|------|------|------|------|------|
| 获取途径优化 | 获取途径优化 | 120px | Microsoft YaHei | #ffffff |
| 原流程： | 原流程： | 64px | Microsoft YaHei | #cfb796 |
| 基于资源的使用场景，优化玩家资源获取途径的导航--- 1.右上角货币栏--可购买类--仅提供直购路径。（其它获取途径根据情况，在界面单独增加曝光入口） 2. 不可购买类--提供主获取路径的跳转 | 基于资源的使用场景，优化玩家资源获取途径 | 64px | Microsoft YaHei | #ffffff |
| 方案方向确定： | 方案方向确定： | 64px | Microsoft YaHei | #ffffff |
| 2024-05-13 | 2024-05-13 | 48px | Microsoft YaHei | #f6f6f6 |
| UE: | UE:  | 48px | Microsoft YaHei | #ffffff |
| 王立哲 | 王立哲 | 48px | Microsoft YaHei | #ffffff |
| 策划: | 策划:  | 48px | Microsoft YaHei | #ffffff |
| ta的名字 | ta的名字 | 48px | Microsoft YaHei | #ffffff |
| 汇总右上角道具代币 | 汇总右上角道具代币 | 40px | Microsoft YaHei | #ffffff |
| 核心资源道具类 | 核心资源道具类 | 40px | Microsoft YaHei | #f8cf00 |
| 收集：招募令、皮肤包、锦囊袋、唤灵宝箱、将印宝箱、夺宝券、 养成：灵韵石、转生丹、进化灵石、功勋、朱砂、 牌局：手气卡、换将卡、鲜花、斗地主金豆、 | 收集：招募令、皮肤包、锦囊袋、唤灵宝箱、 | 40px | Microsoft YaHei | #ffffff |
| 获取途径： 1.主要：成长任务、战令任务、商城兑换、直购、 2.有活动时：限时活动任务、限时礼包、 | 获取途径：
1.主要：成长任务、战令任务 | 40px | Microsoft YaHei | #ffffff |
| 获取途径： 1.主要：限时活动任务、限时礼包、 2.部分有：成长任务、战令任务、商城兑换、直购、 | 获取途径：
1.主要：限时活动任务、限时 | 40px | Microsoft YaHei | #ffffff |
| 活动资源道具类 | 活动资源道具类 | 40px | Microsoft YaHei | #f8cf00 |
| 核心招募：祈福灯、纳贤令、锦绣、夺宝等 | 核心招募：祈福灯、纳贤令、锦绣、夺宝等 | 40px | Microsoft YaHei | #ffffff |
| 兑换：同心结、鼎、动态水晶、 | 兑换：同心结、鼎、动态水晶、 | 40px | Microsoft YaHei | #ffffff |
| 单一路径获得、掉落道具，不可直接购买 | 单一路径获得、掉落道具，不可直接购买 | 40px | Microsoft YaHei | #f8cf00 |
| 例如; 招募掉落的将符、锦绣掉落的绸缎、祈福掉落的同心结 | 例如; 招募掉落的将符、锦绣掉落的绸缎、 | 40px | Microsoft YaHei | #ffffff |
| 所有 不可点击资源，增加点击交互事件-弹出弹窗如下： | 所有 不可点击资源，增加点击交互事件-弹 | 40px | Microsoft YaHei | #f8cf00 |
| 点击前往招募，直接跳转至招募界面 | 点击前往招募，直接跳转至招募界面 | 40px | Microsoft YaHei | #f8cf00 |
| 获取路径说明格式：主要通过xxxx获取，其次，可在xxxx中获得 | 获取路径说明格式：主要通过xxxx获取， | 40px | Microsoft YaHei | #f8cf00 |
| 优化：道具仅在使用场景页面显示，活动主页面不显示 | 优化：道具仅在使用场景页面显示，活动主页 | 40px | Microsoft YaHei | #f8cf00 |
| 可直购类-- | 可直购类--
 | 40px | Microsoft YaHei UI | #ffffff |
| 未提供道具的 获取路径信息 绑元、招募令 弹两次窗口？ | 未提供道具的 获取路径信息
绑元、招募令 | 40px | Microsoft YaHei UI | #ffffff |
| 不可购买类--部分道具类 | 不可购买类--部分道具类 | 40px | Microsoft YaHei UI | #ffffff |
| 1.点击无反馈 2.作用与当前界面无关 | 1.点击无反馈
2.作用与当前界面无关 | 40px | Microsoft YaHei UI | #ffffff |
| 右上角资源路径导航问题 | 右上角资源路径导航问题 | 40px | Microsoft YaHei UI | #ffffff |
| 所有活动类-核心资源道具，增加获取途径文字说明， 说明主要获得途径，次要获得途径进行简单说明 | 所有活动类-核心资源道具，增加获取途径文 | 36px | Microsoft YaHei UI | #f2f2f2 |
| 所有掉落道具，配置道具使用说明，增加获取途径文字说明， 说明主要获得途径，次要获得途径进行简单说明 | 所有掉落道具，配置道具使用说明，增加获取 | 36px | Microsoft YaHei UI | #f2f2f2 |

### 4. 颜色规范

**常用颜色表**:
| 颜色值 | 用途 | 说明 |
|--------|------|------|
| #f6f6f6 | 2024-05-13 | 出现1次 |
| #ffffff | UE: | 出现55次 |
| #cfb796 | 原流程： | 出现1次 |
| #f8cf00 | 核心资源道具类 | 出现7次 |
| #6a3c22 | 抵价券 | 出现8次 |
| #c8a176 | 获取道具 | 出现5次 |
| #4d3528 | 纳贤令 | 出现5次 |
| #734d1f | 可在【纳贤】活动界面，进行武将抽取，使用后，可获得水晶碎片*2，且随机获得当前活动页面投放的武将之一。 | 出现10次 |
| #e76d01 | 获得途径：纳贤活动开启时，主要在【活动商城】中获得，另外可通过参与活动任务获得。 | 出现5次 |
| #c1ae8e | 1 | 出现2次 |

---


---

