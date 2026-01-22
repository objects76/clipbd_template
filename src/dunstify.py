import shutil
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass
class NotifyResult:
    """Result of a dunstify call."""

    returncode: int
    stdout: str
    stderr: str
    notify_id: int | None = None  # from --printid (or replace-id echo-back)
    chosen_action: str | None = None  # from --action when user clicks


class DunstifyError(RuntimeError):
    pass


class Dunstify:
    """
    Thin Python wrapper for `dunstify`.

    Key features supported:
      - urgency (low|normal|critical)
      - timeout (ms)
      - icon path/name
      - hints (BOOLEAN/INT/DOUBLE/STRING etc.)
      - progress via hint `int:value:...`
      - actions with labels; prints chosen action to stdout
      - replace existing notification by ID
      - app name, category
      - wait for close/expire (blocks until notification done)
    """

    def __init__(self, binary: str = "dunstify") -> None:
        self.binary = binary
        if not shutil.which(self.binary):
            raise DunstifyError(
                f"`{self.binary}` not found on PATH. Install dunst (which provides dunstify) "
                "and ensure the notification daemon (dunst) is running."
            )
        self.notify_id = None

    @staticmethod
    def _hint_tuple_to_str(k: str, v: bool | float | str | bytes) -> str:
        # Map Python types to dunstify hint TYPE:NAME:VALUE
        if isinstance(v, bool):
            t = "boolean"
            val = "true" if v else "false"
        elif isinstance(v, int):
            t = "int"
            val = str(v)
        elif isinstance(v, float):
            t = "double"
            val = str(v)
        elif isinstance(v, bytes):
            t = "byte"
            val = v.hex()
        else:
            t = "string"
            val = str(v)
        return f"{t}:{k}:{val}"

    def cont(self, summary: str, body: str | None = None, **kwargs) -> NotifyResult:
        kwargs["replace_id"] = self.notify_id
        return self.send(summary, body, **kwargs)

    def close(self, notify_id: int | None = None):
        notify_id = notify_id or self.notify_id
        args: list[str] = [self.binary, "--close", str(notify_id)]
        subprocess.run(args, capture_output=False, text=True)

    def send(
        self,
        summary: str,
        body: str | None = None,
        *,
        urgency: str | None = None,  # "low"|"normal"|"critical"
        timeout_ms: int | None = None,  # may be overridden by daemon config
        icon: str | None = None,
        app_name: str | None = None,
        category: str | None = None,
        hints: Mapping[str, bool | int | float | str | bytes] | None = None,
        actions: Mapping[str, str] | None = None,  # {"action_key": "Button Label", ...}
        replace_id: int | None = None,
        wait: bool = False,  # block until closed/expired
        print_id: bool = True,  # capture notify id
        extra_args: Sequence[str] | None = None,
        check: bool = False,  # raise on non-zero exit
    ) -> NotifyResult:
        args: list[str] = [self.binary]

        if app_name:
            args += ["--appname", app_name]
        if urgency:
            if urgency not in {"low", "normal", "critical"}:
                raise ValueError("urgency must be one of: low, normal, critical")
            args += ["--urgency", urgency]
        if timeout_ms is not None:
            args += ["--timeout", str(timeout_ms)]
        if icon:
            args += ["--icon", icon]
        if category:
            # dunstify forwards category to the server (same semantics as notify-send)
            args += ["--category", category]
        if hints:
            for k, v in hints.items():
                args += ["--hints", self._hint_tuple_to_str(k, v)]
        if actions:
            # One or more --action=KEY,LABEL (ArchWiki / docs)
            for key, label in actions.items():
                args += [f"--action={key},{label}"]
        if replace_id is not None:
            args += ["--replace", str(replace_id)]
        # if wait:
        #     args.append("--wait")
        if print_id:
            args.append("--printid")
        if extra_args:
            args += list(extra_args)

        args.append(summary)
        if body:
            args.append(body)

        print("subprocess.run", args)

        proc = subprocess.run(args, capture_output=True, text=True)
        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()

        # Heuristics:
        chosen_action = None
        notify_id: int | None = None

        # When actions are used, dunst prints the chosen action key to stdout.
        # When --printid is used, dunstify prints the id to stdout.
        # If both are present, action is printed AFTER the id (docs/guides).
        # We'll parse the last line if it's non-numeric as action; first numeric as id.
        if stdout:
            lines = [line.strip() for line in stdout.splitlines() if line.strip()]
            # first numeric token -> id
            for token in lines:
                if token.isdigit():
                    self.notify_id = int(token)
                    break
            # last non-digit -> action
            if lines and not lines[-1].isdigit():
                chosen_action = lines[-1]

        result = NotifyResult(
            returncode=proc.returncode,
            stdout=stdout,
            stderr=stderr,
            notify_id=self.notify_id,
            chosen_action=chosen_action,
        )

        if check and proc.returncode != 0:
            raise DunstifyError(
                f"dunstify failed (code {proc.returncode}). stderr:\n{stderr}"
            )
        return result

    # Convenience helpers

    def progress(
        self,
        summary: str,
        value: int,
        body: str | None = None,
        **kwargs,
    ) -> NotifyResult:
        """Show a progress-style notification using the `int:value` hint."""
        hints = dict(kwargs.pop("hints", {}) or {})
        hints.setdefault("value", int(value))  # dunst expects 'int:value:N'
        return self.send(summary, body, hints=hints, **kwargs)

    def critical(self, summary: str, body: str | None = None, **kwargs) -> NotifyResult:
        return self.send(summary, body, urgency="critical", **kwargs)

    def ask(
        self,
        summary: str,
        body: str | None = None,
        *,
        options: Mapping[str, str],  # {"yes": "확인", "no": "취소"}
        **kwargs,
    ) -> NotifyResult:
        """Prompt the user with action buttons and return the chosen action key."""
        # dunstify --action="yes,OK" --action="no,CANCEL" "질문" "원하는 옵션을 선택하세요"
        return self.send(summary, body, actions=options, **kwargs)


_notify = None


def notify_send(title: str, body: str | None = None, **kwargs):
    global _notify
    _notify = Dunstify()
    _notify.send(title, body, **kwargs)


def notify_cont(title: str, body: str | None = None, **kwargs):
    if _notify:
        _notify.cont(title, body, **kwargs)


def notify_close(notify_id: int | None = None):
    if _notify:
        _notify.close(notify_id)


import os
import sys
import time


def require_gui():
    # dunst는 GUI 세션과 DBus가 필요합니다.
    # Wayland/X11 환경 모두에서 동작하지만, 세션이 없으면 테스트를 중단합니다.
    if "DISPLAY" not in os.environ and "WAYLAND_DISPLAY" not in os.environ:
        print("No DISPLAY or WAYLAND_DISPLAY. Run this inside a desktop session.")
        sys.exit(1)


def test_basic(client: Dunstify):
    print("[basic] 기본 알림 테스트")
    res = client.send("테스트: 기본 알림", "본문입니다.", icon="dialog-information")
    print("  -> returncode:", res.returncode, "id:", res.notify_id)


def test_urgency(client: Dunstify):
    print("[urgency] 긴급도 테스트 (critical)")
    res = client.critical("테스트: 긴급", "사용자가 닫을 때까지 유지될 수 있습니다.")
    print("  -> returncode:", res.returncode, "id:", res.notify_id)


def test_replace(client: Dunstify):
    print("[replace] 같은 알림을 업데이트하여 교체")
    first = client.send("진행 상태", "초기화 중…", print_id=True, timeout_ms=5000)
    print("  -> first id:", first.notify_id)
    time.sleep(1.0)
    client.cont("진행 상태", "50% 완료")
    time.sleep(1.0)
    client.cont("진행 상태", "완료!")
    print("  -> replaced id:", first.notify_id)
    time.sleep(1.0)
    client.close()


def test_progress(client: Dunstify):
    print("[progress] 힌트(int:value)로 진행률 표시")
    for v in (10, 30, 60, 90, 100):
        client.progress("다운로드 중…", value=v, body=f"{v}% 완료", timeout_ms=1500)
        time.sleep(0.9)


def test_actions(client: Dunstify):
    print("[actions] 액션 버튼 테스트: 확인/취소")
    options: dict[str, str] = {"ok": "확인", "cancel": "취소"}
    res = client.ask(
        "선택해주세요",
        "버튼을 클릭하면 stdout으로 액션 키가 반환됩니다.",
        options=options,
        wait=True,  # 사용자가 닫거나 만료될 때까지 블록
        timeout_ms=15000,  # 15초 내 선택하지 않으면 만료
    )
    print("  -> chosen_action:", res.chosen_action, "id:", res.notify_id)


def test_wait_and_printid(client: Dunstify):
    print("[wait/printid] 알림이 닫힐 때까지 대기 & ID 출력")
    res = client.send(
        "대기 테스트", "3초 타임아웃 후 종료", wait=True, timeout_ms=3000, print_id=True
    )
    print("  -> waited. id:", res.notify_id)


def main():
    require_gui()
    client = Dunstify()  # PATH에서 dunstify 확인

    # 개별 테스트 실행
    # test_basic(client)
    # test_urgency(client)

    test_replace(client)
    # test_progress(client)

    # test_actions(client)
    # test_wait_and_printid(client)

    print(
        "\n모든 테스트가 실행되었습니다. 화면의 알림과 터미널 출력을 함께 확인하세요."
    )


if __name__ == "__main__":
    main()
