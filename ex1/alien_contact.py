from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    """
    Enum for alien contact types.
    """
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """
    AlienContact model with custom business rule validation.
    """
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_contact_rules(self) -> 'AlienContact':
        """
        Apply custom business rules to the entire model.
        """
        # Rule 1: Contact ID must start with "AC"
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        # Rule 2: Physical contact reports must be verified
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        # Rule 3: Telepathic contact requires at least 3 witnesses
        if (self.contact_type == ContactType.TELEPATHIC and
                self.witness_count < 3):
            err_msg = "Telepathic contact requires at least 3 witnesses"
            raise ValueError(err_msg)

        # Rule 4: Strong signals (> 7.0) should include received messages
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) must include a message")

        return self


def main() -> None:
    """
    Demonstration function for AlienContact model.
    """
    print("Alien Contact Log Validation")
    print("=" * 38)

    # Valid contact report
    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2024-04-19T10:00:00",  # type: ignore[arg-type]
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}")

    print()
    print("=" * 38)

    # Invalid contact report (Telepathic with < 3 witnesses)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_TELE_01",
            timestamp=datetime.now(),
            location="Crop Circle, UK",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=1,  # Should fail (needs >= 3)
            message_received="Mind meld in progress"
        )
    except ValidationError as e:
        # Strip the 'Value error, ' prefix added by Pydantic v2
        msg = e.errors()[0]['msg']
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, "):]
        print(msg)


if __name__ == "__main__":
    main()
