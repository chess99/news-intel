---
title: "GitHub Actions: Upcoming image migrations"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-14-github-actions-upcoming-image-migrations
published: 2026-05-15T02:31:34+08:00
lang: en
category: platform
fetched_at: 2026-05-16T00:30:27.100711+08:00
---

# GitHub Actions: Upcoming image migrations

**来源**: GitHub Changelog | **发布**: 2026-05-15 | **链接**: https://github.blog/changelog/2026-05-14-github-actions-upcoming-image-migrations

## RSS 摘要

There are two upcoming image migrations customers should be aware of, and GitHub is transitioning to owning the Arm64 images for hosted runners. Arm64 runner images now maintained by GitHub&#8230; The post GitHub Actions: Upcoming image migrations appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement May 14, 2026 • 2 minute read GitHub Actions: Upcoming image migrations Table of Contents Arm64 runner images now maintained by GitHub Windows 2025 Visual Studio 2026 image migration macos-latest migration begins June 15 Menu. Currently selected: Arm64 runner images now maintained by GitHub Arm64 runner images now maintained by GitHub Windows 2025 Visual Studio 2026 image migration macos-latest migration begins June 15 There are two upcoming image migrations customers should be aware of, and GitHub is transitioning to owning the Arm64 images for hosted runners. Arm64 runner images now maintained by GitHub GitHub now owns and maintains the Arm64 runner images for GitHub Actions hosted runners. These images were previously maintained by Arm Limited, LLC and are now fully managed by GitHub. No action is required from users as part of this transition. What&rsquo;s changing Windows 11 Arm ( windows-11-arm ) images have already transitioned to GitHub-managed builds and pipelines. Ubuntu 24.04 ( ubuntu-24.04-arm ) and Ubuntu 22.04 ( ubuntu-22.04-arm ) images are being migrated to GitHub&rsquo;s internal pipelines. During the transition, these images won&rsquo;t receive updates, and no new release notes will appear in the actions/runner-images repository for them. The actions/partner-runner-images repository will be archived after the transition is complete. All open issues and future support will move to actions/runner-images . What&rsquo;s not changing Image functionality and compatibility remain exactly the same. No packages are being added or removed as part of this transition. No breaking changes will be introduced during the migration period. If you encounter a critical issue with the Ubuntu Arm64 images during the transition, such as a CVE or vulnerability, open an issue in the actions/runner-images repository. Windows 2025 Visual Studio 2026 image migration The windows-latest and windows-2025 labels in GitHub Actions will be migrated to use Visual Studio 2026 by default. This change will be rolled out over a week beginning June 8, 2026 and will complete by June 15, 2026. If you want to test the new image, update the runs-on: target in your YAML workflow file to the new label windows-2025-vs2026 . Note: This label is meant for testing only. After the migration, this label will point to the windows-2025 image. If you want to remain on VS 2022, update the runs-on: target in your YAML workflow file to windows-2022 . For more information, or if you have questions, head to the runner-images repository . macos-latest migration begins June 15 The macos-latest image label migration will begin June 15 and take 30 days to complete. The macos-latest image label will point to the macOS 26 image instead of macOS 15. During the migration, users should expect to see their workflows begin running on the macOS 26 image. To continue using macOS 15, you can target the macos-15 label directly. For questions, or more information, head to the runner-images repository . Table of Contents Arm64 runner images now maintained by GitHub Windows 2025 Visual Studio 2026 image migration macos-latest migration begins June 15 Menu. Currently selected: Arm64 runner images now maintained by GitHub Arm64 runner images now maintained by GitHub Windows 2025 Visual Studio 2026 image migration macos-latest migration begins June 15 actions Share Copied Shared Back to changelog
