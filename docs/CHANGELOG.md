# Changelog

> Historical development record. For current usage, start with the [documentation index](README.md); for the workbench implementation and local verification, see [Workbench status](WORKBENCH-STATUS.md).

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added the local workbench, saved recipes, checkpointed runs, review pauses, and the authored Moon walkthrough.
- Added in-app Guides, Markdown and JSON exports, and additive ZIP workspace backups.
- Added offline practice for decision memos, evidence briefs, and document reviews, with a fixed source packet and editable handoffs.
- Added Chain Lab with offline starter missions, interactive token attachments (`[Goal]`, `[Clues]`, `[Answer N]`), human-answered runs, and remixing.
- Added Classroom Challenges (Rainy Recess, Missing Mascot, Paper Bridge) and Dragon Challenge ("Build the next prompt") with prepared comparisons.
- Added dedicated everyday recipes and discovery paths for kids, parents/caregivers, and teachers.
- Added strict same-origin request boundary protection and origin-checking on local mutations.

## [0.2.0] - 2025-12-05

### Phase 4: Polish
- [x] Build CLI interface for easy use
- [x] Add batch generation capability
- [x] Integrate SEO optimization step
- [x] Create "content calendar" generator
- [x] Write documentation

### Added
- **MS Blog Content Tools**: A complete suite of tools for generating high-quality, accessible blog content.
    - **Prompt Card Generator**: Creates structured prompt cards with problem statements, examples, and variations.
    - **Shortcut Spotlight Generator**: Generates accessibility-focused tool tutorials.
    - **Multi-Phase Guide Generator**: Creates comprehensive system setup guides with "Quick Path" options.
    - **Content Idea Expander**: Brainstorms content ideas across multiple formats from a single seed.
    - **Low-Energy Content Pipeline**: A master tool that auto-detects the best format for a given problem and generates publication-ready content.
- **Documentation**:
    - `QUICKSTART.md`: New 5-minute getting started guide.
    - `ARCHITECTURE.md`: Detailed 6-layer system architecture documentation.
    - `tools/ms_blog/README.md`: Comprehensive documentation for the new blog tools.

### Changed
- Updated `README.md` to reflect the new architecture and tools.
- Updated `IDEAS.md` to mark implemented features as complete.

## [0.1.0] - 2025-12-04

### Added
- **Core Framework**:
    - `MinimalChainable`: The base class for sequential prompt chaining.
    - `ArtifactStore`: Persistent knowledge management system.
    - `ChainComposer`: Orchestration engine for multi-tool workflows.
    - `MetaChainGenerator`: Self-improving system that designs its own chains.
- **Tools**:
    - `concept_simplifier`: Educational tool for breaking down complex topics.
    - `subject_connector`: Tool for finding connections between disparate subjects.
