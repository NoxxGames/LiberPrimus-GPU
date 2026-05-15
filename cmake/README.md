# cmake

## Purpose

Shared CMake helper modules live here.

## What belongs here

Project options, warning settings, CUDA configuration helpers, and future reusable CMake functions.

## What does not belong here

Generated CMake cache files, build directories, downloaded dependencies, or toolchain installers.

## Codex modification policy

Codex may modify these files when build behavior changes, but should keep options conservative and documented.

## Stage 0A restrictions

Only scaffold build helpers are present. No third-party dependency fetching is allowed in Stage 0A.
