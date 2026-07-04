from rich.console import Console
from rich.panel import Panel

from src.agent import Agent

console = Console()


def main():
    console.print(Panel.fit("Agente de Busca na Internet", style="bold cyan"))
    console.print("[dim]Digite 'sair' para encerrar.\n")

    agent = Agent()

    while True:
        user_input = console.input("[bold green]Pergunta[/bold green]: ")
        if user_input.lower() in ("sair", "quit", "exit"):
            console.print("[bold cyan]AgentIA:[/bold cyan] Até logo!")
            break

        console.print("[bold cyan]AgentIA[/bold cyan]: ", end="")
        with console.status("[yellow]Pesquisando na internet...[/yellow]"):
            response = agent.ask(user_input)
        console.print(response)
        console.print()


if __name__ == "__main__":
    main()
