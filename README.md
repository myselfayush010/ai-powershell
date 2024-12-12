# PowerShell AI Assistant 

An interactive command-line tool that helps you learn and use PowerShell commands with AI-powered explanations and safety features.

## Features 

-  AI-powered command generation from natural language
-  Simple explanations for every command
-  Beautiful colored interface
-  Built-in safety checks
-  Learning-friendly output
-  Command previews before execution

## Safety Features 

-  Admin privilege detection
-  Dangerous command warnings
-  Command confirmation prompts
-  System protection measures

## Installation 

1. Install required packages:
```powershell
pip install -r requirements_powershell.txt
```

2. Set up your environment:
   - Copy `env.example` to `.env`:
     ```powershell
     Copy-Item env.example .env
     ```
   - Edit `.env` and configure your preferred AI provider:

### AI Provider Configuration 🤖

The assistant supports multiple AI providers. Choose one and configure accordingly:

#### Google Gemini (Default)
```env
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=gemini
```

#### OpenAI GPT
```env
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=openai
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
```

#### Anthropic Claude
```env
CLAUDE_API_KEY=your_claude_api_key_here
AI_PROVIDER=claude
CLAUDE_MODEL=claude-2  # or claude-instant
```

#### X.AI (Grok)
```env
XAI_API_KEY=your_xai_api_key_here
AI_PROVIDER=xai
XAI_MODEL=grok-beta
```

Choose the AI provider that best suits your needs:
- **Gemini**: Good balance of performance and cost
- **GPT-4**: Best for complex command understanding
- **Claude**: Excellent for detailed explanations
- **Grok**: Specialized in technical and coding tasks

The `.env` file is automatically ignored by git for security.

## Usage 

Run the assistant:
```powershell
python ps.py
```

### Common Commands 

- System information: `show system info`
- Process management: `show running processes`
- Network status: `show network status`
- Service management: `list services`, `check service status`
- File operations: `list files`, `create directory`
- Registry operations: `read registry`, `check installed software`

### Example Usage 

```
 What would you like to do? show running processes

 Command Explanation:
╔════════════════════════════════════════════════════════════╗
║ Lists all active processes running on your system          ║
╚════════════════════════════════════════════════════════════╝

 Executing command:
╔════════════════════════════════════════════════════════════╗
║ Get-Process                                               ║
╚════════════════════════════════════════════════════════════╝
```

## Tips for Learning 

1. Use the `help` command to see available options
2. Read the command explanations before execution
3. Start with simple commands and gradually try more complex ones
4. Pay attention to the safety warnings
5. Use the command preview feature to understand what will be executed

## Contributing 

Feel free to submit issues and enhancement requests!

## License 

MIT License - feel free to use and modify for your needs!
