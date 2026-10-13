# Humanizer

A text humanization service that transforms AI-generated prose into 
natural-sounding writing using a hybrid approach of deterministic 
analysis and LLM-powered rewriting.

## Features

- Configurable "naturalness dial" (0-100)
- Detects and replaces AI-isms
- Analyzes sentence variance and repetition
- Preserves semantic meaning
- Iterative refinement until targets met
- Genre-aware presets

## Installation

```bash
pip install -e .