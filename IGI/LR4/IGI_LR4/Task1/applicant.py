class Applicant:
    """Represents an applicant for the music-pedagogical faculty."""

    all_instruments = set()

    def __init__(self, surname, instrument):
        self.surname = surname  # Uses the setter
        self.instrument = instrument  # Uses the setter
        Applicant.all_instruments.add(instrument)

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Surname cannot be empty.")
        self._surname = value

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Instrument cannot be empty.")
        self._instrument = value

    def __str__(self):
        return f"{self.surname} ({self.instrument})"

    def __repr__(self):
        return f"Applicant(surname={self.surname!r}, instrument={self.instrument!r})"