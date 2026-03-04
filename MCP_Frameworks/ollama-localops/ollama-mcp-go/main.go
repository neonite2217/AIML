package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

const (
	version = "2.0.0"
	banner  = `
██╗      ██████╗  ██████╗ █████╗ ██╗      ██████╗ ██████╗ ███████╗
██║     ██╔═══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝
██║     ██║   ██║██║     ███████║██║     ██║   ██║██████╔╝███████╗
██║     ██║   ██║██║     ██╔══██║██║     ██║   ██║██╔═══╝ ╚════██║
███████╗╚██████╔╝╚██████╗██║  ██║███████╗╚██████╔╝██║     ███████║
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝
🤖 Local AI Operations Assistant v%s
Made by neonite._
`
)

type Config struct {
	ConfigDir        string
	ApprovedFile     string
	BlockedFile      string
	UsageFile        string
	OllamaModel      string
	OllamaURL        string
	ApprovedCommands []string
	BlockedCommands  []string
}

type OllamaRequest struct {
	Model  string `json:"model"`
	Prompt string `json:"prompt"`
	Stream bool   `json:"stream"`
}

type OllamaResponse struct {
	Response string `json:"response"`
	Done     bool   `json:"done"`
}

func main() {
	config := initConfig()

	if len(os.Args) < 2 {
		runInteractiveMode(config)
		return
	}

	command := strings.Join(os.Args[1:], " ")
	
	switch command {
	case "install", "--install":
		runInstaller()
	case "help", "--help", "-h":
		showHelp()
	case "version", "--version", "-v":
		fmt.Printf("LocalOps Assistant v%s\n", version)
	case "mcp", "--mcp":
		runMCPServer(config)
	default:
		processCommand(config, command)
	}
}

func initConfig() *Config {
	homeDir, _ := os.UserHomeDir()
	configDir := filepath.Join(homeDir, ".localops")
	
	config := &Config{
		ConfigDir:    configDir,
		ApprovedFile: filepath.Join(configDir, "approved-commands.conf"),
		BlockedFile:  filepath.Join(configDir, "blocked-commands.conf"),
		UsageFile:    filepath.Join(configDir, "usage.log"),
		OllamaModel:  getEnvOrDefault("OLLAMA_MODEL", "llama3.2:3b"),
		OllamaURL:    getEnvOrDefault("OLLAMA_URL", "http://localhost:11434"),
	}

	// Create config directory
	os.MkdirAll(configDir, 0755)
	
	// Load configurations
	config.loadApprovedCommands()
	config.loadBlockedCommands()
	
	return config
}

func (c *Config) loadApprovedCommands() {
	defaultApproved := []string{
		"ls", "pwd", "whoami", "date", "uptime", "df", "free", "ps", "top", "htop",
		"cat", "less", "head", "tail", "grep", "find", "which", "whereis",
		"git status", "git log", "git diff", "docker ps", "docker images",
		"systemctl status", "journalctl", "netstat", "ss", "lsof",
	}
	
	c.ApprovedCommands = c.loadCommandList(c.ApprovedFile, defaultApproved)
}

func (c *Config) loadBlockedCommands() {
	defaultBlocked := []string{
		"rm -rf /", "mkfs", "fdisk", "parted", "dd if=", "shutdown -f",
		"reboot -f", "halt -f", "init 0", "init 6", ":(){ :|:& };:",
	}
	
	c.BlockedCommands = c.loadCommandList(c.BlockedFile, defaultBlocked)
}

func (c *Config) loadCommandList(filename string, defaults []string) []string {
	if data, err := os.ReadFile(filename); err == nil {
		lines := strings.Split(string(data), "\n")
		var commands []string
		for _, line := range lines {
			if line = strings.TrimSpace(line); line != "" && !strings.HasPrefix(line, "#") {
				commands = append(commands, line)
			}
		}
		return commands
	}
	
	// Create file with defaults
	c.saveCommandList(filename, defaults)
	return defaults
}

func (c *Config) saveCommandList(filename string, commands []string) {
	file, err := os.Create(filename)
	if err != nil {
		return
	}
	defer file.Close()
	
	for _, cmd := range commands {
		fmt.Fprintln(file, cmd)
	}
}

func runInteractiveMode(config *Config) {
	fmt.Printf(banner, version)
	fmt.Println("\n🚀 Interactive Mode - AI-Powered Operations Assistant")
	fmt.Println("⚙️ Type 'help' for commands, 'exit' to quit\n")
	
	scanner := bufio.NewScanner(os.Stdin)
	
	for {
		fmt.Print("👤 Enter your request: ")
		if !scanner.Scan() {
			break
		}
		
		input := strings.TrimSpace(scanner.Text())
		if input == "" {
			continue
		}
		
		if input == "exit" || input == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}
		
		if input == "help" {
			showInteractiveHelp()
			continue
		}
		
		if input == "show approved commands" {
			showApprovedCommands(config)
			continue
		}
		
		if input == "show blocked commands" {
			showBlockedCommands(config)
			continue
		}
		
		if input == "show stats" {
			showStats(config)
			continue
		}
		
		processCommand(config, input)
		fmt.Println()
	}
}

func processCommand(config *Config, userInput string) {
	fmt.Printf("🧠 Processing: \"%s\"\n", userInput)
	
	// First try built-in command mapping for instant responses
	suggestion := mapCommonCommands(userInput)
	if suggestion != "" {
		fmt.Printf("⚡ Quick response: %s\n", suggestion)
		executeCommand(config, userInput, suggestion)
		return
	}
	
	// Check if it was just a conversational response (no command to execute)
	// mapCommonCommands returns empty string for greetings/conversations
	if isConversationalInput(userInput) {
		return
	}
	
	// Get AI suggestion for more complex requests
	suggestion, err := getAISuggestion(config, userInput)
	if err != nil {
		fmt.Printf("❌ AI Service Error: %v\n", err)
		fmt.Println("💡 Suggestions:")
		fmt.Println("   • Run 'localops install' to set up Ollama")
		fmt.Println("   • Try simpler commands like 'show system info'")
		fmt.Println("   • Check if Ollama is running: 'ollama serve'")
		return
	}
	
	suggestion = strings.TrimSpace(suggestion)
	if suggestion == "" {
		// This was handled by mapCommonCommands (like greetings)
		return
	}
	
	fmt.Printf("🤖 AI suggests: %s\n", suggestion)
	
	// Check command safety
	if config.isBlocked(suggestion) {
		fmt.Println("🛡️ Command blocked for safety")
		config.logUsage(userInput, suggestion, "blocked")
		return
	}
	
	if config.isApproved(suggestion) {
		fmt.Printf("🚀 Auto-executing (pre-approved): %s\n", suggestion)
		executeCommand(config, userInput, suggestion)
		return
	}
	
	// Ask for confirmation
	fmt.Printf("⚠️ Execute command? (y/N/a for always): ")
	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		response := strings.ToLower(strings.TrimSpace(scanner.Text()))
		
		switch response {
		case "y", "yes":
			executeCommand(config, userInput, suggestion)
		case "a", "always":
			config.ApprovedCommands = append(config.ApprovedCommands, suggestion)
			config.saveCommandList(config.ApprovedFile, config.ApprovedCommands)
			fmt.Println("✅ Command added to auto-approved list")
			executeCommand(config, userInput, suggestion)
		default:
			fmt.Println("❌ Command cancelled")
			config.logUsage(userInput, suggestion, "cancelled")
		}
	}
}

func executeCommand(config *Config, userInput, command string) {
	fmt.Printf("⚡ Executing: %s\n", command)
	
	cmd := exec.Command("bash", "-c", command)
	output, err := cmd.CombinedOutput()
	
	if err != nil {
		fmt.Printf("❌ Error: %v\n", err)
		config.logUsage(userInput, command, "error")
	} else {
		fmt.Printf("✅ %s\n", strings.TrimSpace(string(output)))
		config.logUsage(userInput, command, "success")
	}
}

func getAISuggestion(config *Config, userInput string) (string, error) {
	// First try built-in command mapping for common requests
	if cmd := mapCommonCommands(userInput); cmd != "" {
		return cmd, nil
	}
	
	prompt := fmt.Sprintf(`You are an expert Linux system administrator and command-line interface specialist. Convert natural language requests into precise, safe Linux commands.

User Request: "%s"

CRITICAL RULES:
- Return ONLY the exact command to run, no explanations, quotes, or markdown
- Prioritize safety and commonly available commands
- Use colorful output when possible (--color=auto, -h for human readable)
- Chain commands with && when logical (e.g., update before install)

COMMAND CATEGORIES:

SYSTEM INFO:
- System overview: uname -a && lscpu | head -10 && free -h && df -h
- Hardware: lscpu, lshw -short, lsblk, lsusb, lspci
- Performance: top -bn1 | head -15, htop, iotop, vmstat
- Temperature: sensors, cat /sys/class/thermal/thermal_zone*/temp

MEMORY & STORAGE:
- Memory: free -h, cat /proc/meminfo | head -10
- Disk usage: df -h, du -sh *, lsblk
- Disk I/O: iostat, iotop

FILES & DIRECTORIES:
- List current: ls -la --color=auto, tree, find . -maxdepth 2
- List home: ls -la --color=auto $HOME
- List specific: ls -la --color=auto /path/to/directory
- Search: find / -name "*filename*" 2>/dev/null, locate filename
- Permissions: ls -la, stat filename, chmod, chown

PROCESSES & SERVICES:
- Processes: ps aux, ps aux --sort=-%cpu, pgrep -l name
- Services: systemctl list-units --type=service, systemctl status service
- Kill: pkill name, killall name

NETWORK:
- Interfaces: ip addr show, ifconfig
- Connections: netstat -tuln, ss -tuln, lsof -i
- Connectivity: ping -c 4 host, traceroute host, nslookup host

PACKAGE MANAGEMENT:
- Update: sudo apt update
- Upgrade: sudo apt update && sudo apt upgrade -y
- Install: sudo apt update && sudo apt install -y package
- Search: apt search package, apt list --installed | grep package
- Remove: sudo apt remove package, sudo apt autoremove -y
- Clean: sudo apt autoremove -y && sudo apt autoclean
- Full upgrade: sudo apt update && sudo apt full-upgrade -y

VERSION CHECKS:
- Software: command --version, command -v, which command
- System: lsb_release -a, cat /etc/os-release

LOGS & MONITORING:
- System logs: journalctl -n 20, dmesg | tail -20
- Service logs: journalctl -u service -n 20
- Error logs: journalctl -p err -n 10

Examples:
"show system info" → uname -a && echo -e '\n💾 CPU:' && lscpu | head -5 && echo -e '\n🧠 Memory:' && free -h && echo -e '\n💿 Disk:' && df -h
"check memory usage" → free -h && echo -e '\n🔥 Top Memory Users:' && ps aux --sort=-%mem | head -6
"list files here" → ls -la --color=auto
"list files in home directory" → ls -la --color=auto $HOME
"running processes" → ps aux --sort=-%cpu | head -10
"install docker" → sudo apt update && sudo apt install -y docker.io && sudo systemctl enable docker
"check network" → ip addr show && echo -e '\n🌐 Active Connections:' && netstat -tuln | head -10
"apt update" → sudo apt update
"upgrade system" → sudo apt update && sudo apt upgrade -y
"install htop" → sudo apt update && sudo apt install -y htop

Command:`, userInput)

	reqBody := OllamaRequest{
		Model:  config.OllamaModel,
		Prompt: prompt,
		Stream: false,
	}
	
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return "", err
	}
	
	resp, err := http.Post(config.OllamaURL+"/api/generate", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	
	var ollamaResp OllamaResponse
	if err := json.Unmarshal(body, &ollamaResp); err != nil {
		return "", err
	}
	
	// Clean up the response
	command := strings.TrimSpace(ollamaResp.Response)
	command = strings.Trim(command, "`\"'")
	
	return command, nil
}

// mapCommonCommands provides instant responses for very common requests
func mapCommonCommands(input string) string {
	input = strings.ToLower(strings.TrimSpace(input))
	
	// Enhanced greetings and conversational responses
	greetings := []string{"hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy", "sup", "what's up"}
	for _, greeting := range greetings {
		if strings.Contains(input, greeting) {
			responses := []string{
				"👋 Hello! I'm LocalOps Assistant, your AI-powered system companion. What can I help you with today?",
				"🤖 Hi there! Ready to help you manage your system. Try asking me to 'show system info' or 'list files'!",
				"✨ Hey! I'm here to turn your natural language into powerful system commands. What would you like to do?",
			}
			fmt.Println(responses[len(input)%len(responses)])
			return ""
		}
	}
	
	// Conversational responses
	conversational := map[string]string{
		"how are you":     "🤖 I'm running smoothly! Ready to help you with system operations. What do you need?",
		"what can you do": "💪 I can help you with system info, file operations, process management, installations, and much more! Try: 'show system info'",
		"who are you":     "🤖 I'm LocalOps Assistant - your AI-powered command line companion. I translate natural language into system commands!",
		"thank you":       "😊 You're welcome! Happy to help with your system operations anytime!",
		"thanks":          "😊 No problem! Let me know if you need anything else!",
		"good job":        "🎉 Thanks! I'm here whenever you need system help!",
		"nice":            "😊 Glad I could help! What else can I do for you?",
	}
	
	for phrase, response := range conversational {
		if strings.Contains(input, phrase) {
			fmt.Println(response)
			return ""
		}
	}
	
	// Enhanced system information requests
	systemInfoPatterns := map[string]string{
		"system info":        "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"show system":        "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"system details":     "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"computer info":      "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"machine info":       "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"show me system":     "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"system status":      "echo '📊 SYSTEM STATUS' && uptime && echo -e '\n🔥 TOP PROCESSES:' && ps aux --sort=-%cpu | head -6",
		"system overview":    "echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h",
		"hardware info":      "echo '🔧 HARDWARE INFO' && lscpu && echo -e '\n💾 MEMORY:' && free -h && echo -e '\n💿 STORAGE:' && lsblk",
		"specs":              "echo '📋 SYSTEM SPECS' && lscpu | grep -E 'Model name|CPU\\(s\\)|Thread|Core' && echo -e '\n💾 Memory:' && free -h | grep Mem && echo -e '\n💿 Storage:' && df -h /",
	}
	
	// Memory and disk
	memoryDiskPatterns := map[string]string{
		"memory":          "free -h",
		"ram":             "free -h", 
		"disk":            "df -h",
		"disk space":      "df -h",
		"disk usage":      "df -h",
		"storage":         "df -h",
		"check memory":    "free -h",
		"check ram":       "free -h",
		"check disk":      "df -h",
		"show memory":     "free -h",
		"show disk":       "df -h",
	}
	
	// Home directory and specific directory patterns (check these first)
	homeDirectoryPatterns := map[string]string{
		"list files in home directory":  "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"show files in home directory":  "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"files in home directory":       "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"show files in home":            "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"home directory":                "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"files in home":                 "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"list home":                     "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"show home directory":           "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"home folder":                   "echo '🏠 Home Directory: $HOME' && ls -la --color=auto $HOME",
		"go home":                       "cd $HOME && echo '🏠 Changed to home directory: $HOME' && ls -la --color=auto",
		// Other specific directory patterns
		"list root directory":           "echo '🌳 Root Directory: /' && ls -la --color=auto /",
		"show root directory":           "echo '🌳 Root Directory: /' && ls -la --color=auto /",
		"files in root directory":       "echo '🌳 Root Directory: /' && ls -la --color=auto /",
		"show root":                     "echo '🌳 Root Directory: /' && ls -la --color=auto /",
		"root directory":                "echo '🌳 Root Directory: /' && ls -la --color=auto /",
		"list etc directory":            "echo '⚙️ /etc Directory:' && ls -la --color=auto /etc | head -20",
		"show etc directory":            "echo '⚙️ /etc Directory:' && ls -la --color=auto /etc | head -20",
		"files in etc":                  "echo '⚙️ /etc Directory:' && ls -la --color=auto /etc | head -20",
		"list etc":                      "echo '⚙️ /etc Directory:' && ls -la --color=auto /etc | head -20",
		"show etc":                      "echo '⚙️ /etc Directory:' && ls -la --color=auto /etc | head -20",
		"list var directory":            "echo '📁 /var Directory:' && ls -la --color=auto /var",
		"show var directory":            "echo '📁 /var Directory:' && ls -la --color=auto /var",
		"files in var":                  "echo '📁 /var Directory:' && ls -la --color=auto /var",
		"list var":                      "echo '📁 /var Directory:' && ls -la --color=auto /var",
		"show var":                      "echo '📁 /var Directory:' && ls -la --color=auto /var",
		"list tmp directory":            "echo '🗂️ /tmp Directory:' && ls -la --color=auto /tmp",
		"show tmp directory":            "echo '🗂️ /tmp Directory:' && ls -la --color=auto /tmp",
		"files in tmp":                  "echo '🗂️ /tmp Directory:' && ls -la --color=auto /tmp",
		"list tmp":                      "echo '🗂️ /tmp Directory:' && ls -la --color=auto /tmp",
		"show tmp":                      "echo '🗂️ /tmp Directory:' && ls -la --color=auto /tmp",
	}

	// Enhanced file and directory operations (current directory)
	filePatterns := map[string]string{
		"list files":         "ls -la --color=auto",
		"show files":         "ls -la --color=auto", 
		"files":              "ls -la --color=auto",
		"directories":        "ls -la --color=auto",
		"current dir":        "echo '📁 Current Directory:' && pwd && echo -e '\n📋 Contents:' && ls -la --color=auto",
		"where am i":         "pwd",
		"show directory":     "ls -la --color=auto",
		"list dir":           "ls -la --color=auto",
		"show folders":       "ls -la --color=auto | grep '^d'",
		"folders":            "ls -la --color=auto | grep '^d'",
		"file tree":          "tree -L 2 2>/dev/null || find . -maxdepth 2 -type d",
		"directory tree":     "tree -L 2 2>/dev/null || find . -maxdepth 2 -type d",
		"what's here":        "echo '📁 Current: ' && pwd && echo -e '\n📋 Files:' && ls -la --color=auto",
		"contents":           "ls -la --color=auto",
		"dir contents":       "ls -la --color=auto",
		"show contents":      "ls -la --color=auto",
		"list everything":    "ls -la --color=auto",
		"show all files":     "ls -la --color=auto",
		"hidden files":       "ls -la --color=auto | grep '^\\.\\|^total'",
	}
	
	// Process management
	processPatterns := map[string]string{
		"processes":       "ps aux",
		"running":         "ps aux",
		"tasks":           "ps aux", 
		"show processes":  "ps aux",
		"list processes":  "ps aux",
		"running processes": "ps aux",
		"what's running":  "ps aux",
	}
	
	// Network information
	networkPatterns := map[string]string{
		"ip":              "ip addr show",
		"network":         "ip addr show",
		"my ip":           "ip addr show",
		"ip address":      "ip addr show",
		"network info":    "ip addr show && netstat -tuln",
		"connections":     "netstat -tuln",
		"ports":           "netstat -tuln",
		"listening":       "netstat -tuln",
	}
	
	// Enhanced version checks and software detection
	if strings.Contains(input, "version") || strings.Contains(input, "check") {
		versionMap := map[string]string{
			"docker":     "docker --version 2>/dev/null || echo '❌ Docker not installed'",
			"git":        "git --version 2>/dev/null || echo '❌ Git not installed'",
			"python":     "python3 --version 2>/dev/null || echo '❌ Python3 not installed'",
			"node":       "node --version 2>/dev/null || echo '❌ Node.js not installed'",
			"npm":        "npm --version 2>/dev/null || echo '❌ NPM not installed'",
			"go":         "go version 2>/dev/null || echo '❌ Go not installed'",
			"java":       "java --version 2>/dev/null || echo '❌ Java not installed'",
			"nginx":      "nginx -v 2>&1 || echo '❌ Nginx not installed'",
			"apache":     "apache2 -v 2>/dev/null || echo '❌ Apache not installed'",
			"mysql":      "mysql --version 2>/dev/null || echo '❌ MySQL not installed'",
			"postgresql": "psql --version 2>/dev/null || echo '❌ PostgreSQL not installed'",
			"redis":      "redis-server --version 2>/dev/null || echo '❌ Redis not installed'",
			"php":        "php --version 2>/dev/null || echo '❌ PHP not installed'",
			"ruby":       "ruby --version 2>/dev/null || echo '❌ Ruby not installed'",
			"rust":       "rustc --version 2>/dev/null || echo '❌ Rust not installed'",
			"vim":        "vim --version | head -1 2>/dev/null || echo '❌ Vim not installed'",
			"curl":       "curl --version | head -1 2>/dev/null || echo '❌ Curl not installed'",
			"wget":       "wget --version | head -1 2>/dev/null || echo '❌ Wget not installed'",
		}
		
		for software, command := range versionMap {
			if strings.Contains(input, software) {
				return command
			}
		}
		
		// General version check
		if input == "check versions" || input == "show versions" || input == "software versions" {
			return "echo '🔍 SOFTWARE VERSIONS:' && echo '━━━━━━━━━━━━━━━━━━━━' && " +
				"echo '🐳 Docker:' && (docker --version 2>/dev/null || echo '❌ Not installed') && " +
				"echo '📦 Git:' && (git --version 2>/dev/null || echo '❌ Not installed') && " +
				"echo '🐍 Python:' && (python3 --version 2>/dev/null || echo '❌ Not installed') && " +
				"echo '📗 Node.js:' && (node --version 2>/dev/null || echo '❌ Not installed') && " +
				"echo '🔧 Go:' && (go version 2>/dev/null || echo '❌ Not installed')"
		}
	}
	
	// Package management patterns (apt commands)
	aptPatterns := map[string]string{
		"apt update":         "sudo apt update",
		"update packages":    "sudo apt update",
		"update package list": "sudo apt update",
		"refresh packages":   "sudo apt update",
		"apt upgrade":        "sudo apt update && sudo apt upgrade -y",
		"upgrade packages":   "sudo apt update && sudo apt upgrade -y",
		"upgrade system":     "sudo apt update && sudo apt upgrade -y",
		"system upgrade":     "sudo apt update && sudo apt upgrade -y",
		"full upgrade":       "sudo apt update && sudo apt full-upgrade -y",
		"apt full-upgrade":   "sudo apt update && sudo apt full-upgrade -y",
		"apt autoremove":     "sudo apt autoremove -y",
		"clean packages":     "sudo apt autoremove -y && sudo apt autoclean",
		"apt clean":          "sudo apt autoremove -y && sudo apt autoclean",
		"update and upgrade": "sudo apt update && sudo apt upgrade -y",
		"apt list installed": "apt list --installed",
		"installed packages": "apt list --installed | head -20",
		"search packages":    "apt search",
	}
	
	for pattern, command := range aptPatterns {
		if strings.Contains(input, pattern) {
			return command
		}
	}
	
	// Enhanced installation requests
	if strings.Contains(input, "install") {
		installMap := map[string]string{
			"htop":       "sudo apt update && sudo apt install -y htop",
			"docker":     "sudo apt update && sudo apt install -y docker.io && sudo systemctl enable docker && sudo systemctl start docker",
			"git":        "sudo apt update && sudo apt install -y git",
			"curl":       "sudo apt update && sudo apt install -y curl",
			"wget":       "sudo apt update && sudo apt install -y wget",
			"vim":        "sudo apt update && sudo apt install -y vim",
			"nano":       "sudo apt update && sudo apt install -y nano",
			"tree":       "sudo apt update && sudo apt install -y tree",
			"neofetch":   "sudo apt update && sudo apt install -y neofetch",
			"nodejs":     "sudo apt update && sudo apt install -y nodejs npm",
			"node":       "sudo apt update && sudo apt install -y nodejs npm",
			"python":     "sudo apt update && sudo apt install -y python3 python3-pip",
			"python3":    "sudo apt update && sudo apt install -y python3 python3-pip",
			"nginx":      "sudo apt update && sudo apt install -y nginx && sudo systemctl enable nginx",
			"apache":     "sudo apt update && sudo apt install -y apache2 && sudo systemctl enable apache2",
			"mysql":      "sudo apt update && sudo apt install -y mysql-server && sudo systemctl enable mysql",
			"postgresql": "sudo apt update && sudo apt install -y postgresql postgresql-contrib && sudo systemctl enable postgresql",
			"redis":      "sudo apt update && sudo apt install -y redis-server && sudo systemctl enable redis-server",
			"php":        "sudo apt update && sudo apt install -y php php-cli php-fpm",
			"java":       "sudo apt update && sudo apt install -y default-jdk",
			"build-essential": "sudo apt update && sudo apt install -y build-essential",
			"gcc":        "sudo apt update && sudo apt install -y build-essential gcc",
			"make":       "sudo apt update && sudo apt install -y build-essential make",
			"zip":        "sudo apt update && sudo apt install -y zip unzip",
			"unzip":      "sudo apt update && sudo apt install -y zip unzip",
			"snap":       "sudo apt update && sudo apt install -y snapd",
			"flatpak":    "sudo apt update && sudo apt install -y flatpak",
			"software-properties-common": "sudo apt update && sudo apt install -y software-properties-common",
		}
		
		for software, command := range installMap {
			if strings.Contains(input, software) {
				return command
			}
		}
	}
	
	// Additional useful patterns
	servicePatterns := map[string]string{
		"services":           "systemctl list-units --type=service --state=running",
		"running services":   "systemctl list-units --type=service --state=running",
		"active services":    "systemctl list-units --type=service --state=active",
		"failed services":    "systemctl list-units --type=service --state=failed",
		"service status":     "systemctl status",
		"system services":    "systemctl list-units --type=service",
	}
	
	performancePatterns := map[string]string{
		"performance":        "echo '⚡ SYSTEM PERFORMANCE' && top -bn1 | head -20",
		"cpu usage":          "echo '💾 CPU Usage:' && top -bn1 | grep 'Cpu(s)' && echo -e '\n🔥 Top CPU Processes:' && ps aux --sort=-%cpu | head -6",
		"load average":       "uptime",
		"system load":        "uptime && echo -e '\n📊 Load Details:' && cat /proc/loadavg",
		"temperature":        "sensors 2>/dev/null || echo '🌡️ Temperature sensors not available (install lm-sensors)'",
		"temp":               "sensors 2>/dev/null || echo '🌡️ Temperature sensors not available (install lm-sensors)'",
	}
	
	logPatterns := map[string]string{
		"logs":               "journalctl -n 20 --no-pager",
		"system logs":        "journalctl -n 20 --no-pager",
		"recent logs":        "journalctl -n 20 --no-pager",
		"error logs":         "journalctl -p err -n 10 --no-pager",
		"boot logs":          "journalctl -b --no-pager | tail -20",
		"kernel logs":        "dmesg | tail -20",
	}
	
	userPatterns := map[string]string{
		"users":              "echo '👥 LOGGED IN USERS:' && who && echo -e '\n📋 All Users:' && cut -d: -f1 /etc/passwd | sort",
		"logged in":          "who",
		"current user":       "whoami && echo 'Groups:' && groups",
		"user info":          "id && echo -e '\nHome:' && echo $HOME",
		"who am i":           "whoami && id",
	}
	
	// Check all pattern maps (order matters - more specific patterns first)
	allPatterns := []map[string]string{
		homeDirectoryPatterns, // Check specific directory patterns first
		systemInfoPatterns,
		memoryDiskPatterns, 
		filePatterns,
		processPatterns,
		networkPatterns,
		servicePatterns,
		performancePatterns,
		logPatterns,
		userPatterns,
		aptPatterns,
	}
	
	for _, patterns := range allPatterns {
		for pattern, command := range patterns {
			if strings.Contains(input, pattern) {
				return command
			}
		}
	}
	
	return ""
}

func (c *Config) isApproved(command string) bool {
	for _, approved := range c.ApprovedCommands {
		if strings.Contains(command, approved) {
			return true
		}
	}
	return false
}

func (c *Config) isBlocked(command string) bool {
	for _, blocked := range c.BlockedCommands {
		if strings.Contains(command, blocked) {
			return true
		}
	}
	return false
}

func (c *Config) logUsage(userInput, command, status string) {
	logEntry := fmt.Sprintf("%s | %s | %s | %s\n", 
		time.Now().Format("2006-01-02 15:04:05"), 
		userInput, 
		command, 
		status)
	
	file, err := os.OpenFile(c.UsageFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return
	}
	defer file.Close()
	
	file.WriteString(logEntry)
}

func checkOllamaConnection(url string) bool {
	client := &http.Client{Timeout: 2 * time.Second}
	resp, err := client.Head(url)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return resp.StatusCode == 200
}

func runInstaller() {
	fmt.Printf(banner, version)
	fmt.Println("🚀 LocalOps Assistant Installer")
	fmt.Println("Setting up your AI-powered operations center...\n")
	
	// Detect system
	fmt.Println("🔍 Detecting system...")
	osType := runtime.GOOS
	arch := runtime.GOARCH
	fmt.Printf("✅ Detected: %s/%s\n\n", osType, arch)
	
	if osType != "linux" && osType != "darwin" {
		fmt.Println("❌ Unsupported operating system. LocalOps Assistant requires Linux or macOS.")
		return
	}
	
	// Install Ollama
	fmt.Println("📥 Installing Ollama...")
	if !commandExists("ollama") {
		installOllama()
	} else {
		fmt.Println("✅ Ollama already installed")
	}
	
	// Start Ollama service
	fmt.Println("🚀 Starting Ollama service...")
	startOllama()
	
	// Install model
	fmt.Println("🧠 Installing AI model...")
	installModel()
	
	// Setup configuration
	fmt.Println("⚙️ Setting up configuration...")
	config := initConfig()
	fmt.Printf("✅ Configuration created at: %s\n", config.ConfigDir)
	
	// Test installation
	fmt.Println("🧪 Testing installation...")
	if checkOllamaConnection("http://localhost:11434") {
		fmt.Println("✅ LocalOps Assistant is ready!")
	} else {
		fmt.Println("⚠️ Installation completed but Ollama may need manual start")
	}
	
	fmt.Println("\n🎉 Installation Complete!")
	fmt.Println("Usage:")
	fmt.Println("  localops \"show system info\"    # Direct command")
	fmt.Println("  localops                        # Interactive mode")
}

func installOllama() {
	fmt.Println("Downloading and installing Ollama...")
	
	cmd := exec.Command("curl", "-fsSL", "https://ollama.ai/install.sh")
	installScript := exec.Command("sh")
	
	pipe, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Printf("❌ Error setting up Ollama installation: %v\n", err)
		return
	}
	
	installScript.Stdin = pipe
	
	if err := cmd.Start(); err != nil {
		fmt.Printf("❌ Error downloading Ollama: %v\n", err)
		return
	}
	
	if err := installScript.Run(); err != nil {
		fmt.Printf("❌ Error installing Ollama: %v\n", err)
		return
	}
	
	cmd.Wait()
	fmt.Println("✅ Ollama installed successfully")
}

func startOllama() {
	// Try to start Ollama service
	exec.Command("ollama", "serve").Start()
	time.Sleep(2 * time.Second)
	
	if checkOllamaConnection("http://localhost:11434") {
		fmt.Println("✅ Ollama service started")
	} else {
		fmt.Println("⚠️ Ollama service may need manual start: ollama serve")
	}
}

func installModel() {
	model := getEnvOrDefault("OLLAMA_MODEL", "llama3.2:3b")
	fmt.Printf("Installing model: %s (this may take a few minutes...)\n", model)
	
	cmd := exec.Command("ollama", "pull", model)
	if err := cmd.Run(); err != nil {
		fmt.Printf("⚠️ Model installation failed: %v\n", err)
		fmt.Printf("You can install it later with: ollama pull %s\n", model)
	} else {
		fmt.Printf("✅ Model %s installed successfully\n", model)
	}
}

func commandExists(cmd string) bool {
	_, err := exec.LookPath(cmd)
	return err == nil
}

func getEnvOrDefault(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func isConversationalInput(input string) bool {
	input = strings.ToLower(strings.TrimSpace(input))
	conversationalPhrases := []string{
		"hello", "hi", "hey", "good morning", "good afternoon", "good evening", 
		"howdy", "sup", "what's up", "how are you", "what can you do", 
		"who are you", "thank you", "thanks", "good job", "nice",
	}
	
	for _, phrase := range conversationalPhrases {
		if strings.Contains(input, phrase) {
			return true
		}
	}
	return false
}

func showHelp() {
	fmt.Printf(banner, version)
	fmt.Println("USAGE:")
	fmt.Println("  localops \"your request\"        # Direct command")
	fmt.Println("  localops                        # Interactive mode")
	fmt.Println("  localops install                # Run installer")
	fmt.Println("  localops mcp                    # MCP server mode")
	fmt.Println("  localops help                   # Show this help")
	fmt.Println("  localops version                # Show version")
	fmt.Println()
	fmt.Println("EXAMPLES:")
	fmt.Println("  localops \"show disk usage\"")
	fmt.Println("  localops \"install docker\"")
	fmt.Println("  localops \"check running processes\"")
	fmt.Println("  localops \"restart nginx service\"")
	fmt.Println()
	fmt.Println("MCP INTEGRATION:")
	fmt.Println("  ./start-mcp-server.sh           # Start as MCP server")
	fmt.Println("  Use mcp-config.json for MCP client configuration")
	fmt.Println()
	fmt.Println("ENVIRONMENT VARIABLES:")
	fmt.Println("  OLLAMA_MODEL    AI model to use (default: llama3.2:3b)")
	fmt.Println("  OLLAMA_URL      Ollama server URL (default: http://localhost:11434)")
}

func showInteractiveHelp() {
	fmt.Println("📋 Available Commands:")
	fmt.Println("  help                    Show this help")
	fmt.Println("  exit/quit              Exit interactive mode")
	fmt.Println("  show approved commands  List auto-approved commands")
	fmt.Println("  show blocked commands   List blocked commands")
	fmt.Println("  show stats             Show usage statistics")
	fmt.Println()
	fmt.Println("🗣️ Natural Language Examples:")
	fmt.Println("  \"Hello\" or \"Hi\"           Get a friendly greeting")
	fmt.Println("  \"Show system info\"        Complete system overview")
	fmt.Println("  \"Check memory usage\"      Memory and top processes")
	fmt.Println("  \"List files\"              Show directory contents")
	fmt.Println("  \"What's running\"          Show active processes")
	fmt.Println("  \"Check docker version\"    Verify software versions")
	fmt.Println("  \"Install htop\"            Install system packages")
	fmt.Println("  \"Show network info\"       Network configuration")
	fmt.Println("  \"System performance\"      CPU usage and load")
	fmt.Println("  \"Recent logs\"             View system logs")
	fmt.Println()
	fmt.Println("💡 Smart Features:")
	fmt.Println("  ✅ Instant responses for common requests")
	fmt.Println("  🤖 AI-powered command generation for complex tasks")
	fmt.Println("  🛡️ Safety checks prevent dangerous operations")
	fmt.Println("  📊 Colorful, formatted output")
	fmt.Println("  🔄 Learning system remembers your preferences")
	fmt.Println()
	fmt.Println("⚡ Quick Commands:")
	fmt.Println("  Type 'a' when prompted to auto-approve command types")
	fmt.Println("  Safe read-only commands execute automatically")
}

func showApprovedCommands(config *Config) {
	fmt.Println("✅ Auto-approved commands:")
	for i, cmd := range config.ApprovedCommands {
		fmt.Printf("  %d. %s\n", i+1, cmd)
	}
}

func showBlockedCommands(config *Config) {
	fmt.Println("🛡️ Blocked commands:")
	for i, cmd := range config.BlockedCommands {
		fmt.Printf("  %d. %s\n", i+1, cmd)
	}
}

func showStats(config *Config) {
	fmt.Println("📊 Usage Statistics:")
	
	data, err := os.ReadFile(config.UsageFile)
	if err != nil {
		fmt.Println("  No usage data available")
		return
	}
	
	lines := strings.Split(string(data), "\n")
	total := 0
	success := 0
	
	for _, line := range lines {
		if strings.TrimSpace(line) == "" {
			continue
		}
		total++
		if strings.Contains(line, "success") {
			success++
		}
	}
	
	fmt.Printf("  Total commands: %d\n", total)
	fmt.Printf("  Successful: %d\n", success)
	if total > 0 {
		fmt.Printf("  Success rate: %.1f%%\n", float64(success)/float64(total)*100)
	}
}

// MCP Protocol structures
type MCPRequest struct {
	JSONRPC string      `json:"jsonrpc"`
	ID      interface{} `json:"id"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
}

type MCPResponse struct {
	JSONRPC string      `json:"jsonrpc"`
	ID      interface{} `json:"id"`
	Result  interface{} `json:"result,omitempty"`
	Error   *MCPError   `json:"error,omitempty"`
}

type MCPError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

type MCPTool struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	InputSchema map[string]interface{} `json:"inputSchema"`
}

// MCP Server mode
func runMCPServer(config *Config) {
	for {
		var request MCPRequest
		decoder := json.NewDecoder(os.Stdin)
		if err := decoder.Decode(&request); err != nil {
			if err == io.EOF {
				break
			}
			continue
		}
		
		response := handleMCPRequest(config, &request)
		
		encoder := json.NewEncoder(os.Stdout)
		encoder.Encode(response)
	}
}

func handleMCPRequest(config *Config, request *MCPRequest) *MCPResponse {
	response := &MCPResponse{
		JSONRPC: "2.0",
		ID:      request.ID,
	}
	
	switch request.Method {
	case "initialize":
		response.Result = map[string]interface{}{
			"protocolVersion": "2024-11-05",
			"capabilities": map[string]interface{}{
				"tools": map[string]interface{}{},
			},
			"serverInfo": map[string]interface{}{
				"name":    "localops-assistant",
				"version": version,
			},
		}
		
	case "tools/list":
		response.Result = map[string]interface{}{
			"tools": []MCPTool{
				{
					Name:        "execute_system_command",
					Description: "Execute system commands using natural language with LocalOps Assistant",
					InputSchema: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"command": map[string]interface{}{
								"type":        "string",
								"description": "Natural language command to execute (e.g., 'show system info', 'list files', 'check memory')",
							},
						},
						"required": []string{"command"},
					},
				},
				{
					Name:        "get_system_info",
					Description: "Get comprehensive system information including CPU, memory, disk usage",
					InputSchema: map[string]interface{}{
						"type":       "object",
						"properties": map[string]interface{}{},
					},
				},
				{
					Name:        "list_files",
					Description: "List files and directories in the current or specified path",
					InputSchema: map[string]interface{}{
						"type": "object",
						"properties": map[string]interface{}{
							"path": map[string]interface{}{
								"type":        "string",
								"description": "Path to list (optional, defaults to current directory)",
							},
						},
					},
				},
			},
		}
		
	case "tools/call":
		params, ok := request.Params.(map[string]interface{})
		if !ok {
			response.Error = &MCPError{Code: -32602, Message: "Invalid params"}
			return response
		}
		
		toolName, ok := params["name"].(string)
		if !ok {
			response.Error = &MCPError{Code: -32602, Message: "Missing tool name"}
			return response
		}
		
		arguments, ok := params["arguments"].(map[string]interface{})
		if !ok {
			arguments = make(map[string]interface{})
		}
		
		result := executeMCPTool(config, toolName, arguments)
		response.Result = result
		
	default:
		response.Error = &MCPError{Code: -32601, Message: "Method not found"}
	}
	
	return response
}

func executeMCPTool(config *Config, toolName string, arguments map[string]interface{}) map[string]interface{} {
	switch toolName {
	case "execute_system_command":
		command, ok := arguments["command"].(string)
		if !ok {
			return map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": "Error: Missing or invalid command parameter",
					},
				},
			}
		}
		
		// Use the same logic as the main application
		suggestion := mapCommonCommands(command)
		if suggestion == "" && !isConversationalInput(command) {
			// Try AI suggestion
			var err error
			suggestion, err = getAISuggestion(config, command)
			if err != nil {
				return map[string]interface{}{
					"content": []map[string]interface{}{
						{
							"type": "text",
							"text": fmt.Sprintf("Error getting AI suggestion: %v", err),
						},
					},
				}
			}
		}
		
		if suggestion == "" {
			return map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": "Command processed (conversational response)",
					},
				},
			}
		}
		
		// Execute the command
		output, err := executeCommandForMCP(config, command, suggestion)
		if err != nil {
			return map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": fmt.Sprintf("Error executing command: %v", err),
					},
				},
			}
		}
		
		return map[string]interface{}{
			"content": []map[string]interface{}{
				{
					"type": "text",
					"text": fmt.Sprintf("Command: %s\nOutput:\n%s", suggestion, output),
				},
			},
		}
		
	case "get_system_info":
		output, err := executeCommandForMCP(config, "system info", 
			"echo '🖥️  SYSTEM OVERVIEW' && uname -a && echo -e '\n💾 CPU INFO:' && lscpu | head -10 && echo -e '\n🧠 MEMORY:' && free -h && echo -e '\n💿 DISK SPACE:' && df -h")
		if err != nil {
			return map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": fmt.Sprintf("Error getting system info: %v", err),
					},
				},
			}
		}
		
		return map[string]interface{}{
			"content": []map[string]interface{}{
				{
					"type": "text",
					"text": output,
				},
			},
		}
		
	case "list_files":
		path, ok := arguments["path"].(string)
		if !ok {
			path = "."
		}
		
		command := fmt.Sprintf("ls -la --color=never %s", path)
		output, err := executeCommandForMCP(config, "list files", command)
		if err != nil {
			return map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": fmt.Sprintf("Error listing files: %v", err),
					},
				},
			}
		}
		
		return map[string]interface{}{
			"content": []map[string]interface{}{
				{
					"type": "text",
					"text": output,
				},
			},
		}
		
	default:
		return map[string]interface{}{
			"content": []map[string]interface{}{
				{
					"type": "text",
					"text": "Unknown tool: " + toolName,
				},
			},
		}
	}
}

func executeCommandForMCP(config *Config, userInput, command string) (string, error) {
	// Check if command is blocked
	if config.isBlocked(command) {
		config.logUsage(userInput, command, "blocked")
		return "", fmt.Errorf("command blocked for safety")
	}
	
	// Execute command
	cmd := exec.Command("bash", "-c", command)
	output, err := cmd.CombinedOutput()
	
	if err != nil {
		config.logUsage(userInput, command, "error")
		return "", err
	}
	
	config.logUsage(userInput, command, "success")
	return strings.TrimSpace(string(output)), nil
}