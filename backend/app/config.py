import os
from typing import List

class Settings:
    # Resolve DB file location relative to this configuration module
    DATABASE_FILE: str = os.path.abspath(
        os.getenv(
            "DATABASE_FILE", 
            os.path.join(os.path.dirname(__file__), "../hockey_coach.db")
        )
    )

    # Defaults for first time DB seeding
    DEFAULT_GOOGLE_CLIENT_ID: str = os.getenv(
        "DEFAULT_GOOGLE_CLIENT_ID",
        "1083993716124-rle31j9i93h345fg33o536o5ur6vmp6s.apps.googleusercontent.com"
    )

    @property
    def DEFAULT_COACH_EMAILS(self) -> List[str]:
        emails_str = os.getenv("DEFAULT_COACH_EMAILS", "singhalrajeev89@gmail.com")
        return [email.strip().lower() for email in emails_str.split(",") if email.strip()]

    @property
    def DEFAULT_SQUAD_PLAYERS(self) -> List[str]:
      squad_str = os.getenv(
          "DEFAULT_SQUAD_PLAYERS",
          "Alina, Defne, Hannah, Kate, Kyra, Liz, Liv, Mira, Sai, Shanaya"
      )
      return [player.strip() for player in squad_str.split(",") if player.strip()]

    @property
    def DEFAULT_TRIMMERS_SQUAD_PLAYERS(self) -> List[str]:
      squad_str = os.getenv(
          "DEFAULT_TRIMMERS_SQUAD_PLAYERS",
          "André van der Sterre, Anna Erdmann-Witzel, Arold Boekhout, Boris Bonsel, Eelco Oudhof, Elise Visscher, Frances Handoko-de Man, Glenn Groenewegen, Gregor de Vries, Hester Kuis, Jeff Zwijsen, Marije Koelink, Marnix Langstraat, Noortje Semmelink, Norbert van Haaften, Rajeev Singhal, Robert-Jan van Weerd, Sander Duivesteijn, Saskia Klaverstijn, Tom Weller, Willem Reddingius"
      )
      return [player.strip() for player in squad_str.split(",") if player.strip()]

settings = Settings()
