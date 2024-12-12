import os
import google.generativeai as genai
from dotenv import load_dotenv
import subprocess
import ctypes
import sys
import colorama
from colorama import Fore, Back, Style
import platform
import psutil
import time
import textwrap

# Initialize colorama for Windows
colorama.init()

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

def get_system_info():
    """Get detailed Windows system information"""
    return {
        'os': platform.system(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'ram': f"{psutil.virtual_memory().total / (1024.0 ** 3):.1f}GB",
        'cpu_count': psutil.cpu_count(),
        'cpu_usage': f"{psutil.cpu_percent()}%"
    }

def print_styled(text, color=Fore.WHITE, style=Style.NORMAL, end='\n'):
    """Print text with color and style"""
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def print_header():
    """Print a styled header with system information"""
    system_info = get_system_info()
    print_styled("╔═══════════════════════════════════════════════════════════════╗", Fore.CYAN)
    print_styled("║             Windows 11 PowerShell AI Assistant                ║", Fore.CYAN)
    print_styled("╠═══════════════════════════════════════════════════════════════╣", Fore.CYAN)
    print_styled(f"║ OS: Windows {system_info['version'].split('.')[2]}                                           ║", Fore.GREEN)
    print_styled(f"║ CPU: {system_info['processor'][:40]}     ║", Fore.GREEN)
    print_styled(f"║ RAM: {system_info['ram']}                                                  ║", Fore.GREEN)
    print_styled("╚═══════════════════════════════════════════════════════════════╝", Fore.CYAN)

def is_admin():
    """Check if the script is running with administrative privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Restart the script with admin privileges"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def requires_admin(command):
    """Check if a PowerShell command might require admin privileges"""
    admin_keywords = [
        'Set-ExecutionPolicy', 'Install-', 'New-Service', 'Stop-Service', 'Start-Service',
        'Register-', 'Remove-Service', 'Set-Service', 'New-EventLog', 'Clear-EventLog',
        'Remove-EventLog', 'Mount-', 'Dismount-', 'Set-Acl', 'Reset-', 'Enable-',
        'Disable-', 'Add-Computer', 'Remove-Computer', 'Restart-Computer', 'Stop-Computer',
        'Set-NetConnectionProfile', 'Set-VMProcessor', 'Set-VM', 'New-VM', 'Remove-VM'
    ]
    return any(keyword.lower() in command.lower() for keyword in admin_keywords)

def is_dangerous_command(command):
    """Check if a PowerShell command might be dangerous"""
    dangerous_keywords = [
        'Remove-', 'Delete', 'Format-', 'Clear-', 'Reset-', 'Stop-', 'Disable-',
        'Uninstall-', 'Kill', '-Force', 'rmdir', 'del ', 'rm ', 'shutdown',
        'Set-MpPreference', 'Set-NetFirewallRule', 'Invoke-Expression',
        'Remove-VM', 'Stop-VM', 'Remove-VMSnapshot'
    ]
    return any(keyword.lower() in command.lower() for keyword in dangerous_keywords)

def generate_powershell_command(prompt):
    """Generate PowerShell command from natural language using Gemini API"""
    system_prompt = """You are a Windows 11 PowerShell expert. Convert the following natural language request into a PowerShell command.
    Only return the exact PowerShell command, nothing else. Ensure the command is safe and follows best practices.
    Optimize for Windows 11 Workstation Pro environment and avoid potentially dangerous operations without explicit confirmation."""
    
    full_prompt = f"{system_prompt}\n\nRequest: {prompt}"
    
    try:
        print_styled("🤔 Thinking...", Fore.YELLOW)
        response = model.generate_content(full_prompt)
        command = response.text.strip()
        return command
    except Exception as e:
        return f"Error generating command: {str(e)}"

def print_command_explanation(command):
    """Print a user-friendly explanation of the PowerShell command"""
    try:
        # Simple command explanations dictionary
        explanations = {
            'Get-Date': 'Shows the current date and time',
            'Get-Process': 'Lists all running processes on your computer',
            'Get-NetAdapter': 'Shows all network adapters (WiFi, Ethernet, etc.)',
            'Get-Service': 'Lists all Windows services',
            'Get-ComputerInfo': 'Shows detailed information about your computer',
        }
        
        # Get base command without parameters
        base_command = command.split()[0]
        
        # Print styled explanation box
        print_styled("\n📝 Command Explanation:", Fore.CYAN)
        print_styled("╔" + "═" * 60 + "╗", Fore.BLUE)
        
        if base_command in explanations:
            explanation = explanations[base_command]
        else:
            # Use Gemini to generate explanation for unknown commands
            prompt = f"Explain this PowerShell command in simple terms (max 2 lines): {command}"
            response = model.generate_content(prompt)
            explanation = response.text.strip()
        
        # Wrap text to fit in box
        wrapped_text = textwrap.fill(explanation, width=58)
        for line in wrapped_text.split('\n'):
            print_styled(f"║ {line:<58} ║", Fore.BLUE)
        
        print_styled("╚" + "═" * 60 + "╝", Fore.BLUE)
        print()

    except Exception as e:
        print_styled(f"Could not generate explanation: {str(e)}", Fore.YELLOW)

def execute_powershell_command(command, admin_mode=False):
    """Execute the generated PowerShell command"""
    try:
        if requires_admin(command) and not admin_mode:
            print_styled("⚠️ This command requires administrative privileges!", Fore.YELLOW)
            return

        if is_dangerous_command(command):
            print_styled("⚠️ Warning: This command might be dangerous!", Fore.RED)
            return

        # Add command explanation
        print_command_explanation(command)

        print_styled("\n🚀 Executing command:", Fore.CYAN)
        print_styled("╔" + "═" * 60 + "╗", Fore.GREEN)
        print_styled(f"║ {command:<58} ║", Fore.GREEN)
        print_styled("╚" + "═" * 60 + "╝", Fore.GREEN)

        # Execute command and capture output
        result = subprocess.run(['powershell', '-Command', command], 
                              capture_output=True, text=True)

        # Print result in a styled box
        print_styled("\n📊 Result:", Fore.CYAN)
        print_styled("╔" + "═" * 60 + "╗", Fore.MAGENTA)
        
        output_lines = result.stdout.strip().split('\n')
        for line in output_lines:
            print_styled(f"║ {line:<58} ║", Fore.MAGENTA)
            
        print_styled("╚" + "═" * 60 + "╝", Fore.MAGENTA)
        print()

        return result.stdout.strip()

    except Exception as e:
        print_styled(f"\n❌ Error: {str(e)}", Fore.RED)
        return None

def show_progress_spinner():
    """Show a simple progress spinner"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for char in chars:
        sys.stdout.write(f'\r{char} ')
        sys.stdout.flush()
        time.sleep(0.1)

def main():
    print_header()
    print_styled("\n💡 Type 'exit' to quit, 'help' for commands list", Fore.YELLOW)
    print_styled("\nSafety Features:", Fore.CYAN)
    print_styled("✓ Administrative privilege detection", Fore.GREEN)
    print_styled("✓ Dangerous command detection", Fore.GREEN)
    print_styled("✓ Windows 11 optimization", Fore.GREEN)
    print_styled("✓ Command confirmation required", Fore.GREEN)
    
    while True:
        try:
            print_styled("\n🔷 What would you like to do? ", Fore.CYAN, end='')
            user_input = input()
            
            if user_input.lower() == 'exit':
                print_styled("\nGoodbye! 👋", Fore.YELLOW)
                break
                
            if user_input.lower() == 'help':
                print_styled("\nCommon Commands:", Fore.CYAN)
                print_styled("- System information: 'show system info'", Fore.WHITE)
                print_styled("- Process management: 'show running processes'", Fore.WHITE)
                print_styled("- Network status: 'show network status'", Fore.WHITE)
                print_styled("- VM management: 'list virtual machines'", Fore.WHITE)
                continue
            
            # Generate PowerShell command
            command = generate_powershell_command(user_input)
            
            print_styled("\nGenerated Command:", Fore.CYAN)
            print_styled(f"{command}", Fore.WHITE)
            
            # Check for dangerous operations
            needs_admin = requires_admin(command)
            is_dangerous = is_dangerous_command(command)
            
            if is_dangerous:
                print_styled("\n⚠️ WARNING: This command may perform dangerous operations!", Fore.RED)
                
            if needs_admin:
                print_styled("\n🛡️ NOTE: This command requires administrative privileges.", Fore.YELLOW)
            
            # Ask for confirmation with additional warning
            print_styled("\nExecute this command? (y/n): ", Fore.YELLOW, end='')
            confirm = input().lower()
            
            if confirm == 'y':
                if is_dangerous:
                    print_styled("⚠️ This is a potentially dangerous command. Type 'yes' to confirm: ", Fore.RED, end='')
                    double_confirm = input().lower()
                    if double_confirm != 'yes':
                        print_styled("Command execution cancelled.", Fore.YELLOW)
                        continue
                
                result = execute_powershell_command(command, needs_admin)
                print_styled("\nResult:", Fore.CYAN)
                print_styled(result, Fore.WHITE)
            else:
                print_styled("Command execution cancelled.", Fore.YELLOW)
                
        except KeyboardInterrupt:
            print_styled("\nGoodbye! 👋", Fore.YELLOW)
            break
        except Exception as e:
            print_styled(f"\n❌ Error: {str(e)}", Fore.RED)

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print_styled("❌ Error: GEMINI_API_KEY not found in .env file", Fore.RED)
        exit(1)
    main()
