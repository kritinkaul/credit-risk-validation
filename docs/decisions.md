# Engineering and research decisions

| Decision | Rationale and consequences |
| --- | --- |
| Foundation before experiments | A working config/CLI and explicit plan can be reviewed without invented results. No dataset or horizon is silently assumed. |
| Python 3.11+; quickstart on 3.11 | Maintain a clear minimum and test an additional recent interpreter in CI. `src/` packaging prevents accidental root imports. |
| uv lock plus optional extras | Default environment contains only config runtime and quality tools. Modeling, analytical and plotting extras are resolved but are not runtime-verified here. |
| Safe YAML plus strict Pydantic schema | Reject typos, coercion and duplicates. Explicit nulls describe unresolved choices; structural validity is not experiment readiness. |
| Local DuckDB/SQL planned | Inspectable analytical queries without service infrastructure. No database is created by validation. |
| Separate evaluation workflow | Frozen artifacts and a predeclared protocol reduce tuning leakage; one developer does not provide organizational independence. |
| Add modules when implemented | Avoid empty package trees and no-op training commands. Architecture docs define future boundaries. |
| MIT for original code | Dataset licenses are separate and must be checked before use or redistribution. |
| No CI badge initially | The workflow and observed run links are sufficient; do not imply passing status without evidence. |

Revise decisions with the motivating evidence and consequences. Defaults such as
seed 42 are engineering conveniences, not statistical guarantees or chosen model settings.
