# Agents: tools are a contract

Keep useful Claude agent instructions, then check the definition's tool names and repository-instruction settings for Copilot CLI. Use `/agent` to select the intended definition; resolve duplicate names before relying on one. The [focused investigator](../../examples/agents/focused-investigator.agent.md) and [repository reviewer](../../examples/agents/repository-reviewer.agent.md) allow only `view`, `grep` and `glob`, with no shell or edit tools. Ask for findings with file/line references and a proposed test.

Set `include-custom-instructions: true` when a custom subagent needs your repository rules; selecting the same agent as the main session is a different context. For a second opinion without a new definition, use `/rubber-duck`. For parallel investigations, see [fleet and subagents](../workflows/fleet-and-subagents.md), and keep one owner for implementation changes.
