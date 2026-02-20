"""
CLI interface — interact with the agent system from the terminal.

Commands:
    agent chat              Interactive text chat (REPL)
    agent voice             Interactive voice mode (mic/speaker)
    agent ask "question"    One-shot text query
    agent status            Show system status
    agent auth gmail        Run Gmail OAuth flow
    agent auth outlook      Run Outlook OAuth flow

Usage:
    python -m cli.main chat
    python -m cli.main ask "What are Harshit's skills?"
    python -m cli.main voice

Install: pip install typer rich
"""

# TODO: Phase 1 — implement with typer + rich
#
# import typer
# import asyncio
# from rich.console import Console
# from rich.panel import Panel
# from agents.orchestrator import orchestrator
#
# app = typer.Typer(name="agent", help="HarshitOS Agent CLI")
# console = Console()
#
# @app.command()
# def chat():
#     """Interactive text chat with the agent."""
#     console.print(Panel("HarshitOS Agent — type 'exit' to quit", style="bold cyan"))
#     while True:
#         query = console.input("[bold cyan]you>[/bold cyan] ")
#         if query.lower() in ("exit", "quit", "q"):
#             break
#         response = asyncio.run(orchestrator.handle(query))
#         console.print(f"[green]agent>[/green] {response}")
#
# @app.command()
# def voice():
#     """Interactive voice mode."""
#     from voice.cli_transport import VoiceCLI
#     asyncio.run(VoiceCLI().start())
#
# @app.command()
# def ask(question: str):
#     """One-shot query."""
#     response = asyncio.run(orchestrator.handle(question))
#     console.print(response)
#
# @app.command()
# def status():
#     """Show system status."""
#     ...


def main():
    print("[cli] Not yet implemented — Phase 1")
    print("  Install: pip install typer rich")
    print("  Commands: chat, voice, ask, status, auth")


if __name__ == "__main__":
    main()
