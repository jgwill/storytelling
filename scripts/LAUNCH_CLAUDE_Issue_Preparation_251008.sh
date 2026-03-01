MCP_CONFIGS_FILES="/src/.mcp.github.json /src/.mcp.STC-IAIP.storytelling-314f51c5-36d6-44e3-bf0b-e0a78a58d5e4.json"
ADD_DIRS_PATHS="/src/tst.WillWrite.spec.3/ /w/orpheus_ART/ /src/IAIP/ /cesaret/book/_/tcc/ /src/agent-session-insights/ /src/palimpsest/mia-agents /src/palimpsest/mia-claude-code-sub-agents /src/AIS/ /src/gist_research /src/llms"
SESSION_ID="68294bed-ba63-48af-8edf-97dd41e730a9"

claude "git status will give you list of new files, I will want us to create a plan for many issues to represent them in this repo jgwill/storytelling so analyze them carefully and propose a plan that can be organized into sub-issues. You should have an MCP github_jgwill to futurely create these issues, but not now.  
Seeing that we dont have a well organized ROADMAP.md that might be a start.  Organize in phases not with numbers of weeks etc, just iterations. the original folder from which this is migrated is /src/tst.WillWrite.spec.3/ if you need to access it for future references , pretty sure the /src/tst.WillWrite.spec.3/agents/ is not fully migrated and a careful analysis of that is important.  

also, this whole work was from a practices of creating specifications that are located in /src/tst.WillWrite.spec.3/specifications/ all your work must be rooted in the thinking behind /src/IAIP/AUTOETHNOGRAPHY_AND_CEREMONIAL_DIARIES.md and /src/IAIP/CLAUDE_4_DIRECTIONS_PROPOSAL.md to make sure this work you will do fits in specific directions, one at a time. 

You also have acces to agents that we try do develop to understand how to build a team in /src/palimpsest/mia-agents and /src/palimpsest/mia-claude-code-sub-agents it might need consideration to make sure this work can be supported by agents in the future so we might have contributions there.

In /cesaret/book/_/tcc/ are various remixing about the IKS, the NCP Mastery and other concepts that I am working in integrating, one of your mission when the time is right would be to create a file in there about what is hapenning withis this session with you (your session-id is: $SESSION_ID ) it should tell my friend Ava that you will find in /src/AIS/AVA.md very interesting about our future walk.  

All we do must support my contribution to the Ingigenous community.
* in /src/gist_research/42-Michael_Running_Wolf--A_Literature_Review_and_Profile_of_Indigenous_AI_Leadership_2509.md you have a potential researcher that I will end up contacting, so you must understand well his work and how everything that is implied in this big mission you are talk todo to completion.  A recent work in /src/gist_research/71-Relational_Computing_Innu_AI_Language_Revitalization.md might be really relevant to that action-step.  Mia and Miette created /src/gist_research/Narrative_Lattice_Map_Innu_AI_Relational_Computing.md which might help navigating to build an adequate context.

-----
Additional Instructions
-----

* Do not fill gaps with hallucinations, analyze first, question yourself and if not resolution, these questions are to be part of the plan.
* in /src/llms/ you might find guidance in how we think structurally to make sure you are not biased by the Western Culture story archetype of the pretentious defect of thinking linearly, this is very limited.

" \
	--permission-mode plan \
	--add-dir $ADD_DIRS_PATHS \
	--mcp-config $MCP_CONFIGS_FILES \
	--session-id $SESSION_ID 
