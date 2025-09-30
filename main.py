import click
from app.chat import ChatManager
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.command()
@click.option('--model', default='gemma3:4b', help='Ollama model to use')
@click.option('--no-tools', is_flag=True, help='Disable tools')
@click.option('--temperature', default=0.7, type=float, help='LLM temperature')
def chat(model, no_tools, temperature):
    """Starts a chat session with the AI assistant."""
    
    # Welcome message
    console.print(Panel.fit(
        f"[bold blue]AI Assistant CLI[/bold blue]\n"
        f"Model: {model} | Tools: {'Disabled' if no_tools else 'Enabled'}\n"
        "Commands: /tools, /clear, /reload, /model, /help, exit",
        title="Welcome"
    ))
    
    # Initialize chat manager
    chat_manager = ChatManager(
        model_name=model,
        use_tools=not no_tools,
        temperature=temperature
    )
    
    # Show loaded tools
    if not no_tools:
        tools = chat_manager.get_tool_list()
        if tools:
            console.print(f"\n[green]Loaded {len(tools)} tools:[/green] {', '.join(tools)}\n")
    
    while True:
        # Get user input
        prompt = console.input("[bold cyan]You>[/bold cyan] ")
        
        # Handle commands
        if prompt.lower() in ['exit', 'quit', 'q']:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        elif prompt.lower() == '/tools':
            show_tools(chat_manager)
            continue
        
        elif prompt.lower() == '/clear':
            chat_manager.clear_history()
            console.print("[green]Conversation history cleared[/green]")
            continue
        
        else:
            response = chat_manager.chat(prompt)
            console.print(f"[blue]AI>[/blue] {response}")

def show_tools(chat_manager):
    tools = chat_manager.get_tool_list()
    if tools:
        console.print(f"[green]Available tools:[/green] {', '.join(tools)}")
    else:
        console.print("[yellow]No tools available[/yellow]")

if __name__ == '__main__':
    chat()