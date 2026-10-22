"""Strict foundation configuration validation, separate from future data checks."""

from pathlib import Path
from typing import Annotated, Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

NonEmptyText = Annotated[str, Field(min_length=1, pattern=r"\S")]


class ConfigError(ValueError):
    """A configuration file cannot be read or does not satisfy the schema."""


class StrictSection(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Project(StrictSection):
    name: Literal["credit-risk-validation"]
    stage: Literal["foundation"]


class Dataset(StrictSection):
    name: NonEmptyText | None
    source: NonEmptyText | None


class Target(StrictSection):
    definition: NonEmptyText | None
    horizon_days: Annotated[int, Field(gt=0)] | None


class Evaluation(StrictSection):
    split_strategy: Literal["pending", "temporal", "grouped"]
    observation_timestamp_column: NonEmptyText | None
    borrower_id_column: NonEmptyText | None

    @model_validator(mode="after")
    def check_split_columns(self) -> Self:
        if self.split_strategy == "temporal" and self.observation_timestamp_column is None:
            raise ValueError("temporal splitting requires observation_timestamp_column")
        if self.split_strategy == "grouped" and self.borrower_id_column is None:
            raise ValueError("grouped splitting requires borrower_id_column")
        return self


class Storage(StrictSection):
    engine: Literal["duckdb"]
    path: NonEmptyText


class Config(StrictSection):
    project: Project
    dataset: Dataset
    target: Target
    evaluation: Evaluation
    storage: Storage
    random_seed: Annotated[int, Field(ge=0, le=2**32 - 1)]


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently taking the last value."""


def _unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str):
            raise ConfigError("YAML mapping keys must be strings")
        if key in mapping:
            raise ConfigError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def load_config(path: str | Path) -> Config:
    """Read safe YAML and validate structure; do not access data or create files."""
    try:
        with Path(path).open(encoding="utf-8") as handle:
            payload = yaml.load(handle, Loader=UniqueKeyLoader)
        return Config.model_validate(payload)
    except (OSError, UnicodeError, yaml.YAMLError, ValidationError) as exc:
        # Do not echo input values: local configurations may contain private information.
        if isinstance(exc, ValidationError):
            details = "; ".join(
                f"{'.'.join(map(str, error['loc'])) or 'root'}: {error['type']}"
                for error in exc.errors()
            )
            raise ConfigError(f"Schema validation failed: {details}") from exc
        raise ConfigError(f"Cannot read configuration ({type(exc).__name__})") from exc
