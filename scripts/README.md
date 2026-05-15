# scripts

## Purpose

Windows PowerShell helpers for toolchain verification, bootstrap, configure, and cleanup.

## What belongs here

Small checked-in scripts that are safe to inspect and run locally.

## What does not belong here

Downloaded installers, generated logs, build outputs, or scripts from unverified third-party URLs.

## Codex modification policy

Codex may modify scripts to improve safety, detection, and reproducibility.

## Stage 0A restrictions

Scripts must not modify Git remotes, delete data directories, run long benchmarks, or install CUDA drivers automatically.
