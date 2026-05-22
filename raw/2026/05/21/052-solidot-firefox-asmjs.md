---
title: "Firefox 将移除 asm.js 相关代码"
source: Solidot
url: https://www.solidot.org/story?sid=84356
published: 2026-05-20T23:39:42+08:00
lang: zh
category: open_source_zh
fetched_at: 2026-05-21T00:30:24.040584+08:00
---

# Firefox 将移除 asm.js 相关代码

**来源**: Solidot | **发布**: 2026-05-20 | **链接**: https://www.solidot.org/story?sid=84356

## RSS 摘要

Mozilla 宣布 Firefox 未来将移除 asm.js 相关代码，因为它早有了后继者 WebAssembly，同时维护两者耗费时间且增加攻击面。asm.js 是 Mozilla 对 NaCl 和 PNaCl 的回应：通过选择一个严格静态的 JavaScript 子集获得类似 NaCl/PNaCl 的性能，同时代码又能直接运行在 Web 内容中。asm.js 于 2013 年随 Firefox 22 发布，获得了巨大的成功，证明只使用 Web 技术就能在 Web 上以接近原生的速度运行代码，它为 WebAssembly 的诞生铺平了道路，WebAssembly 在 2019 年成为 W3C 标准。Mozilla 从 Firefox 148 开始 JS 引擎 SpiderMonkey 默认禁用 asm.js 优化，未来版本将完全移除相关代码，使用 asm.js 的网站不会受到影响，开发者建议想要继续使用 asm.js 发布内容的网站重编译到 WebAssembly，它的执行速度更快，二进制文件更小。

## 正文

奇客Solidot | Firefox 将移除 asm.js 相关代码 登录 注册 文章 往日文章 往日投票 皮肤 蓝色 橙色 绿色 浅绿色 分类: 首页 Linux 科学 科技 移动 苹果 硬件 软件 安全 游戏 书籍 idle 云计算 高飞的电子替身 关注我们： solidot新版网站常见问题，请点击 这里 查看。 消息 本文已被查看 442 次 Firefox 将移除 asm.js 相关代码 Edwards (42866)发表于 2026年05月20日 23时39分 星期三 新浪微博分享 来自快乐基因 Mozilla 宣布 Firefox 未来将移除 asm.js 相关代码，因为它早有了后继者 WebAssembly，同时维护两者耗费时间且增加攻击面。asm.js 是 Mozilla 对 NaCl 和 PNaCl 的回应：通过选择一个严格静态的 JavaScript 子集获得类似 NaCl/PNaCl 的性能，同时代码又能直接运行在 Web 内容中。asm.js 于 2013 年随 Firefox 22 发布，获得了巨大的成功，证明只使用 Web 技术就能在 Web 上以接近原生的速度运行代码，它为 WebAssembly 的诞生铺平了道路，WebAssembly 在 2019 年成为 W3C 标准。Mozilla 从 Firefox 148 开始 JS 引擎 SpiderMonkey 默认禁用 asm.js 优化，未来版本将完全移除相关代码，使用 asm.js 的网站不会受到影响，开发者建议想要继续使用 asm.js 发布内容的网站重编译到 WebAssembly，它的执行速度更快，二进制文件更小。 https://spidermonkey.dev/blog/2026/05/20/saying-goodbye-to-asmjs.html 回复 ﻿ 你不问我，我就不会说谎话。 首页 至顶网 往日文章 过去的投票 编辑介绍 隐私政策 使用条款 网站介绍 RSS 本站提到的所有注册商标属于他们各自的所有人所有，评论属于其发表者所有，其余内容版权属于 solidot.org(2009- ) 所有 。 京ICP证161336号&nbsp;&nbsp;&nbsp;&nbsp; 京ICP备15039648号-15 北京市公安局海淀分局备案号：11010802021500 举报电话：010-62641205 涉未成年人举报专线：010-62641208 举报邮箱：jubao@zhiding.cn 网上有害信息举报专区： https://www.12377.cn
