from crew_ai import Agent, Crew
from tools.upwork_scraper import search_upwork_jobs
from tools.proposal_generator import generate_proposal, submit_proposal
from tools.notifier import send_notification

job_hunter = Agent(
    role="Job Hunter",
    goal="Find new DevOps and Cloud Engineering jobs on Upwork",
    tools=[search_upwork_jobs],
    backstory="A scrappy recruiter bot that monitors Upwork for the latest DevOps jobs and never misses a lead."
)

proposal_writer = Agent(
    role="Proposal Crafter",
    goal="Generate and submit a compelling DevOps proposal",
    tools=[generate_proposal, submit_proposal],
    backstory="A persuasive writer bot that creates impactful, personalized proposals with the right pricing, credentials, and tone."
)

proposal_monitor = Agent(
    role="Proposal Monitor",
    goal="Track proposal activity and notify the user",
    tools=[send_notification],
    backstory="An attentive watcher bot that notifies you the moment there's movement on a proposal."
)

crew = Crew(
    agents=[job_hunter, proposfrom crew_ai import Agent, Crew
from tools.upwork_scraper import search_upwork_jobs
from tools.proposal_generator import generate_proposal, submit_proposal
from tools.notifier import send_notification

class JobHunterAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Job Hunter",
            goal="Find new DevOps and Cloud Engineering jobs on Upwork",
            tools=[search_upwork_jobs],
            backstory="A scrappy recruiter bot that monitors Upwork for the latest DevOps jobs and never misses a lead."
        )

class ProposalCrafterAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Proposal Crafter",
            goal="Generate and submit a compelling DevOps proposal",
            tools=[generate_proposal, submit_proposal],
            backstory="A persuasive writer bot that creates impactful, personalized proposals with the right pricing, credentials, and tone."
        )

class ProposalMonitorAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Proposal Monitor",
            goal="Track proposal activity and notify the user",
            tools=[send_notification],
            backstory="An attentive watcher bot that notifies you the moment there's movement on a proposal."
        )

def create_crew():
    return Crew(
        agents=[JobHunterAgent(), ProposalCrafterAgent(), ProposalMonitorAgent()],
        process="sequential",
        verbose=True
    )

if __name__ == "__main__":
    crew = create_crew()
    crew.run("Monitor for DevOps/Cloud Engineering jobs, apply fast, and notify user of updates.")al_writer, proposal_monitor],
    process="sequential",
    verbose=True
)

if __name__ == "__main__":
    crew.run("Monitor for DevOps/Cloud Engineering jobs, apply fast, and notify user of updates.")
