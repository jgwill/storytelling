#!/bin/bash

# Interactive Storytelling System - WillWrite
# Guided story generation with session management and knowledge base integration

set -e

# Colors for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/story_prompts"
KNOWLEDGE_BASE_DIR="$SCRIPT_DIR/knowledge_base"
OUTPUTS_DIR="$SCRIPT_DIR/generated_stories"

# Ensure directories exist
mkdir -p "$OUTPUTS_DIR" "$KNOWLEDGE_BASE_DIR"

# Helper functions
print_header() {
    echo -e "\n${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                    🌟 TAYI-SKA STORYTELLING SYSTEM 🌟${NC}"
    echo -e "${PURPLE}                    \"Weaver of Threads\" - Story Generator${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}\n"
}

print_section() {
    echo -e "\n${CYAN}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${WHITE}$1${NC} ${CYAN}│${NC}"
    echo -e "${CYAN}└─────────────────────────────────────────────────────────────────┘${NC}\n"
}

check_storytelling_installed() {
    if ! command -v storytelling &> /dev/null; then
        echo -e "${RED}❌ Error: 'storytelling' command not found${NC}"
        echo -e "${YELLOW}Please install the storytelling package:${NC}"
        echo -e "${GREEN}  cd $SCRIPT_DIR && pip install -e .${NC}"
        echo -e "${GREEN}  # or with full features: pip install -e .[all]${NC}"
        exit 1
    fi
}

list_available_prompts() {
    print_section "📚 Available Story Prompts"
    local i=1
    for prompt_file in "$PROMPTS_DIR"/*.txt; do
        if [[ -f "$prompt_file" ]]; then
            local filename=$(basename "$prompt_file" .txt)
            local title=$(head -n 1 "$prompt_file")
            echo -e "${GREEN}$i.${NC} ${WHITE}$title${NC}"
            echo -e "   ${CYAN}File: $filename.txt${NC}"
            echo
            ((i++))
        fi
    done
}

show_prompt_preview() {
    local prompt_file="$1"
    print_section "📖 Story Prompt Preview"
    echo -e "${WHITE}$(head -n 1 "$prompt_file")${NC}\n"
    echo -e "${CYAN}$(sed -n '3,8p' "$prompt_file")${NC}"
    echo -e "\n${YELLOW}... [content continues] ...${NC}\n"
}

list_sessions() {
    print_section "📋 Available Sessions"
    storytelling --list-sessions 2>/dev/null || echo -e "${YELLOW}No sessions found or storytelling not properly configured.${NC}"
}

session_info() {
    local session_id="$1"
    print_section "ℹ️  Session Information"
    storytelling --session-info "$session_id" 2>/dev/null || echo -e "${RED}Session not found: $session_id${NC}"
}

create_knowledge_base() {
    print_section "📚 Knowledge Base Setup"
    
    if [[ -d "$KNOWLEDGE_BASE_DIR" ]] && [[ -n "$(ls -A "$KNOWLEDGE_BASE_DIR"/*.md 2>/dev/null)" ]]; then
        echo -e "${GREEN}✅ Knowledge base directory exists with content:${NC}"
        ls -la "$KNOWLEDGE_BASE_DIR"/*.md 2>/dev/null | head -5
        echo
        read -p "$(echo -e "${YELLOW}Add more files to knowledge base? (y/n): ${NC}")" add_more
        if [[ "$add_more" =~ ^[Yy] ]]; then
            create_kb_content
        fi
    else
        echo -e "${YELLOW}📁 Creating knowledge base structure...${NC}"
        create_kb_content
    fi
}

create_kb_content() {
    echo -e "${CYAN}Creating sample knowledge base files...${NC}\n"
    
    # Indigenous Knowledge Systems
    cat > "$KNOWLEDGE_BASE_DIR/indigenous_knowledge_systems.md" << 'EOF'
# Indigenous Knowledge Systems

## Two-Eyed Seeing (Etuaptmumk)

Two-Eyed Seeing is a guiding principle developed by Mi'kmaq educators that encourages learning to see from one eye with the strengths of Indigenous knowledge and ways of knowing, and from the other eye with the strengths of Western knowledge and ways of knowing, and to use both eyes together for the benefit of all.

## Recursive Methodologies

Indigenous research often employs recursive methodologies where knowledge is built through iterative cycles of observation, reflection, and ceremonial integration. This differs from linear research models by embracing spiraling patterns of understanding.

## Land-Based Knowledge

Traditional knowledge is intimately connected to specific places and landscapes. This knowledge is not abstract but embodied, relational, and tied to the health and wellbeing of particular ecosystems and communities.
EOF

    # Ceremonial Practices
    cat > "$KNOWLEDGE_BASE_DIR/ceremonial_research_practices.md" << 'EOF'
# Ceremonial Research Practices

## Research as Ceremony

Shawn Wilson's concept that "research is ceremony" emphasizes that research should be conducted with the same respect, intentionality, and relational accountability as traditional ceremonies.

## Relational Accountability

Research must consider relationships - to community, to land, to ancestors, and to future generations. Knowledge creation is not extractive but reciprocal and responsible.

## Sacred Knowledge Protocols

Some knowledge is sacred and restricted, requiring specific protocols, permissions, and ceremonial contexts. Researchers must understand and respect these boundaries.
EOF

    # Traditional Technologies
    cat > "$KNOWLEDGE_BASE_DIR/traditional_technologies.md" << 'EOF'
# Traditional Technologies and Innovation

## Indigenous Computing Concepts

Many Indigenous cultures developed sophisticated information processing systems through beadwork, quipus, songlines, and other traditional technologies that encoded complex data and computational processes.

## Sustainable Design Principles

Traditional Indigenous building and design practices often incorporate principles of sustainability, biomimicry, and harmony with natural systems that are increasingly relevant to contemporary innovation.

## Algorithmic Thinking

Traditional practices like basket weaving, beadwork patterns, and textile creation often employ algorithmic thinking and recursive patterns that parallel modern computational concepts.
EOF

    echo -e "${GREEN}✅ Sample knowledge base created with 3 files${NC}"
    echo -e "${CYAN}Knowledge base location: $KNOWLEDGE_BASE_DIR${NC}\n"
    
    read -p "$(echo -e "${YELLOW}Would you like to add your own knowledge files? (y/n): ${NC}")" add_custom
    if [[ "$add_custom" =~ ^[Yy] ]]; then
        echo -e "${CYAN}You can add .md files to: $KNOWLEDGE_BASE_DIR${NC}"
        echo -e "${CYAN}Then restart this script to use them in story generation.${NC}"
        read -p "Press Enter to continue..."
    fi
}

generate_story() {
    local prompt_file="$1"
    local use_knowledge_base="$2"
    
    print_section "🎯 Story Generation Setup"
    
    # Get output filename
    local default_output="$(basename "$prompt_file" .txt)_$(date +%Y%m%d_%H%M%S)"
    read -p "$(echo -e "${YELLOW}Output filename (default: $default_output): ${NC}")" output_name
    output_name="${output_name:-$default_output}"
    
    # Build storytelling command
    local cmd="storytelling --prompt \"$prompt_file\" --output \"$OUTPUTS_DIR/$output_name\""
    
    # Add knowledge base if requested
    if [[ "$use_knowledge_base" == "yes" ]] && [[ -d "$KNOWLEDGE_BASE_DIR" ]]; then
        local kb_files_count=$(ls -1 "$KNOWLEDGE_BASE_DIR"/*.md 2>/dev/null | wc -l)
        if [[ "$kb_files_count" -gt 0 ]]; then
            cmd="$cmd --knowledge-base-path \"$KNOWLEDGE_BASE_DIR\" --embedding-model \"mxbai-embed-large:latest\""
            echo -e "${GREEN}✅ Using knowledge base with $kb_files_count files${NC}"
        else
            echo -e "${YELLOW}⚠️  Knowledge base directory exists but contains no .md files${NC}"
        fi
    fi
    
    # Advanced options
    read -p "$(echo -e "${YELLOW}Use debug mode for detailed logging? (y/n): ${NC}")" use_debug
    if [[ "$use_debug" =~ ^[Yy] ]]; then
        cmd="$cmd --debug"
    fi
    
    echo -e "\n${CYAN}Executing command:${NC}"
    echo -e "${WHITE}$cmd${NC}\n"
    
    # Execute the story generation
    if eval "$cmd"; then
        echo -e "\n${GREEN}✅ Story generation completed successfully!${NC}"
        echo -e "${CYAN}Output saved to: $OUTPUTS_DIR/$output_name${NC}"
        
        # Offer to view results
        read -p "$(echo -e "${YELLOW}View generated story? (y/n): ${NC}")" view_story
        if [[ "$view_story" =~ ^[Yy] ]]; then
            view_results "$output_name"
        fi
    else
        echo -e "\n${RED}❌ Story generation failed${NC}"
        echo -e "${YELLOW}Check the logs for details or try with --debug flag${NC}"
    fi
}

resume_session() {
    print_section "🔄 Resume Story Generation"
    
    # List available sessions
    storytelling --list-sessions 2>/dev/null || {
        echo -e "${YELLOW}No sessions found or storytelling not properly configured.${NC}"
        return 1
    }
    
    echo
    read -p "$(echo -e "${YELLOW}Enter session ID to resume: ${NC}")" session_id
    
    if [[ -z "$session_id" ]]; then
        echo -e "${RED}No session ID provided${NC}"
        return 1
    fi
    
    # Show session info first
    session_info "$session_id"
    
    echo
    read -p "$(echo -e "${YELLOW}Resume from specific node? (leave empty for auto): ${NC}")" resume_node
    
    # Build resume command
    local cmd="storytelling --resume \"$session_id\""
    if [[ -n "$resume_node" ]]; then
        cmd="$cmd --resume-from-node \"$resume_node\""
    fi
    
    echo -e "\n${CYAN}Executing command:${NC}"
    echo -e "${WHITE}$cmd${NC}\n"
    
    # Execute resume
    if eval "$cmd"; then
        echo -e "\n${GREEN}✅ Session resumed successfully!${NC}"
    else
        echo -e "\n${RED}❌ Failed to resume session${NC}"
    fi
}

view_results() {
    local output_name="$1"
    
    if [[ -z "$output_name" ]]; then
        print_section "📄 View Generated Stories"
        echo -e "${CYAN}Available generated stories:${NC}\n"
        
        if ls "$OUTPUTS_DIR"/* &>/dev/null; then
            local i=1
            for file in "$OUTPUTS_DIR"/*; do
                if [[ -f "$file" ]]; then
                    echo -e "${GREEN}$i.${NC} ${WHITE}$(basename "$file")${NC}"
                    echo -e "   ${CYAN}Modified: $(date -r "$file" '+%Y-%m-%d %H:%M:%S')${NC}"
                    echo
                    ((i++))
                fi
            done
            
            read -p "$(echo -e "${YELLOW}Enter number to view (or filename): ${NC}")" selection
            
            if [[ "$selection" =~ ^[0-9]+$ ]]; then
                local files=("$OUTPUTS_DIR"/*)
                local selected_file="${files[$((selection-1))]}"
                if [[ -f "$selected_file" ]]; then
                    output_name="$(basename "$selected_file")"
                fi
            else
                output_name="$selection"
            fi
        else
            echo -e "${YELLOW}No generated stories found in $OUTPUTS_DIR${NC}"
            return 1
        fi
    fi
    
    local file_path="$OUTPUTS_DIR/$output_name"
    
    if [[ -f "$file_path" ]]; then
        print_section "📖 Viewing: $output_name"
        
        # Use less for pagination if file is large
        if [[ $(wc -l < "$file_path") -gt 50 ]]; then
            echo -e "${CYAN}Opening in pager (press 'q' to quit)...${NC}\n"
            sleep 1
            less "$file_path"
        else
            cat "$file_path"
        fi
    else
        echo -e "${RED}File not found: $file_path${NC}"
    fi
}

# Main menu
main_menu() {
    while true; do
        print_header
        
        echo -e "${WHITE}What would you like to do?${NC}\n"
        echo -e "${GREEN}1.${NC} ${WHITE}Generate New Story${NC} - Create a story from available prompts"
        echo -e "${GREEN}2.${NC} ${WHITE}Resume Existing Session${NC} - Continue interrupted story generation"
        echo -e "${GREEN}3.${NC} ${WHITE}View Generated Stories${NC} - Read completed stories"
        echo -e "${GREEN}4.${NC} ${WHITE}Manage Sessions${NC} - List and inspect sessions"
        echo -e "${GREEN}5.${NC} ${WHITE}Setup Knowledge Base${NC} - Create/manage knowledge base for RAG"
        echo -e "${GREEN}6.${NC} ${WHITE}System Status${NC} - Check storytelling system health"
        echo -e "${RED}0.${NC} ${WHITE}Exit${NC}\n"
        
        read -p "$(echo -e "${YELLOW}Choose an option (0-6): ${NC}")" choice
        
        case $choice in
            1)
                # Generate new story
                list_available_prompts
                read -p "$(echo -e "${YELLOW}Select prompt number: ${NC}")" prompt_num
                
                local prompt_files=("$PROMPTS_DIR"/*.txt)
                local selected_prompt="${prompt_files[$((prompt_num-1))]}"
                
                if [[ -f "$selected_prompt" ]]; then
                    show_prompt_preview "$selected_prompt"
                    read -p "$(echo -e "${YELLOW}Use this prompt? (y/n): ${NC}")" confirm
                    
                    if [[ "$confirm" =~ ^[Yy] ]]; then
                        read -p "$(echo -e "${YELLOW}Use knowledge base for context? (y/n): ${NC}")" use_kb
                        if [[ "$use_kb" =~ ^[Yy] ]]; then
                            create_knowledge_base
                        fi
                        generate_story "$selected_prompt" "$use_kb"
                    fi
                else
                    echo -e "${RED}Invalid selection${NC}"
                fi
                ;;
            2)
                resume_session
                ;;
            3)
                view_results
                ;;
            4)
                list_sessions
                echo
                read -p "$(echo -e "${YELLOW}Enter session ID for details (or press Enter to continue): ${NC}")" session_id
                if [[ -n "$session_id" ]]; then
                    session_info "$session_id"
                fi
                ;;
            5)
                create_knowledge_base
                ;;
            6)
                print_section "🔧 System Status"
                echo -e "${CYAN}Checking storytelling installation...${NC}"
                if command -v storytelling &> /dev/null; then
                    echo -e "${GREEN}✅ storytelling command available${NC}"
                    storytelling --version 2>/dev/null || echo -e "${YELLOW}⚠️  Version info unavailable${NC}"
                else
                    echo -e "${RED}❌ storytelling command not found${NC}"
                fi
                
                echo -e "\n${CYAN}Directory structure:${NC}"
                echo -e "${GREEN}✅ Prompts: $PROMPTS_DIR ($(ls -1 "$PROMPTS_DIR"/*.txt 2>/dev/null | wc -l) files)${NC}"
                echo -e "${GREEN}✅ Knowledge base: $KNOWLEDGE_BASE_DIR ($(ls -1 "$KNOWLEDGE_BASE_DIR"/*.md 2>/dev/null | wc -l) files)${NC}"
                echo -e "${GREEN}✅ Outputs: $OUTPUTS_DIR ($(ls -1 "$OUTPUTS_DIR"/* 2>/dev/null | wc -l) files)${NC}"
                ;;
            0)
                echo -e "\n${PURPLE}Thank you for using Tayi-Ska Storytelling System!${NC}"
                echo -e "${CYAN}May your stories weave wisdom and wonder. 🌟${NC}\n"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Please choose 0-6.${NC}"
                ;;
        esac
        
        echo
        read -p "$(echo -e "${YELLOW}Press Enter to continue...${NC}")"
    done
}

# Check requirements and start
check_storytelling_installed
main_menu