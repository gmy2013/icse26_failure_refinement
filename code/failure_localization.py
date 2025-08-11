import openai
import requests
from typing import List, Dict, Tuple

# Constants for OpenAI API
OPENAI_API_KEY = 'your_openai_api_key'


# Function to query the external knowledge base (e.g., reference solution repository)
import json
from typing import Optional


def retrieve_reference_solution(problem_description: str) -> Optional[str]:
    """
    Retrieve the reference solution for a given problem description from a local knowledge base.

    Args:
        problem_description (str): The description of the programming problem.

    Returns:
        str: The reference solution for the problem, or an empty string if not found.
    """
    try:
        # Open the local knowledge base (JSON file)
        with open('reference_solutions.json', 'r') as file:
            solutions_db = json.load(file)

        # Retrieve the solution based on the problem description
        solution = solutions_db.get(problem_description, "")

        return solution

    except FileNotFoundError:
        print("Error: Local knowledge base file 'reference_solutions.json' not found.")
        return ""

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the knowledge base file.")
        return ""



def localize_failure(agent_logs: List[Dict], problem_description: str) -> Dict:
    """
    Localizes the failure to specific agents by analyzing their actions, messages, and comparing with reference solutions.

    Args:
        agent_logs (List[Dict]): Logs of the actions and decisions made by each agent.
        problem_description (str): The problem description for the task.

    Returns:
        Dict: Mapping of agents to their responsibility score for the failure.
    """
    failure_localization = {}

    # Retrieve the reference solution for the given problem
    reference_solution = retrieve_reference_solution(problem_description)

    if not reference_solution:
        print(f"Error: Reference solution not found for problem: {problem_description}")
        return failure_localization  # No solution found in the repository

    # For each agent in the logs, generate a prompt and retrieve reasoning from OpenAI
    for agent_log in agent_logs:
        agent_name = agent_log["agent"]
        action = agent_log["action"]
        message = agent_log["message"]
        role = agent_log["role"]  # Added role of the agent

        # Construct the prompt based on the agent's role and action
        prompt = create_role_aware_prompt(agent_name, role, action, message, reference_solution)

        # Send the prompt to OpenAI and get the failure reasoning
        reasoning = reason_with_openai(prompt)

        # Analyze the reasoning to determine the responsibility score
        if "missing" in reasoning or "wrong" in reasoning:
            # Assign responsibility based on the nature of the failure
            failure_localization[agent_name] = failure_localization.get(agent_name, 0) + 0.25
        elif "misinterpreted" in reasoning or "overlooked" in reasoning:
            failure_localization[agent_name] = failure_localization.get(agent_name, 0) + 0.15
        elif "incorrect" in reasoning or "incomplete" in reasoning:
            failure_localization[agent_name] = failure_localization.get(agent_name, 0) + 0.2

    # Normalize the responsibility scores to sum to 1
    total_responsibility = sum(failure_localization.values())
    if total_responsibility > 0:
        for agent in failure_localization:
            failure_localization[agent] /= total_responsibility

    # If no agent is assigned any responsibility, we assign equal responsibility to all
    if total_responsibility == 0:
        for agent in agent_logs:
            failure_localization[agent["agent"]] = 1.0 / len(agent_logs)

    return failure_localization


def create_role_aware_prompt(agent_name: str, role: str, action: str, message: str, reference_solution: str) -> str:
    """
    Creates a detailed prompt based on the agent's role, action, and message to guide the reasoning process.

    Args:
        agent_name (str): Name of the agent.
        role (str): Role of the agent (Product Manager, Architect, Engineer, QA Engineer).
        action (str): The action taken by the agent.
        message (str): The message or explanation provided by the agent.
        reference_solution (str): The correct solution to the problem.

    Returns:
        str: A role-specific prompt for failure reasoning.
    """
    prompt = f"""
    You are a {role} responsible for a task in a collaborative code generation process.
    The problem description is: "{problem_description}"
    The reference solution is:
    "{reference_solution}"
    Your action was: "{action}"
    Your message was: "{message}"

    Based on the information provided above, explain whether your action or message caused the failure and if so, how it contributed to the error. 
    In your reasoning, consider common mistakes made by {role}s (e.g., product managers often misdefine constraints, architects may propose poor designs, engineers may implement incorrectly, QA engineers may miss edge cases).
    """

    return prompt


def reason_with_openai(prompt: str) -> str:
    """
    Sends the constructed prompt to OpenAI for reasoning and returns the response.

    Args:
        prompt (str): The prompt to be sent to OpenAI.

    Returns:
        str: The reasoning or feedback received from OpenAI.
    """
    # Example of how to interact with OpenAI's GPT model to get reasoning
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return "Error in reasoning"