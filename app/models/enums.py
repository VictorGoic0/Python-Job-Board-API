import enum


class JobType(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"


class ExperienceLevel(enum.Enum):
    ENTRY = "ENTRY"
    MID = "MID"
    SENIOR = "SENIOR"


class RemoteOption(enum.Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"
