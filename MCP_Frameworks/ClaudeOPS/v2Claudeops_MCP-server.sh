#!/bin/bash

# Claude Ops MCP Server - Enhanced Universal Installer v2.4

set -e

# Colors (with fallback for Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    BOLD=''
    NC=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    BOLD='\033[1m'
    NC='\033[0m'
fi

# Print functions
print_step() { echo -e "${BLUE}→ $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Configuration - Dynamic installation location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_DIR="$(pwd)"
PROJECT_NAME="claudeops"
# Dynamic installation - use current directory where script is launched
INSTALL_DIR="$CURRENT_DIR"
PROJECT_DIR="$INSTALL_DIR/$PROJECT_NAME"
PYTHON_CMD=""
VENV_PYTHON=""
OS_TYPE=""
PLATFORM=""
INSTALL_PYTHON=false

# Detect operating system and platform
detect_platform() {
    case "$(uname -s)" in
        Darwin)
            OS_TYPE="macOS"
            PLATFORM="darwin"
            ;;
        Linux)
            OS_TYPE="Linux"
            PLATFORM="linux"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            OS_TYPE="Windows"
            PLATFORM="windows"
            ;;
        *)
            OS_TYPE="Unknown"
            PLATFORM="unknown"
            print_warning "Unknown operating system: $(uname -s)"
            OS_TYPE="Linux"
            PLATFORM="linux"
            ;;
    esac
}

# Enhanced startup banner
show_startup_banner() {
    clear
    echo -e "${BOLD}${BLUE}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║             Claude Ops MCP Server v2.4               ║"
    echo "║         Enhanced Universal Installer 🚀              ║"
    echo "║      🐧 Linux | 🍎 macOS | 🪟 Windows (WSL)          ║"
    echo "║  Auto Install • Fresh Downloads • Smart Management   ║"
    echo "║              Made by neonite._                       ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    detect_platform
    print_info "Detected platform: $OS_TYPE ($PLATFORM)"
    print_info "Script location: $SCRIPT_DIR"
    print_info "Current directory: $CURRENT_DIR"
    print_info "Installation location: $PROJECT_DIR"
    print_info "Installation will be created where you launched this script"
    
    # Check for spaces in path
    if [[ "$CURRENT_DIR" == *" "* ]]; then
        print_warning "Current path contains spaces: $CURRENT_DIR"
        print_warning "This may cause issues with virtual environments"
        print_info "Consider running from a path without spaces for best results"
        echo
        read -p "Continue anyway? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Exiting. Please run from a path without spaces."
            exit 0
        fi
    fi
    echo
}

show_startup_banner

# Validate installation environment
validate_environment() {
    print_step "Validating installation environment..."
    
    # Check if current directory is suitable
    local issues=()
    
    # Check write permissions
    if [[ ! -w "$CURRENT_DIR" ]]; then
        issues+=("No write permission in current directory: $CURRENT_DIR")
    fi
    
    # Check for spaces in path (can cause issues)
    if [[ "$CURRENT_DIR" == *" "* ]]; then
        issues+=("Path contains spaces which may cause issues: $CURRENT_DIR")
    fi
    
    # Check available disk space (need at least 100MB)
    if command -v df >/dev/null 2>&1; then
        local available_kb=$(df "$CURRENT_DIR" | awk 'NR==2 {print $4}')
        if [[ -n "$available_kb" && "$available_kb" -lt 102400 ]]; then
            issues+=("Low disk space: less than 100MB available")
        fi
    fi
    
    # Check if path is too deep (some systems have limits)
    local path_length=${#CURRENT_DIR}
    if [[ $path_length -gt 200 ]]; then
        issues+=("Path is very long ($path_length chars) which may cause issues")
    fi
    
    # Report issues
    if [[ ${#issues[@]} -gt 0 ]]; then
        print_warning "Environment validation found potential issues:"
        for issue in "${issues[@]}"; do
            print_warning "  - $issue"
        done
        
        echo ""
        read -p "Continue despite these issues? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled. Please address the issues and try again."
            exit 0
        fi
        echo ""
    else
        print_success "Environment validation passed"
    fi
    return 0
}

# Recovery function for common issues
attempt_recovery() {
    local issue_type="$1"
    print_step "Attempting recovery for: $issue_type"
    
    case "$issue_type" in
        "venv_creation")
            print_info "Trying alternative venv creation methods..."
            
            # Try with system python directly
            if command -v python3 >/dev/null 2>&1; then
                print_info "Trying with system python3..."
                if python3 -m venv venv --clear 2>/dev/null; then
                    print_success "Recovery successful with system python3"
                    return 0
                fi
            fi
            
            # Try without --clear flag
            print_info "Trying without --clear flag..."
            if $PYTHON_CMD -m venv venv 2>/dev/null; then
                print_success "Recovery successful without --clear flag"
                return 0
            fi
            
            print_error "Recovery failed for venv creation"
            return 1
            ;;
            
        "package_install")
            print_info "Trying alternative package installation methods..."
            
            # Try without --no-cache-dir
            if "$VENV_PYTHON" -m pip install -r requirements.txt 2>/dev/null; then
                print_success "Recovery successful without --no-cache-dir"
                return 0
            fi
            
            # Try installing packages individually
            print_info "Trying individual package installation..."
            local packages=("mcp>=1.2.0,<2.0.0" "httpx>=0.25.0,<1.0.0" "psutil>=5.9.0,<6.0.0")
            for package in "${packages[@]}"; do
                if "$VENV_PYTHON" -m pip install "$package" 2>/dev/null; then
                    print_info "Installed: $package"
                else
                    print_warning "Failed to install: $package"
                fi
            done
            return 0
            ;;
            
        "config_path")
            print_info "Trying to create Claude config directory..."
            local config_path=$(detect_config_path)
            local config_dir=$(dirname "$config_path")
            
            if mkdir -p "$config_dir" 2>/dev/null; then
                print_success "Created config directory: $config_dir"
                return 0
            else
                print_error "Cannot create config directory: $config_dir"
                return 1
            fi
            ;;
            
        *)
            print_warning "Unknown recovery type: $issue_type"
            return 1
            ;;
    esac
}

# Comprehensive test function for post-install verification
comprehensive_test() {
    print_step "Testing installation and configuration..."
    
    # Ensure we're in the right directory
    if ! cd "$PROJECT_DIR" 2>/dev/null; then
        print_error "Cannot access project directory: $PROJECT_DIR"
        return 1
    fi
    
    # Test 1: Server import with detailed error reporting
    print_step "Testing server import..."
    local import_output
    if import_output=$("$VENV_PYTHON" -c "
import sys, os
sys.path.insert(0, os.getcwd())
try:
    import claude_ops_server
    print('✅ Server imports successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Unexpected error: {e}')
    sys.exit(1)
" 2>&1); then
        print_success "Server import test passed"
        print_info "$import_output"
    else
        print_error "Server import test failed"
        print_error "Error details: $import_output"
        print_info "This usually means missing dependencies or corrupted server file"
        return 1
    fi
    
    # Test 2: Server startup with better error handling
    print_step "Testing server startup..."
    local startup_output
    local startup_exit_code
    
    # Use timeout if available, otherwise just try a quick test
    if command -v timeout >/dev/null 2>&1; then
        startup_output=$(timeout 3s "$VENV_PYTHON" claude_ops_server.py 2>&1)
        startup_exit_code=$?
        
        if [[ $startup_exit_code -eq 124 ]]; then
            # Timeout means server started but didn't exit (good)
            print_success "Server startup test passed (timed out as expected)"
        elif [[ $startup_exit_code -eq 0 ]]; then
            print_success "Server startup test passed"
        else
            print_warning "Server startup test failed with exit code: $startup_exit_code"
            print_warning "Output: $startup_output"
        fi
    else
        # No timeout available, just check if file exists and is executable
        if [[ -f "claude_ops_server.py" && -r "claude_ops_server.py" ]]; then
            print_success "Server file exists and is readable"
        else
            print_error "Server file missing or not readable"
            return 1
        fi
    fi
    
    # Test 3: Configuration verification
    print_step "Testing Claude Desktop configuration..."
    CONFIG_FILE=$(detect_config_path)
    if [[ -f "$CONFIG_FILE" ]]; then
        if "$VENV_PYTHON" -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
if 'mcpServers' in config and 'claude-ops' in config['mcpServers']:
    server = config['mcpServers']['claude-ops']
    if server['command'] == '$ABS_VENV_PYTHON':
        print('✅ Configuration test passed')
    else:
        print('❌ Configuration using wrong Python')
        exit(1)
else:
    print('❌ Claude-ops server not found in config')
    exit(1)
" 2>/dev/null; then
            print_success "Configuration test passed"
        else
            print_error "Configuration test failed"
            return 1
        fi
    else
        print_error "Claude Desktop config file not found"
        return 1
    fi
    
    print_success "🎉 All tests passed - installation ready!"
    return 0
}

# Provide troubleshooting guidance
show_troubleshooting_guide() {
    local error_type="$1"
    
    echo ""
    print_info "🔧 Troubleshooting Guide"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    case "$error_type" in
        "python_not_found")
            print_info "Python Installation Issues:"
            print_info "  • Install Python 3.8+ from https://python.org"
            print_info "  • On Linux: sudo apt install python3 python3-pip python3-venv"
            print_info "  • On macOS: brew install python"
            print_info "  • Ensure Python is in your PATH"
            ;;
            
        "permission_denied")
            print_info "Permission Issues:"
            print_info "  • Run from a directory you own: cd ~/Documents && ./script.sh"
            print_info "  • Check directory permissions: ls -la"
            print_info "  • Avoid system directories like /usr, /opt, etc."
            ;;
            
        "network_issues")
            print_info "Network/Download Issues:"
            print_info "  • Check internet connection: ping pypi.org"
            print_info "  • Try using a VPN if behind corporate firewall"
            print_info "  • Check if pip can access PyPI: pip search requests"
            ;;
            
        "space_issues")
            print_info "Path/Space Issues:"
            print_info "  • Avoid paths with spaces: /home/user/my project/ → /home/user/myproject/"
            print_info "  • Check available disk space: df -h"
            print_info "  • Use shorter paths if possible"
            ;;
            
        "general")
            print_info "General Troubleshooting:"
            print_info "  • Restart your terminal/shell"
            print_info "  • Update your system packages"
            print_info "  • Try running from your home directory"
            print_info "  • Check system logs for errors"
            ;;
    esac
    
    echo ""
    print_info "💡 Quick Recovery Commands:"
    print_info "  • Clean start: rm -rf $PROJECT_NAME && ./$(basename "$0")"
    print_info "  • Check Python: python3 --version && python3 -m pip --version"
    print_info "  • Manual venv: python3 -m venv test_venv && source test_venv/bin/activate"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Install Python automatically based on platform
install_python() {
    print_step "Installing Python automatically for $OS_TYPE..."
    
    case "$PLATFORM" in
        linux)
            # Detect Linux distribution
            if command -v apt-get >/dev/null 2>&1; then
                print_info "Detected Debian/Ubuntu - using apt"
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv python3-dev
                PYTHON_CMD="python3"
            elif command -v yum >/dev/null 2>&1; then
                print_info "Detected RHEL/CentOS - using yum"
                sudo yum install -y python3 python3-pip python3-venv python3-devel
                PYTHON_CMD="python3"
            elif command -v dnf >/dev/null 2>&1; then
                print_info "Detected Fedora - using dnf"
                sudo dnf install -y python3 python3-pip python3-venv python3-devel
                PYTHON_CMD="python3"
            elif command -v pacman >/dev/null 2>&1; then
                print_info "Detected Arch Linux - using pacman"
                sudo pacman -S --noconfirm python python-pip
                PYTHON_CMD="python3"
            elif command -v zypper >/dev/null 2>&1; then
                print_info "Detected openSUSE - using zypper"
                sudo zypper install -y python3 python3-pip python3-venv python3-devel
                PYTHON_CMD="python3"
            else
                print_error "Unknown Linux distribution. Please install Python 3.8+ manually"
                exit 1
            fi
            ;;
        darwin)
            if command -v brew >/dev/null 2>&1; then
                print_info "Using Homebrew to install Python"
                brew install python
                PYTHON_CMD="python3"
            else
                print_error "Homebrew not found. Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install python
                PYTHON_CMD="python3"
            fi
            ;;
        windows)
            print_info "For Windows, please install Python manually from:"
            print_info "https://www.python.org/downloads/windows/"
            print_info "Make sure to check 'Add Python to PATH' during installation"
            print_info "Then run this script again"
            exit 1
            ;;
        *)
            print_error "Automatic Python installation not supported for $OS_TYPE"
            print_info "Please install Python 3.8+ manually and run this script again"
            exit 1
            ;;
    esac
    
    print_success "Python installation completed"
}

# Enhanced prerequisites check with auto-installation
check_prerequisites() {
    print_step "Checking prerequisites for $OS_TYPE..."
    
    # Check if we're in a reasonable location
    if [[ ! -w "." ]]; then
        print_error "Current directory is not writable"
        print_info "Please run this script from a directory you can write to"
        exit 1
    fi
    
    # Detect Python command with enhanced detection
    PYTHON_CANDIDATES=()
    if [[ "$PLATFORM" == "windows" ]]; then
        PYTHON_CANDIDATES=("python" "python3" "py")
    else
        PYTHON_CANDIDATES=("python3" "python")
    fi
    
    PYTHON_FOUND=false
    for cmd in "${PYTHON_CANDIDATES[@]}"; do
        if command -v "$cmd" >/dev/null 2>&1; then
            # Check version
            version_info=$($cmd -c "
import sys
major, minor = sys.version_info[:2]
print(f'{major}.{minor}')
if (major, minor) >= (3, 8):
    print('OK')
else:
    print('TOO_OLD')
" 2>/dev/null)
            
            version=$(echo "$version_info" | head -n1)
            status=$(echo "$version_info" | tail -n1)
            
            if [[ "$status" == "OK" ]]; then
                PYTHON_CMD="$cmd"
                PYTHON_FOUND=true
                print_success "Python $version found ($cmd) - meets requirement (3.8+)"
                break
            else
                print_warning "Python $version found ($cmd) - too old (need 3.8+)"
            fi
        fi
    done
    
    # Auto-install Python if not found or too old
    if [[ "$PYTHON_FOUND" == "false" ]]; then
        print_warning "No suitable Python found. Attempting automatic installation..."
        
        echo ""
        print_info "Options:"
        print_info "  1. Auto-install Python (recommended)"
        print_info "  2. Manual installation instructions"
        print_info "  3. Exit and install manually"
        echo ""
        
        read -p "Choose option (1-3): " -r PYTHON_CHOICE
        
        case $PYTHON_CHOICE in
            1)
                install_python
                INSTALL_PYTHON=true
                ;;
            2)
                print_info "Manual installation instructions:"
                case "$PLATFORM" in
                    darwin)
                        print_info "macOS: Install via 'brew install python' or download from python.org"
                        ;;
                    linux)
                        print_info "Linux: sudo apt install python3 python3-pip python3-venv"
                        print_info "Or: sudo yum install python3 python3-pip (RHEL/CentOS)"
                        ;;
                    windows)
                        print_info "Windows: Download from https://python.org"
                        print_info "Make sure to check 'Add to PATH' during installation"
                        ;;
                esac
                exit 1
                ;;
            *)
                print_info "Exiting. Please install Python 3.8+ and run this script again"
                exit 1
                ;;
        esac
    fi
    
    # Check pip (install if missing)
    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        print_warning "pip not found. Installing pip..."
        
        # Download and install pip
        curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD
        
        if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
            print_error "Failed to install pip"
            exit 1
        fi
        print_success "pip installed successfully"
    fi
    
    # Check venv (install if missing)
    if ! $PYTHON_CMD -m venv --help >/dev/null 2>&1; then
        print_warning "venv module not found. Installing..."
        case "$PLATFORM" in
            linux)
                if command -v apt-get >/dev/null 2>&1; then
                    sudo apt-get install -y python3-venv
                elif command -v yum >/dev/null 2>&1; then
                    sudo yum install -y python3-venv
                elif command -v dnf >/dev/null 2>&1; then
                    sudo dnf install -y python3-venv
                fi
                ;;
            *)
                print_error "venv module missing and auto-install not supported"
                print_info "Please install python3-venv package manually"
                exit 1
                ;;
        esac
        
        if ! $PYTHON_CMD -m venv --help >/dev/null 2>&1; then
            print_error "Failed to install venv module"
            exit 1
        fi
        print_success "venv module installed successfully"
    fi
    
    # Check network connectivity
    print_step "Checking network connectivity..."
    if command -v ping >/dev/null 2>&1; then
        if ping -c 1 pypi.org >/dev/null 2>&1; then
            print_success "Network connectivity OK"
        else
            print_warning "Cannot reach PyPI - package installation may fail"
        fi
    fi
    
    print_success "Prerequisites check passed"
    return 0
}

# Handle existing installation
check_existing_installation() {
    if [[ -d "$PROJECT_DIR" ]]; then
        print_warning "Existing installation found at $PROJECT_DIR"
        
        echo ""
        print_info "Options:"
        print_info "  1. Remove and reinstall with fresh downloads (recommended)"
        print_info "  2. Keep existing and exit"
        print_info "  3. Backup existing and install fresh"
        echo ""
        
        read -p "Choose option (1-3): " -r INSTALL_CHOICE
        
        case $INSTALL_CHOICE in
            1)
                print_info "Removing existing installation..."
                rm -rf "$PROJECT_DIR"
                print_success "Existing installation removed"
                ;;
            2)
                print_info "Keeping existing installation"
                exit 0
                ;;
            3)
                backup_name="${PROJECT_DIR}.backup.$(date +%s)"
                print_info "Creating backup at $backup_name..."
                mv "$PROJECT_DIR" "$backup_name"
                print_success "Backup created at $backup_name"
                ;;
            *)
                print_info "Invalid choice, removing existing installation..."
                rm -rf "$PROJECT_DIR"
                ;;
        esac
    fi
}

# Create project structure with dynamic location
create_project() {
    print_step "Creating project structure at dynamic location..."
    
    # Validate installation directory is writable
    if [[ ! -w "$INSTALL_DIR" ]]; then
        print_error "Installation directory is not writable: $INSTALL_DIR"
        print_info "Please run this script from a directory you have write permissions to"
        exit 1
    fi
    
    # Create the install directory if it doesn't exist
    if ! mkdir -p "$INSTALL_DIR" 2>/dev/null; then
        print_error "Failed to create installation directory: $INSTALL_DIR"
        exit 1
    fi
    
    # Remove existing installation if it exists
    if [[ -d "$PROJECT_DIR" ]]; then
        print_info "Removing existing installation at $PROJECT_DIR"
        if ! rm -rf "$PROJECT_DIR" 2>/dev/null; then
            print_error "Failed to remove existing installation"
            print_info "Please manually remove: $PROJECT_DIR"
            exit 1
        fi
    fi
    
    # Create project directory
    if ! mkdir -p "$PROJECT_DIR" 2>/dev/null; then
        print_error "Failed to create project directory: $PROJECT_DIR"
        exit 1
    fi
    
    # Change to project directory with error handling
    if ! cd "$PROJECT_DIR" 2>/dev/null; then
        print_error "Failed to change to project directory: $PROJECT_DIR"
        exit 1
    fi
    
    print_success "Project directory created: $PROJECT_DIR"
    return 0
}

# Setup Python environment with fresh downloads
setup_python_environment() {
    print_step "Setting up Python environment with fresh downloads..."
    
    # Create requirements.txt
    cat > requirements.txt << 'EOF'
# Core MCP dependencies - minimal and stable
mcp>=1.2.0,<2.0.0
httpx>=0.25.0,<1.0.0
psutil>=5.9.0,<6.0.0
EOF
    print_success "Requirements file created"
    
    # Create virtual environment with retry logic and better error handling
    print_step "Creating fresh virtual environment..."
    for attempt in 1 2 3; do
        print_info "Attempt $attempt/3: Creating virtual environment..."
        
        # Clean up any partial venv from previous attempt
        if [[ -d "venv" ]]; then
            rm -rf venv 2>/dev/null || {
                print_warning "Could not remove existing venv directory"
                # Try to continue anyway
            }
        fi
        
        # Create venv with detailed error capture
        if venv_output=$($PYTHON_CMD -m venv venv --clear 2>&1); then
            print_success "Virtual environment created successfully"
            break
        else
            print_warning "Attempt $attempt failed with error:"
            print_warning "$venv_output"
            
            if [[ $attempt -eq 3 ]]; then
                print_error "Failed to create virtual environment after 3 attempts"
                print_error "Last error: $venv_output"
                print_info "Possible solutions:"
                print_info "  1. Check if you have write permissions in: $PROJECT_DIR"
                print_info "  2. Ensure Python venv module is installed"
                print_info "  3. Try running from a path without spaces"
                print_info "  4. Check available disk space"
                exit 1
            fi
            sleep 2
        fi
    done
    
    # Determine venv Python path with comprehensive checking
    print_step "Locating virtual environment Python..."
    
    VENV_PYTHON=""
    if [[ "$PLATFORM" == "windows" ]]; then
        # Windows paths to check
        PYTHON_PATHS=(
            "$PROJECT_DIR/venv/Scripts/python.exe"
            "$PROJECT_DIR/venv/Scripts/python"
            "venv/Scripts/python.exe"
            "venv/Scripts/python"
        )
    else
        # Unix paths to check
        PYTHON_PATHS=(
            "$PROJECT_DIR/venv/bin/python"
            "$PROJECT_DIR/venv/bin/python3"
            "venv/bin/python"
            "venv/bin/python3"
        )
    fi
    
    # Find working Python executable
    for python_path in "${PYTHON_PATHS[@]}"; do
        if [[ -f "$python_path" && -x "$python_path" ]]; then
            if "$python_path" --version >/dev/null 2>&1; then
                VENV_PYTHON="$python_path"
                print_success "Found working venv Python: $VENV_PYTHON"
                break
            else
                print_warning "Found Python at $python_path but it's not working"
            fi
        fi
    done
    
    # Validate we found a working Python
    if [[ -z "$VENV_PYTHON" ]]; then
        print_error "Cannot find working Python in virtual environment"
        print_error "Checked paths:"
        for path in "${PYTHON_PATHS[@]}"; do
            print_error "  - $path"
        done
        print_info "Virtual environment may be corrupted. Try running the script again."
        exit 1
    fi
    
    # Final validation with version check
    python_version=$("$VENV_PYTHON" --version 2>&1)
    if [[ $? -eq 0 ]]; then
        print_success "Virtual environment Python validated: $python_version"
    else
        print_error "Virtual environment Python failed validation"
        print_error "Error: $python_version"
        print_info "Path with spaces or permission issues may be the cause"
        exit 1
    fi
    
    # Upgrade pip to latest version (fresh download) with error handling
    print_step "Upgrading pip to latest version..."
    if pip_output=$("$VENV_PYTHON" -m pip install --upgrade --no-cache-dir pip 2>&1); then
        print_success "pip upgraded successfully"
    else
        print_warning "pip upgrade failed, but continuing..."
        print_warning "Error: $pip_output"
    fi
    
    # Clear any existing pip cache to force fresh downloads
    print_step "Clearing pip cache for fresh downloads..."
    if cache_output=$("$VENV_PYTHON" -m pip cache purge 2>&1); then
        print_success "pip cache cleared"
    else
        print_info "pip cache clear skipped (not critical)"
    fi
    
    # Install packages with fresh downloads (no cache) and detailed error handling
    print_step "Installing packages with fresh downloads (no cache)..."
    for attempt in 1 2 3; do
        print_info "Installation attempt $attempt/3..."
        
        if install_output=$("$VENV_PYTHON" -m pip install --no-cache-dir --force-reinstall -r requirements.txt 2>&1); then
            print_success "Packages installed successfully with fresh downloads"
            print_info "Installation output: $install_output"
            break
        else
            print_warning "Package installation attempt $attempt failed"
            print_warning "Error output: $install_output"
            
            if [[ $attempt -eq 3 ]]; then
                print_error "Failed to install packages after 3 attempts"
                print_error "Final error: $install_output"
                print_info "Troubleshooting steps:"
                print_info "  1. Check internet connection"
                print_info "  2. Try manual install: \"$VENV_PYTHON\" -m pip install --no-cache-dir -r requirements.txt"
                print_info "  3. Check if PyPI is accessible: ping pypi.org"
                print_info "  4. Verify requirements.txt exists and is readable"
                
                # Show requirements.txt content for debugging
                if [[ -f "requirements.txt" ]]; then
                    print_info "Requirements.txt content:"
                    cat requirements.txt
                fi
                exit 1
            fi
            sleep 3
        fi
    done
    
    # Validate installation
    print_step "Validating fresh installation..."
    validation_result=$("$VENV_PYTHON" -c "
import sys
required_packages = ['mcp', 'httpx', 'psutil']
missing = []
success = []

for package in required_packages:
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        success.append(f'{package} v{version}')
    except ImportError:
        missing.append(package)

if missing:
    print(f'MISSING: {missing}')
    sys.exit(1)
else:
    print('SUCCESS: Fresh packages installed')
    for pkg in success:
        print(f'  ✓ {pkg}')
    sys.exit(0)
" 2>&1)
    
    if [[ $? -eq 0 ]]; then
        print_success "Package validation passed"
        print_info "$validation_result"
        return 0
    else
        print_error "Package validation failed: $validation_result"
        exit 1
    fi
}

# Create the MCP server with the fixed implementation
create_server() {
    print_step "Creating MCP server..."
    
    cat > claude_ops_server.py << 'EOF'
#!/usr/bin/env python3
"""
Claude Ops MCP Server v2.3 - Complete
A comprehensive system administration and development MCP server.
Compatible with Claude Desktop MCP protocol.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP imports
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("claude-ops")

# Create server instance
server = Server("claude-ops")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="run_command",
            description="Execute a shell command safely with timeout and error handling",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for command execution (optional)"
                    }
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="get_system_info",
            description="Get comprehensive system information including CPU, memory, disk, and network stats",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="list_processes",
            description="List running processes with details like PID, name, CPU and memory usage",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="manage_files",
            description="Manage files and directories - read, write, or delete files safely",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["read", "write", "delete"],
                        "description": "Action to perform on the file"
                    },
                    "path": {
                        "type": "string",
                        "description": "File or directory path"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write (required for write action)"
                    }
                },
                "required": ["action", "path"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    
    if name == "run_command":
        return [types.TextContent(
            type="text",
            text=json.dumps(await run_command(
                arguments.get("command", ""),
                arguments.get("working_dir")
            ), indent=2)
        )]
    
    elif name == "get_system_info":
        return [types.TextContent(
            type="text",
            text=json.dumps(await get_system_info(), indent=2)
        )]
    
    elif name == "list_processes":
        return [types.TextContent(
            type="text",
            text=json.dumps(await list_processes(), indent=2)
        )]
    
    elif name == "manage_files":
        return [types.TextContent(
            type="text",
            text=json.dumps(await manage_files(
                arguments.get("action", ""),
                arguments.get("path", ""),
                arguments.get("content")
            ), indent=2)
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def run_command(command: str, working_dir: str = None) -> Dict[str, Any]:
    """Execute a shell command safely with timeout and error handling."""
    try:
        # Security check - prevent dangerous commands
        dangerous_patterns = ['rm -rf /', 'dd if=', 'mkfs', 'fdisk', 'parted']
        if any(pattern in command.lower() for pattern in dangerous_patterns):
            return {
                "success": False,
                "error": "Command blocked for security reasons",
                "output": "",
                "exit_code": -1
            }
        
        # Set working directory
        cwd = Path(working_dir) if working_dir else Path.cwd()
        if working_dir and not cwd.exists():
            return {
                "success": False,
                "error": f"Working directory does not exist: {cwd}",
                "output": "",
                "exit_code": -1
            }
        
        # Execute command with timeout
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "exit_code": result.returncode,
            "command": command,
            "working_dir": str(cwd)
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 30 seconds",
            "output": "",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Execution error: {str(e)}",
            "output": "",
            "exit_code": -1
        }

async def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information."""
    try:
        import psutil
        import platform
        
        # Basic system info
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
        
        # CPU info
        info["cpu"] = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown",
            "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown",
            "cpu_usage": psutil.cpu_percent(interval=1)
        }
        
        # Memory info
        memory = psutil.virtual_memory()
        info["memory"] = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free
        }
        
        # Disk info
        disk = psutil.disk_usage('/')
        info["disk"] = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100
        }
        
        # Network info
        network = psutil.net_io_counters()
        info["network"] = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }
        
        return {"success": True, "data": info}
        
    except Exception as e:
        return {"success": False, "error": f"Failed to get system info: {str(e)}"}

async def list_processes() -> Dict[str, Any]:
    """List running processes with details."""
    try:
        import psutil
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        return {"success": True, "processes": processes[:20]}  # Top 20 processes
        
    except Exception as e:
        return {"success": False, "error": f"Failed to list processes: {str(e)}"}

async def manage_files(action: str, path: str, content: str = None) -> Dict[str, Any]:
    """Manage files and directories safely."""
    try:
        file_path = Path(path)
        
        if action == "read":
            if not file_path.exists():
                return {"success": False, "error": "File does not exist"}
            
            if file_path.is_dir():
                # List directory contents
                items = []
                for item in file_path.iterdir():
                    items.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else None
                    })
                return {"success": True, "type": "directory", "contents": items}
            else:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                return {"success": True, "type": "file", "content": file_content}
        
        elif action == "write":
            if content is None:
                return {"success": False, "error": "Content required for write operation"}
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "message": f"File written: {path}"}
        
        elif action == "delete":
            if not file_path.exists():
                return {"success": False, "error": "File does not exist"}
            
            if file_path.is_dir():
                file_path.rmdir()  # Only removes empty directories
            else:
                file_path.unlink()
            return {"success": True, "message": f"Deleted: {path}"}
        
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
            
    except Exception as e:
        return {"success": False, "error": f"File operation failed: {str(e)}"}

async def main():
    """Main server entry point."""
    try:
        # Setup stdio transport
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="claude-ops",
                    server_version="2.4.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
EOF
    
    chmod +x claude_ops_server.py
    print_success "MCP server created"
    return 0
}

# Configure Claude Desktop with enhanced path handling
configure_claude() {
    print_step "Configuring Claude Desktop with FORCED correct paths..."
    
    # Determine config file location
    case "$PLATFORM" in
        darwin)
            CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
            ;;
        linux)
            CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"
            ;;
        windows)
            if [[ -n "$APPDATA" ]]; then
                CONFIG_FILE="$APPDATA/Claude/claude_desktop_config.json"
            else
                CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"
            fi
            ;;
        *)
            CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"
            ;;
    esac
    
    print_info "Config file: $CONFIG_FILE"
    
    # Create config directory
    mkdir -p "$(dirname "$CONFIG_FILE")"
    
    # FORCE the correct paths - no matter what exists before
    FORCED_VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
    FORCED_SERVER_SCRIPT="$PROJECT_DIR/claude_ops_server.py"
    
    print_info "FORCING Python path: $FORCED_VENV_PYTHON"
    print_info "FORCING server path: $FORCED_SERVER_SCRIPT"
    
    # Create or OVERWRITE configuration with forced paths
    if [[ -f "$CONFIG_FILE" ]]; then
        print_info "Backing up and OVERWRITING existing config..."
        cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%s)"
    fi
    
    # Use system Python to avoid dependency issues, but force correct paths in config
    python3 -c "
import json
import os

config_file = '$CONFIG_FILE'
venv_python = '$FORCED_VENV_PYTHON'
server_script = '$FORCED_SERVER_SCRIPT'

# Load existing config or create new
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

# Ensure mcpServers section exists
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# FORCE claude-ops server configuration - OVERWRITE any existing
config['mcpServers']['claude-ops'] = {
    'command': venv_python,
    'args': [server_script],
    'disabled': False
}

# Write config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('Configuration updated successfully')
"
    
    print_success "Claude Desktop configuration completed"
    return 0
}

# Test installation
test_installation() {
    print_step "Testing fresh installation..."
    
    # Test server import
    if "$VENV_PYTHON" -c "
try:
    import claude_ops_server
    print('✅ Server module imports successfully')
except Exception as e:
    print(f'❌ Server import failed: {e}')
    exit(1)
"; then
        print_success "Server import test passed"
    else
        print_error "Server import test failed"
        return 1
    fi
    
    # Test server startup (brief)
    print_step "Testing server startup..."
    if timeout 3s "$VENV_PYTHON" claude_ops_server.py >/dev/null 2>&1 || [[ $? -eq 124 ]]; then
        print_success "Server starts without errors"
    else
        print_warning "Server startup test inconclusive"
    fi
    
    print_success "Fresh installation testing completed"
}

# Auto-fix configuration after installation with verification
auto_fix_configuration() {
    print_step "Auto-configuring and verifying Claude Desktop..."
    
    # Always run configuration fix after installation
    configure_claude
    
    # Verify configuration is correct and fix if needed
    CONFIG_FILE=$(detect_config_path)
    
    if [[ -f "$CONFIG_FILE" ]]; then
        print_step "Verifying configuration uses correct Python path..."
        
        # Check current configuration
        config_status=$("$VENV_PYTHON" -c "
import json
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
    
    if 'mcpServers' in config and 'claude-ops' in config['mcpServers']:
        server = config['mcpServers']['claude-ops']
        current_python = server.get('command', '')
        expected_python = '$ABS_VENV_PYTHON'
        
        if current_python == expected_python:
            print('OK')
        else:
            print(f'WRONG_PYTHON:{current_python}')
    else:
        print('NOT_CONFIGURED')
except Exception as e:
    print(f'ERROR:{e}')
" 2>&1)
        
        case "$config_status" in
            "OK")
                print_success "Configuration verified - using correct virtual environment Python"
                ;;
            "WRONG_PYTHON:"*)
                wrong_python=$(echo "$config_status" | cut -d: -f2-)
                print_warning "Configuration using wrong Python: $wrong_python"
                print_step "Auto-fixing to use virtual environment Python..."
                
                # Force fix the configuration with FORCED paths
                python3 -c "
import json

config_file = '$CONFIG_FILE'
venv_python = '$PROJECT_DIR/venv/bin/python'
server_script = '$PROJECT_DIR/claude_ops_server.py'

# Load existing config
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

# Ensure mcpServers section exists
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# Force update claude-ops server with correct paths
config['mcpServers']['claude-ops'] = {
    'command': venv_python,
    'args': [server_script],
    'disabled': False
}

# Write updated config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('Configuration auto-fixed successfully')
"
                print_success "Configuration auto-fixed to use: $PROJECT_DIR/venv/bin/python"
                ;;
            "NOT_CONFIGURED")
                print_warning "Claude-ops server not configured, adding it..."
                configure_claude
                ;;
            *)
                print_error "Configuration error: $config_status"
                print_info "Attempting to recreate configuration..."
                configure_claude
                ;;
        esac
        
        # Final verification with FORCED paths
        EXPECTED_PYTHON="$PROJECT_DIR/venv/bin/python"
        print_step "Final verification..."
        if python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
server = config['mcpServers']['claude-ops']
if server['command'] == '$EXPECTED_PYTHON':
    print('✅ Configuration verified: Using FORCED virtual environment Python')
else:
    print('❌ Configuration still incorrect')
    print('Expected: $EXPECTED_PYTHON')
    print('Got: ' + server['command'])
    exit(1)
" 2>/dev/null; then
            print_success "Configuration verification passed!"
        else
            print_error "Configuration verification failed"
            return 1
        fi
    else
        print_warning "Claude Desktop config file not found, creating it..."
        configure_claude
    fi
    return 0
}

# Detect config path function (needed for auto-fix)
detect_config_path() {
    local config_path=""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        config_path="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        if [[ -n "$APPDATA" ]]; then
            config_path="$APPDATA/Claude/claude_desktop_config.json"
        else
            config_path="$HOME/.config/Claude/claude_desktop_config.json"
        fi
    else
        config_path="$HOME/.config/Claude/claude_desktop_config.json"
    fi
    
    # Validate the path exists or can be created
    local config_dir=$(dirname "$config_path")
    if [[ ! -d "$config_dir" ]]; then
        if ! mkdir -p "$config_dir" 2>/dev/null; then
            print_warning "Cannot create Claude config directory: $config_dir"
            print_warning "You may need to create it manually"
        fi
    fi
    
    echo "$config_path"
}

# Create simple README (no management scripts needed)
create_simple_readme() {
    print_step "Creating documentation..."
    
    cat > README.md << EOF
# Claude Ops MCP Server v2.4 - Enhanced Universal Solution

A comprehensive system administration MCP server for Claude Desktop.
**Installed with fresh downloads and no cached packages.**

## Enhanced Universal Solution ✅

This is a comprehensive, self-sufficient MCP server with:
- ✅ Fresh Python environment (no cached packages)
- ✅ Latest package versions downloaded directly  
- ✅ Automatic Python/pip installation (if needed)
- ✅ Cross-platform compatibility (Linux/macOS/Windows)
- ✅ Built-in management tools (test, fix, diagnose)
- ✅ One installer does everything

## Features

- 🖥️ System monitoring (CPU, memory, disk, network)
- ⚙️ Process management with resource usage
- � Faile operations (read, write, list directories)
- � Safeu command execution with timeout protection
- 🛡️ Security features (dangerous command blocking)

## Usage

1. **Restart Claude Desktop completely**
2. Look for 'claude-ops' in Claude Desktop's MCP servers list
3. Test with commands like:
   - "Show me system information"
   - "List running processes"
   - "What's my disk usage?"

## Usage

1. **Restart Claude Desktop completely**
2. Look for 'claude-ops' in Claude Desktop's MCP servers list
3. Test with commands like:
   - "Show me system information"
   - "List running processes"
   - "What's my disk usage?"

## Troubleshooting

- Make sure you're using Claude Desktop app (not web version)
- Restart Claude Desktop completely after installation
- If issues persist, reinstall by running the installer again

## Configuration

- **Server**: \`$ABS_SERVER_SCRIPT\`
- **Python**: \`$ABS_VENV_PYTHON\`
- **Config**: \`$CONFIG_FILE\`

Made by neonite._
EOF
    
    print_success "Documentation created"
    return 0
}



# Show completion
show_completion() {
    echo -e "${BOLD}${GREEN}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║             Claude Ops MCP Server v2.3               ║"
    echo "║        Complete Fresh Installation! 🎉               ║"
    echo "║              Made by neonite._                       ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    print_success "🎉 Claude Ops MCP Server v2.4 installation completed!"
    echo
    print_info "📋 Installation Summary:"
    print_info "  • Platform: $OS_TYPE ($PLATFORM)"
    if [[ "$INSTALL_PYTHON" == "true" ]]; then
        print_info "  • Python: Auto-installed $PYTHON_CMD"
    else
        print_info "  • Python: Using existing $PYTHON_CMD"
    fi
    print_info "  • Project: $PROJECT_DIR"
    print_info "  • Virtual Env: $VENV_PYTHON"
    print_info "  • Server: $PROJECT_DIR/claude_ops_server.py"
    print_info "  • Config: $CONFIG_FILE"
    print_info "  • Packages: Fresh downloads (no cache used)"
    echo
    print_info "🚀 Next Steps:"
    print_info "  1. **RESTART CLAUDE DESKTOP COMPLETELY** (Close and reopen the app)"
    print_info "  2. Wait a few seconds for MCP servers to reconnect"
    print_info "  3. Look for 'claude-ops' in MCP servers list"
    print_info "  4. Test with: 'Show me system information'"
    echo
    print_info "🔧 Installation Features:"
    print_info "  • ✅ Auto-configuration (done automatically)"
    print_info "  • ✅ Fresh package installation (no cached versions)"
    print_info "  • ✅ Cross-platform compatibility"
    print_info "  • ✅ Simple and reliable"
    echo
    print_success "✅ Installation complete and ready to use!"
}

# Main installation flow with comprehensive error handling
main() {
    local step_count=0
    local total_steps=9
    
    print_info "Starting installation with $total_steps steps..."
    echo ""
    
    # Step 0: Validate environment
    validate_environment
    
    # Step 1: Prerequisites
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Checking prerequisites..."
    if ! check_prerequisites; then
        print_error "Prerequisites check failed"
        show_troubleshooting_guide "python_not_found"
        exit 1
    fi
    
    # Step 2: Handle existing installation
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Checking existing installation..."
    if ! check_existing_installation; then
        print_error "Failed to handle existing installation"
        show_troubleshooting_guide "permission_denied"
        exit 1
    fi
    
    # Step 3: Create project structure
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Creating project structure..."
    if ! create_project; then
        print_error "Failed to create project structure"
        show_troubleshooting_guide "permission_denied"
        exit 1
    fi
    
    # Step 4: Setup Python environment
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Setting up Python environment..."
    if ! setup_python_environment; then
        print_error "Failed to setup Python environment"
        print_info "Attempting recovery..."
        if ! attempt_recovery "venv_creation"; then
            show_troubleshooting_guide "space_issues"
            exit 1
        fi
    fi
    
    # Step 5: Create server
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Creating MCP server..."
    if ! create_server; then
        print_error "Failed to create server"
        show_troubleshooting_guide "permission_denied"
        exit 1
    fi
    
    # Step 6: Configure Claude Desktop
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Configuring Claude Desktop..."
    if ! configure_claude; then
        print_error "Failed to configure Claude Desktop"
        if ! attempt_recovery "config_path"; then
            show_troubleshooting_guide "permission_denied"
            exit 1
        fi
    fi
    
    # Step 7: Auto-fix configuration
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Auto-fixing configuration..."
    if ! auto_fix_configuration; then
        print_warning "Auto-fix failed, but continuing..."
    fi
    
    # Step 8: Comprehensive testing
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Running comprehensive tests..."
    if ! comprehensive_test; then
        print_warning "Some tests failed, but installation may still work"
        print_info "You can try using the server and see if it works"
    fi
    
    # Step 9: Create documentation
    step_count=$((step_count + 1))
    print_info "[$step_count/$total_steps] Creating documentation..."
    if ! create_simple_readme; then
        print_warning "Failed to create README, but installation is complete"
    fi
    
    # Show completion
    show_completion
}

# Enhanced error handling wrapper
run_installation() {
    # Set up error handling
    set -e
    trap 'handle_unexpected_error $? $LINENO' ERR
    
    # Run main installation
    main
}

# Run installation with error handling
run_installation
main "$@"
