# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
