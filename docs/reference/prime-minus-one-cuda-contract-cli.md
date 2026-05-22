# Prime-Minus-One CUDA Contract CLI

Stage 5Z commands are available under:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-contract --help
```

Main commands:

- `build-contract-records`
- `build-kernel-abi`
- `build-host-runner-contract`
- `build-buffer-contract`
- `build-validation-vectors`
- `build-future-parity-plan`
- `build-result-store-compatibility`
- `build-full-p56-blocker`
- `build-scored-experiment-deferral`
- `build-implementation-readiness-gate`
- `build-next-stage-decision`
- `build-summary`
- `validate-stage5z`
- `summary`

The commands write compact committed YAML records plus ignored JSON reports. They do not run CUDA or native parity.
