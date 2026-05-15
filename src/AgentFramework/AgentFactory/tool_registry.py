from typing import List
from pydantic_ai import Agent

from AgentFramework.AgentFactory.agent_config import Tool


class ToolRegistry:
    def __init__(self, agent: Agent, tool_list: List[Tool]):
        self.tools = tool_list
        self.agent = agent

    def register_tools(self) -> None:
        if self.tools:
            for each_tool in self.tools:
                self.agent.tool(each_tool)
