from libreprimus.token_block.preflight_runner import Stage5BDPreflightRunner
from libreprimus.token_block.stage5bb import ExecutionBlockedError


def test_stage5bd_preflight_runner_execution_methods_fail_closed() -> None:
    runner = Stage5BDPreflightRunner()

    try:
        runner.generate_real_token_block_byte_stream()
    except ExecutionBlockedError as exc:
        assert "dry-run only" in str(exc)
    else:
        raise AssertionError("expected dry-run byte generation to be blocked")
