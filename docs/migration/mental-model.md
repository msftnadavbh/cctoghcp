# Mental model: four independent controls

Claude Code habits transfer by **outcome**, not by identical command name. Copilot has (1) planning, (2) continuation, (3) permissions, and (4) parallel workers. `/plan` investigates and produces a reviewable plan; it does not make the OS read-only. `/autopilot` changes how turns continue, not which paths or websites are safe. `--available-tools` hides tools from the model; `--allow-tool`, path verification and URL grants are separate checks. `/fleet` changes scheduling, not authority.

Start in [your own repository](../start/use-copilot-in-your-repository.md): inspect inherited instructions, trace a real task, approve a bounded edit separately and run your project's checks. Copilot entitlement does not require GitHub repository hosting or grant a GitLab token. [Hosting boundaries](../hosting/capability-boundaries.md). Reproduction and tests outrank a convincing generated summary.

Your local Copilot transcript, Git revision, task list and published review are different objects; none should be described as another. For customization use the [compatibility table](compatibility.md); for optional known-result practice use [exercises](../scenarios/index.md). Check [version and platform requirements](../reference/versions.md) before using version-specific features.
