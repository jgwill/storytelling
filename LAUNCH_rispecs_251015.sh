(cd /src/llms;git pull;cd /src/;tar cf - llms)|tar xvf - && cd llms && .__SYNC*sh
	pie;
mkdir -p .github
touch .github/copilot-instructions.md
geminii "look at features offered by this package @storytelling and using the rise-framework that you can observe in @__llms make sure that all the specs in @rispecs/ are up to date (we might have done differently in here or many features and capabilities are not yet implemented.). if you run the script you can observe in @pyproject.toml it should give you a great picture. Get aware of the whole picture before starting that work and create a file that will handoff that job to copilot-agent on github, create RISPECS.md and add adequate instruction to copilot so it knows everything that is hapenning in here.  We would expect that as end-results of your work prepared, copilot agent would completely upgrade and produce up to date files in ./rispecs - dont just write what for him, you have to analyze first the whole work."
