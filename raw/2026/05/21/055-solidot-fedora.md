---
title: "Fedora 移除深度桌面环境包"
source: Solidot
url: https://www.solidot.org/story?sid=84353
published: 2026-05-20T18:43:22+08:00
lang: zh
category: open_source_zh
fetched_at: 2026-05-21T00:30:24.158192+08:00
---

# Fedora 移除深度桌面环境包

**来源**: Solidot | **发布**: 2026-05-20 | **链接**: https://www.solidot.org/story?sid=84353

## RSS 摘要

在 openSUSE 之后，Fedora 发行版移除了深度桌面环境包（Deepin Desktop）。2025 年初 SUSE 安全团队在一次例行审查中发现深度桌面环境有名叫 deepin-feature-enable 的软件包，该软件包是在 2021 年 4 月加入的，并没有咨询或通知 SUSE，它包含了一个“许可协议对话框（license agreement dialog）”，基本上说讲因为 openSUSE 的安全规定，它禁用了 deepin-api 和 deepin-daemon 需要的所有 dbus 和 polkit 功能，这可能导致 Deepin Desktop 不能正常工作，部分功能无效。如果用户不在意这些安全问题，可选择点击确认，之后会自动安装缺少的 dbus 和 polkit。安全团队的调查发现，deepin-daemon 中的核心组件从未递交进行安全审查，它们被悄悄的引入到了 openSUSE 中。鉴于 Deepin 社区过去几年多次违规，openSUSE 决定移除 Deepin Desktop。Fedora 项目随后也对深度桌面环境包展开安全审查，期间开发者发现难

## 正文

奇客Solidot | Fedora 移除深度桌面环境包 登录 注册 文章 往日文章 往日投票 皮肤 蓝色 橙色 绿色 浅绿色 分类: 首页 Linux 科学 科技 移动 苹果 硬件 软件 安全 游戏 书籍 idle 云计算 高飞的电子替身 关注我们： solidot新版网站常见问题，请点击 这里 查看。 消息 本文已被查看 757 次 Fedora 移除深度桌面环境包 Wilson (42865)发表于 2026年05月20日 18时43分 星期三 新浪微博分享 来自基因先知者 在 openSUSE 之后，Fedora 发行版移除了深度桌面环境包（Deepin Desktop）。2025 年初 SUSE 安全团队在一次例行审查中发现深度桌面环境有名叫 deepin-feature-enable 的软件包，该软件包是在 2021 年 4 月加入的，并没有咨询或通知 SUSE，它包含了一个“许可协议对话框（license agreement dialog）”，基本上说讲因为 openSUSE 的安全规定，它禁用了 deepin-api 和 deepin-daemon 需要的所有 dbus 和 polkit 功能，这可能导致 Deepin Desktop 不能正常工作，部分功能无效。如果用户不在意这些安全问题，可选择点击确认，之后会自动安装缺少的 dbus 和 polkit。安全团队的调查发现，deepin-daemon 中的核心组件从未递交进行安全审查，它们被悄悄的引入到了 openSUSE 中。鉴于 Deepin 社区过去几年多次违规，openSUSE 决定移除 Deepin Desktop。Fedora 项目随后也对深度桌面环境包展开安全审查，期间开发者发现难以联系部分深度软件包的维护者，因为安全担忧和软件包缺乏维护，它最终决定移除深度桌面环境。 https://pagure.io/fesco/issue/3409 https://www.phoronix.com/news/Fedora-Removing-Deepin 回复 ﻿ 在b进位制中，以数n起头的数出现的机率为logb(n + 1) − logb(n)--本福特定律 首页 至顶网 往日文章 过去的投票 编辑介绍 隐私政策 使用条款 网站介绍 RSS 本站提到的所有注册商标属于他们各自的所有人所有，评论属于其发表者所有，其余内容版权属于 solidot.org(2009- ) 所有 。 京ICP证161336号&nbsp;&nbsp;&nbsp;&nbsp; 京ICP备15039648号-15 北京市公安局海淀分局备案号：11010802021500 举报电话：010-62641205 涉未成年人举报专线：010-62641208 举报邮箱：jubao@zhiding.cn 网上有害信息举报专区： https://www.12377.cn
