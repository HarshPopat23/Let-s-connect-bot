---
title: Contributing to Kubeflow Projects
category: ecosystems
source_url: https://www.kubeflow.org/docs/about/contributing/
updated: 2026-09-04
---

# Understand Kubeflow first

Kubeflow is an ecosystem of projects for machine learning workflows on Kubernetes. Work is distributed across several repositories and working groups. Identify the exact component, such as Pipelines, Trainer, Katib, Notebooks or the website, before choosing an issue.

# Find the responsible repository and group

Start from the Kubeflow website and GitHub organization. Read the component repository's README, CONTRIBUTING guide, owners files, development setup and issue templates. Join the relevant community meeting or channel and use public discussion.

Kubeflow's current contributor guide requires Developer Certificate of Origin sign-off. Membership is not required to contribute.

# Confirm issues and design

Search for existing issues and pull requests. For behavioral changes, open or confirm an issue and discuss the approach before a large implementation. Kubeflow components interact with Kubernetes APIs and versioned interfaces, so compatibility and upgrade behavior matter.

The current general Kubeflow guide asks contributors to self-assign an available issue with `/assign` before starting. A statement of interest without assignment does not reserve it. Coordinate with an existing assignee and ask a maintainer about reassignment after sustained inactivity rather than creating a duplicate pull request.

# Test realistically

Run component unit tests and formatting. When the change touches Kubernetes behavior, add appropriate controller, integration or end-to-end coverage as required by the repository. Document limitations if you cannot run an expensive test locally, but do not claim it passed.

# Review and ownership

Kubeflow uses OWNERS files for scoped reviewer and approver responsibility and a two-phase review process similar to Kubernetes. Owners and approvers may request architectural sequencing across repositories. A useful change can be delayed until prerequisites merge. Follow the requested sequence and avoid combining integration, policy and user-interface changes into one pull request when reviewers ask for separation.

# Mentorship warning

Kubeflow's participation in any mentorship program must be verified for the current cycle. Contributing to Kubeflow is valuable independently of GSoC or LFX selection.
