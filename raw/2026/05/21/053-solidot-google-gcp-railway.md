---
title: "Google 云服务 GCP 不小心将其大客户 Railway 的账号封禁"
source: Solidot
url: https://www.solidot.org/story?sid=84355
published: 2026-05-20T21:51:47+08:00
lang: zh
category: open_source_zh
fetched_at: 2026-05-21T00:30:24.021010+08:00
---

# Google 云服务 GCP 不小心将其大客户 Railway 的账号封禁

**来源**: Solidot | **发布**: 2026-05-20 | **链接**: https://www.solidot.org/story?sid=84355

## RSS 摘要

2024 年 Google 云服务 GCP 的错误配置导致澳大利亚退休基金管理公司 UniSuper 的数据被完全删除，幸运的是 UniSuper 在另一家公司有备份。这起事故导致 UniSuper 下线了一周多时间。2026 年 5 月 19 日 GCP 发生了一起类似的严重事故，它的自动系统将其大客户、PaaS 平台 Railway.com 的生产账号给封了，导致 Railway 的服务下线，根据 Railway 官方博客的事故报告，宕机持续了大约 8 个小时。账号封禁发生在 19 日 22:10 UTC，导致 Railway 失去了 GCP 相关的基础设施，这些基础设施支持了控制面板、API 以及部分网络基础设施。Railway 立即联系了 GCP 的客户经理，22:29 UTC 账号恢复，但计算实例、磁盘以及网络都需要逐个慢慢恢复，直到第二天 07:58 UTC 事故才完全解决。Railway 宣布将降低对 GCP 的依赖，计划将 GCP 从热路径中移除，保留作为备份/故障转移服务。

## 正文

奇客Solidot | Google 云服务 GCP 不小心将其大客户 Railway 的账号封禁 登录 注册 文章 往日文章 往日投票 皮肤 蓝色 橙色 绿色 浅绿色 分类: 首页 Linux 科学 科技 移动 苹果 硬件 软件 安全 游戏 书籍 idle 云计算 高飞的电子替身 关注我们： solidot新版网站常见问题，请点击 这里 查看。 消息 本文已被查看 843 次 Google 云服务 GCP 不小心将其大客户 Railway 的账号封禁 Edwards (42866)发表于 2026年05月20日 21时51分 星期三 新浪微博分享 来自凡尔纳地球三部曲 2024 年 Google 云服务 GCP 的错误配置导致澳大利亚退休基金管理公司 UniSuper 的数据被完全删除，幸运的是 UniSuper 在另一家公司有备份。这起事故导致 UniSuper 下线了一周多时间。2026 年 5 月 19 日 GCP 发生了一起类似的严重事故，它的自动系统将其大客户、PaaS 平台 Railway.com 的生产账号给封了，导致 Railway 的服务下线，根据 Railway 官方博客的事故报告，宕机持续了大约 8 个小时。账号封禁发生在 19 日 22:10 UTC，导致 Railway 失去了 GCP 相关的基础设施，这些基础设施支持了控制面板、API 以及部分网络基础设施。Railway 立即联系了 GCP 的客户经理，22:29 UTC 账号恢复，但计算实例、磁盘以及网络都需要逐个慢慢恢复，直到第二天 07:58 UTC 事故才完全解决。Railway 宣布将降低对 GCP 的依赖，计划将 GCP 从热路径中移除，保留作为备份/故障转移服务。 https://blog.railway.com/p/incident-report-may-19-2026-gcp-account-outage 回复 ﻿ 世间最庄严的问题是：我能做什么好事？ 首页 至顶网 往日文章 过去的投票 编辑介绍 隐私政策 使用条款 网站介绍 RSS 本站提到的所有注册商标属于他们各自的所有人所有，评论属于其发表者所有，其余内容版权属于 solidot.org(2009- ) 所有 。 京ICP证161336号&nbsp;&nbsp;&nbsp;&nbsp; 京ICP备15039648号-15 北京市公安局海淀分局备案号：11010802021500 举报电话：010-62641205 涉未成年人举报专线：010-62641208 举报邮箱：jubao@zhiding.cn 网上有害信息举报专区： https://www.12377.cn
