import os
from typing import List

class Settings:
    # Database configuration (Defaults to local SQLite if DATABASE_URL is not set)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

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

    ADMIN_NOTIFICATION_EMAIL: str = os.getenv("ADMIN_NOTIFICATION_EMAIL", "singhalrajeev89@gmail.com")

    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    @property
    def DEFAULT_COACH_EMAILS(self) -> List[str]:
        emails_str = os.getenv("DEFAULT_COACH_EMAILS", "singhalrajeev89@gmail.com")
        emails = [email.strip().lower() for email in emails_str.split(",") if email.strip()]
        if "singhalrajeev89@gmail.com" not in emails:
            emails.append("singhalrajeev89@gmail.com")
        return emails

    @property
    def DEFAULT_SQUAD_PLAYERS(self) -> List[str]:
      squad_str = os.getenv(
          "DEFAULT_SQUAD_PLAYERS",
          "Alina, Ayana, Defne, Hannah, Kate, Kyra, Liz, Liv, Mira, Sai Jiya, Shanaya"
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

