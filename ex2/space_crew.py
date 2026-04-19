from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    """
    Enum for crew ranks.
    """
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """
    CrewMember model for individual space travelers.
    """
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field(default=Rank.OFFICER)
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """
    SpaceMission model with nested crew validation.
    """
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime | str = Field(default=datetime.now())
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_safety(self) -> 'SpaceMission':
        """
        Validate mission safety rules.
        """
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        high_ranking = [
            m for m in self.crew
            if m.rank in (Rank.COMMANDER, Rank.CAPTAIN)
        ]
        if not high_ranking:
            err = "Mission must have at least one Commander or Captain"
            raise ValueError(err)

        if self.duration_days > 365:
            exp_crew = [m for m in self.crew if m.years_experience >= 5]
            if len(exp_crew) / len(self.crew) < 0.5:
                err = "Long missions need at least 50% experienced crew"
                raise ValueError(err)

        inactive = [m for m in self.crew if not m.is_active]
        if inactive:
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    """
    Demonstration function for SpaceMission model.
    """
    print("Space Mission Crew Validation")
    print("========================================")

    try:
        crew = [
            CrewMember(
                member_id="C001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=45,
                specialization="Mission Command",
                years_experience=20
            ),
            CrewMember(
                member_id="L002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=30,
                specialization="Navigation",
                years_experience=8
            ),
            CrewMember(
                member_id="O003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=28,
                specialization="Engineering",
                years_experience=4
            )
        ]

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-06-01T08:00:00",
            duration_days=900,
            crew=crew,
            budget_millions=2500.0
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for m in mission.crew:
            print(f"- {m.name} ({m.rank.value}) - {m.specialization}")

    except ValidationError as e:
        print(f"Unexpected validation error: {e.errors()[0]['msg']}")

    print()
    print("========================================")

    print("Expected validation error:")
    try:
        invalid_crew = [
            CrewMember(
                member_id="CAD01",
                name="New Recruit",
                rank=Rank.CADET,
                age=20,
                specialization="Training",
                years_experience=0
            )
        ]
        SpaceMission(
            mission_id="M_FAIL_01",
            mission_name="Bad Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=10,
            crew=invalid_crew,
            budget_millions=100.0
        )
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, "):]
        print(msg)


if __name__ == "__main__":
    main()
