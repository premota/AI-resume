# AgentFactory

The base building block for every AI agent in this project. It gives you a consistent way to define, initialise, and run a `pydantic-ai` agent without repeating the same boilerplate in every component.

---

## Why it exists

Every agent in this project (CV parser, JD parser, Matcher) needs the same things: a model, a system prompt, a typed output schema, optional tools, and a way to run. AgentFactory centralises all of that so each component only has to declare *what* it wants, not *how* to wire it up.

---

## Key files

| File | What it does |
|---|---|
| `agent_config.py` | Dataclass that holds an agent's settings — model name, prompt, output type, deps type, and optional tools |
| `agent.py` | Takes an `AgentConfig` and builds a `pydantic-ai` Agent. Lazy — only initialises on first call to `get_agent()` |
| `runner.py` | Single async function `run_agent()` that executes the agent and returns the typed output |
| `tool_registry.py` | Registers a list of tools onto an already-initialised agent |

---

## How to create a new agent

**1. Define your deps and output schema**
```python
from dataclasses import dataclass
from pydantic import BaseModel
from AgentFramework.AgentFactory.agent_config import AgentDeps

@dataclass(kw_only=True)
class MyDeps(AgentDeps):
    some_input: str

class MyOutput(BaseModel):
    result: str
```

**2. Create the agent via the factory**
```python
from AgentFramework.AgentFactory.agent import Agent
from AgentFramework.AgentFactory.agent_config import AgentConfig

def create_my_agent():
    config = AgentConfig(
        model="openai:gpt-4o",
        prompt="You are a helpful agent.",
        output=MyOutput,
        dep_types=MyDeps,
    )
    return Agent(config).get_agent()
```

**3. Run it**
```python
from AgentFramework.AgentFactory.runner import run_agent

result = await run_agent(
    agent=my_agent,
    user_prompt="execute",
    dependency=MyDeps(some_input="hello"),
    user_instruction="Do the thing with: hello",
)
```

**Adding tools** — pass them in `AgentConfig.tool` and the factory registers them automatically:
```python
def my_tool(ctx, query: str) -> str:
    return "result"

config = AgentConfig(..., tool=[my_tool])
```
