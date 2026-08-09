"""Standalone Tkinter GUI for previewing and testing every automation action.

Run from the repository root with::

    python automation_test_gui.py
"""

from __future__ import annotations

import queue
import sys
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


# Allow this file to run directly without installing the package.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from social_media_automation.actions import ACTIONS  # noqa: E402
from social_media_automation.config import Settings  # noqa: E402
from social_media_automation.integrations import AniListClient  # noqa: E402
from social_media_automation.models import Post  # noqa: E402
from social_media_automation.providers import FacebookPageProvider  # noqa: E402


class AutomationTestGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Social Media Automation Tester")
        self.geometry("900x650")
        self.minsize(720, 500)

        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.action_vars = {
            name: tk.BooleanVar(value=True) for name in sorted(ACTIONS)
        }
        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()
        self.after(100, self._process_events)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        actions = ttk.LabelFrame(outer, text="Automations", padding=10)
        actions.pack(fill="x")
        for column, (name, variable) in enumerate(self.action_vars.items()):
            ttk.Checkbutton(actions, text=name, variable=variable).grid(
                row=0, column=column, padx=(0, 18), sticky="w"
            )

        controls = ttk.Frame(outer, padding=(0, 10))
        controls.pack(fill="x")
        self.preview_button = ttk.Button(
            controls, text="Preview Selected", command=self.preview_selected
        )
        self.preview_button.pack(side="left", padx=(0, 8))
        self.publish_button = ttk.Button(
            controls, text="Publish Selected to Facebook", command=self.publish_selected
        )
        self.publish_button.pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Clear Output", command=self._clear_output).pack(
            side="left"
        )

        output_frame = ttk.LabelFrame(outer, text="Results", padding=8)
        output_frame.pack(fill="both", expand=True)
        self.output = tk.Text(output_frame, wrap="word", state="disabled")
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output.yview
        )
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(outer, textvariable=self.status_var, anchor="w").pack(fill="x", pady=(8, 0))

    def _selected_actions(self) -> list[str]:
        return [name for name, variable in self.action_vars.items() if variable.get()]

    def preview_selected(self) -> None:
        names = self._selected_actions()
        if not names:
            messagebox.showinfo("No selection", "Select at least one automation.")
            return
        self._start_worker(self._build_posts, names, False)

    def publish_selected(self) -> None:
        names = self._selected_actions()
        if not names:
            messagebox.showinfo("No selection", "Select at least one automation.")
            return
        if not messagebox.askyesno(
            "Confirm live publish",
            f"This will create {len(names)} live Facebook post(s). Continue?",
            icon="warning",
        ):
            return
        self._start_worker(self._build_posts, names, True)

    def _start_worker(self, target: object, *args: object) -> None:
        self.preview_button.configure(state="disabled")
        self.publish_button.configure(state="disabled")
        self.status_var.set("Working...")
        threading.Thread(target=target, args=args, daemon=True).start()

    def _build_posts(self, names: list[str], publish: bool) -> None:
        try:
            settings = Settings.from_env() if publish else None
            timeout = settings.request_timeout_seconds if settings else 30.0
            anilist = AniListClient(timeout=timeout)
            provider = (
                FacebookPageProvider(
                    user_token=settings.facebook_user_token,
                    api_version=settings.facebook_graph_api_version,
                    timeout=timeout,
                )
                if settings
                else None
            )

            for name in names:
                self.events.put(("status", f"Running {name}..."))
                post = ACTIONS[name](anilist)
                self.events.put(("output", self._format_post(name, post)))
                if provider:
                    result = provider.publish(post)
                    self.events.put(
                        ("output", f"PUBLISHED: {name} -> Facebook post {result.post_id}\n\n")
                    )
            self.events.put(("done", f"Completed {len(names)} automation(s)."))
        except Exception:
            self.events.put(("error", traceback.format_exc()))

    @staticmethod
    def _format_post(name: str, post: Post) -> str:
        separator = "=" * 72
        image = post.image_url or "(none)"
        comment = post.first_comment or "(none)"
        return (
            f"{separator}\n{name}\n{separator}\n"
            f"MESSAGE\n{post.message}\n\n"
            f"IMAGE URL\n{image}\n\n"
            f"FIRST COMMENT\n{comment}\n\n"
        )

    def _process_events(self) -> None:
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == "output":
                    self._append_output(str(payload))
                elif kind == "status":
                    self.status_var.set(str(payload))
                elif kind == "done":
                    self._finish(str(payload))
                elif kind == "error":
                    self._append_output(f"ERROR\n{payload}\n")
                    self._finish("Failed - see output for details.")
                    messagebox.showerror("Automation failed", "See the Results panel for details.")
        except queue.Empty:
            pass
        self.after(100, self._process_events)

    def _finish(self, status: str) -> None:
        self.status_var.set(status)
        self.preview_button.configure(state="normal")
        self.publish_button.configure(state="normal")

    def _append_output(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def _clear_output(self) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")


def main() -> None:
    AutomationTestGUI().mainloop()


if __name__ == "__main__":
    main()
