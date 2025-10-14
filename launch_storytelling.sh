#!/bin/bash

# Quick Launch Script for Tayi-Ska Storytelling System
# This script provides quick access to common storytelling operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m'

print_banner() {
    echo -e "\n${PURPLE}🌟 TAYI-SKA STORYTELLING LAUNCHER 🌟${NC}"
    echo -e "${WHITE}Quick access to story generation tools${NC}\n"
}

print_banner

# Check if storytelling package is installed
if ! command -v storytelling &> /dev/null; then
    echo -e "${YELLOW}📦 Installing storytelling package...${NC}"
    cd "$SCRIPT_DIR"
    pip install -e . || {
        echo -e "${RED}❌ Failed to install storytelling package${NC}"
        echo -e "${YELLOW}Please ensure you're in a Python environment and try again${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Storytelling package installed${NC}\n"
fi

# Quick options
echo -e "${WHITE}Choose your path:${NC}\n"
echo -e "${GREEN}1.${NC} ${BLUE}🎭 Interactive Story Creator${NC} - Full guided experience"
echo -e "${GREEN}2.${NC} ${BLUE}📚 List Story Prompts${NC} - See available story seeds"
echo -e "${GREEN}3.${NC} ${BLUE}📋 View Sessions${NC} - Check story generation history"
echo -e "${GREEN}4.${NC} ${BLUE}⚡ Quick Generate${NC} - Generate story from first prompt"
echo -e "${GREEN}5.${NC} ${BLUE}🔧 System Check${NC} - Verify installation"

echo
read -p "$(echo -e "${YELLOW}Select option (1-5): ${NC}")" choice

case $choice in
    1)
        echo -e "\n${GREEN}🎭 Launching Interactive Story Creator...${NC}\n"
        exec "$SCRIPT_DIR/interactive_storytelling.sh"
        ;;
    2)
        echo -e "\n${BLUE}📚 Available Story Prompts:${NC}\n"
        for prompt in "$SCRIPT_DIR/story_prompts"/*.txt; do
            if [[ -f "$prompt" ]]; then
                title=$(head -n 1 "$prompt")
                echo -e "${GREEN}• ${title}${NC}"
                echo -e "  ${YELLOW}$(basename "$prompt")${NC}"
                echo
            fi
        done
        ;;
    3)
        echo -e "\n${BLUE}📋 Story Generation Sessions:${NC}\n"
        storytelling --list-sessions || echo -e "${YELLOW}No sessions found${NC}"
        ;;
    4)
        echo -e "\n${GREEN}⚡ Quick Story Generation...${NC}"
        first_prompt="$SCRIPT_DIR/story_prompts/01_spiral_of_memory.txt"
        if [[ -f "$first_prompt" ]]; then
            output_name="quick_story_$(date +%Y%m%d_%H%M%S)"
            echo -e "${BLUE}Generating story from: $(head -n 1 "$first_prompt")${NC}"
            storytelling --prompt "$first_prompt" --output "$SCRIPT_DIR/generated_stories/$output_name" --debug
        else
            echo -e "${YELLOW}No story prompts found${NC}"
        fi
        ;;
    5)
        echo -e "\n${BLUE}🔧 System Status Check:${NC}\n"
        
        echo -e "${GREEN}✓ Storytelling command:${NC}"
        storytelling --version 2>/dev/null || echo -e "${YELLOW}  Version unavailable${NC}"
        
        echo -e "\n${GREEN}✓ Directory structure:${NC}"
        echo -e "  Prompts: $(ls -1 "$SCRIPT_DIR/story_prompts"/*.txt 2>/dev/null | wc -l) files"
        echo -e "  Knowledge base: $(ls -1 "$SCRIPT_DIR/knowledge_base"/*.md 2>/dev/null | wc -l) files"
        echo -e "  Generated stories: $(ls -1 "$SCRIPT_DIR/generated_stories"/* 2>/dev/null | wc -l) files"
        
        echo -e "\n${GREEN}✓ Python environment:${NC}"
        python3 --version
        pip show storytelling 2>/dev/null | grep Version || echo -e "${YELLOW}  Package info unavailable${NC}"
        ;;
    *)
        echo -e "${YELLOW}Invalid option. Launching interactive mode...${NC}"
        exec "$SCRIPT_DIR/interactive_storytelling.sh"
        ;;
esac

echo -e "\n${PURPLE}Done! Use './interactive_storytelling.sh' for the full experience.${NC}"