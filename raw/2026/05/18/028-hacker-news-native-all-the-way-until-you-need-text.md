---
title: "Native all the way, until you need text"
source: Hacker News
url: https://justsitandgrin.im/posts/native-all-the-way-until-you-need-text/
published: 2026-05-17T19:49:46+08:00
lang: en
category: community
fetched_at: 2026-05-18T00:30:14.071915+08:00
---

# Native all the way, until you need text

**来源**: Hacker News | **发布**: 2026-05-17 | **链接**: https://justsitandgrin.im/posts/native-all-the-way-until-you-need-text/

## RSS 摘要

Comments

## 正文

I have been a native macOS / iOS developer for almost twenty years, and I want to say something about the usual “Oh, it is Node / Electron again… what a shame…” reaction. Recently, I tried to implement a simple chat with Markdown support in a pure Swift / SwiftUI app. And honestly, it is almost funny how immature all these “native” things still are when you step outside simple screens. Yes, you can achieve reasonable performance in SwiftUI. You can even convince yourself that jumpy scrolling is fine, and that a few lags here &#x26; there are acceptable. But then you want to select a whole Markdown document built from SwiftUI primitives, and you just cannot. By design. So, being smart &#x26; experienced, you move to NSTextView . It even supports TextKit 2 now. Great. Except now you lose most of the testing &#x26; performance work you had around SwiftUI, because it does not play well with it. Then you try to stream text into it, because it is 2026 &#x26; everyone streams responses from models now, and you start seeing CPU spikes. Fine. We still have AppKit. We still have NSCollectionView . Mature, performant, battle-tested. So you switch again, implement the whole thing, and on the second day you realise the cells will blink no matter what. By design. Then you even consider going lower-level with pure TextKit 2. You make a prototype. Performance is okay. Streaming is still terrible. It does not play well with anything modern. You remove SwiftUI completely, stick with AppKit, and start fighting expanding text chunks manually. At this point almost everything is broken, but hey, you can select the text! Then you realise it will take months just to reach feature parity with basic native macOS behaviour: context menus, dictionary lookup, selection, accessibility, text interactions, all the small things users expect without thinking about them. So you try WebKit to render Markdown. And it works. There are caveats, of course, but mostly it just works. Performance is good. Typography is almost perfect. You have a proper level of control. And then, at the darkest possible moment, you think: okay, let’s generate a simple Electron project. You go to the dark side. And you are amazed. Text operations, Markdown rendering, good typography – all of it works out of the box, with performance you could not get even from your pure TextKit 2 implementation. macOS integrations are there too. You can even render fancy Git diffs with a few lines of code. I am not even talking about things like diffs.com . And then you ask yourself: what went wrong? I did everything people say you should do. Native all the way. I know the platform. I know the options. I know SwiftUI, AppKit, TextKit, WebKit. But I still cannot make a simple thing work properly: a chat with Markdown &#x26; the ability to select a whole message. And suddenly it becomes much clearer why most new chat-heavy apps that depend on one of the most important interface patterns of this era – chat, long-form rich text, flexible typography – are web-based in one way or another. There is no real alternative. SwiftUI is fine for simple screens, preferably without too much scrolling. Swift is still great for performance-critical parts. But you can get most of that performance from Electron or React Native almost for free with the native interoperability, while keeping a much better text &#x26; rendering model. So this is not even a “quick solution vs proper solution” debate anymore. If you want to build rich text rendering for long-form chats, SwiftUI &#x26; Apple’s native SDKs are not helping you. They stop being an advantage &#x26; start becoming constraints. P.S. Discussion on Hacker News
