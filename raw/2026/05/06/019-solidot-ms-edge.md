---
title: "MS Edge 被发现会在内存中明文加载所有密码"
source: Solidot
url: https://www.solidot.org/story?sid=84213
published: 2026-05-05T22:12:37+08:00
lang: zh
category: open_source_zh
fetched_at: 2026-05-06T00:30:09.891057+08:00
---

# MS Edge 被发现会在内存中明文加载所有密码

**来源**: Solidot | **发布**: 2026-05-05 | **链接**: https://www.solidot.org/story?sid=84213

## RSS 摘要

MS Edge 浏览器被发现启动时会在内存中明文加载其保存的所有密码。相比下 Chrome 只在需要时解密凭证，没有将所有密码保存在内存中。Edge 和 Chrome 都是基于开源的 Chromium。微软的做法让从内存中抓取重要数据变得更容易，也增加了共享环境下密码泄露的风险。安全研究人员将这一问题报告给了微软，收到的回应是该行为就是这么设计的。研究人员在 GitHub 上发布了概念演示工具 EdgeSavedPasswordsDumper。

## 正文

奇客Solidot | MS Edge 被发现会在内存中明文加载所有密码 登录 注册 文章 往日文章 往日投票 皮肤 蓝色 橙色 绿色 浅绿色 分类: 首页 Linux 科学 科技 移动 苹果 硬件 软件 安全 游戏 书籍 idle 云计算 高飞的电子替身 关注我们： solidot新版网站常见问题，请点击 这里 查看。 消息 本文已被查看 988 次 MS Edge 被发现会在内存中明文加载所有密码 Edwards (42866)发表于 2026年05月05日 22时12分 星期二 新浪微博分享 来自一九八四·上来透口气 MS Edge 浏览器被发现启动时会在内存中明文加载其保存的所有密码。相比下 Chrome 只在需要时解密凭证，没有将所有密码保存在内存中。Edge 和 Chrome 都是基于开源的 Chromium。微软的做法让从内存中抓取重要数据变得更容易，也增加了共享环境下密码泄露的风险。安全研究人员将这一问题报告给了微软，收到的回应是该行为就是这么设计的。研究人员在 GitHub 上发布了概念演示工具 EdgeSavedPasswordsDumper。 https://lemmy.zip/post/63729962?scrollToComments=true https://github.com/L1v1ng0ffTh3L4N/EdgeSavedPasswordsDumper/tree/main/EdgeSavedPasswordsDumper 回复 ﻿ 在所有的禁欲道德里，人把自己的一部分视为神，加以崇拜，因此被迫把其他部分加以恶魔化。——尼采 首页 至顶网 往日文章 过去的投票 编辑介绍 隐私政策 使用条款 网站介绍 RSS 本站提到的所有注册商标属于他们各自的所有人所有，评论属于其发表者所有，其余内容版权属于 solidot.org(2009- ) 所有 。 京ICP证161336号&nbsp;&nbsp;&nbsp;&nbsp; 京ICP备15039648号-15 北京市公安局海淀分局备案号：11010802021500 举报电话：010-62641205 涉未成年人举报专线：010-62641208 举报邮箱：jubao@zhiding.cn 网上有害信息举报专区： https://www.12377.cn
