import argparse
import os
import sys
from datetime import date, datetime
import random
from faker import Faker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from src.repositories.database.core import get_db_session, Base, engine
from src.repositories.database.mahasiswa import MahasiswaRepository
from src.application.usecases.mahasiswa import MahasiswaService
from src.application.dtos.mahasiswa_dto import CreateMahasiswaDto
from src.ports.mahasiswa import GetMahasiswaPort


def seed_database():
    """Populates the database with initial Mahasiswa data."""
    print("Ensuring all tables are created...")
    Base.metadata.create_all(bind=engine)

    db: Session = next(get_db_session())

    try:
        fake = Faker("id_ID")
        mahasiswa_repo = MahasiswaRepository(session_db=db)
        mahasiswa_service = MahasiswaService(mahasiswa_repo=mahasiswa_repo)

        num_records_to_generate = 10

        print(
            f"Generating and seeding {num_records_to_generate} fake Mahasiswa data..."
        )

        prodi_options = ["TI", "SIB"]
        current_year_prefix = str(datetime.now().year)[-2:]

        for _ in range(num_records_to_generate):
            nim_suffix = "".join(random.choices("0123456789", k=8))
            nim = f"{current_year_prefix}{nim_suffix}"

            prodi = random.choice(prodi_options)
            class_number = random.randint(1, 4)  # 1 ~ 4
            class_letter = random.choice([chr(ord("A") + i) for i in range(9)])  # A ~ I
            kelas = f"{prodi}-{class_number}{class_letter}"

            nama = fake.name()
            tempat_lahir = fake.city()
            tanggal_lahir = fake.date_of_birth(minimum_age=18, maximum_age=25)

            data = CreateMahasiswaDto(
                nim=nim,
                nama=nama,
                kelas=kelas,
                tempat_lahir=tempat_lahir,
                tanggal_lahir=tanggal_lahir,
            )

            existing_mahasiswa = mahasiswa_service.read(GetMahasiswaPort(nim=data.nim))
            if not existing_mahasiswa:
                mahasiswa_service.create(data)
                print(f"Created Mahasiswa: {data.nama} (NIM: {data.nim})")
            else:
                print(f"Mahasiswa with NIM {data.nim} already exists. Skipping.")

        print("Database seeding complete!")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Manage your P-ToDo-Y project.")
    parser.add_argument(
        "command",
        choices=["seed"],
        help="The command to run (e.g., 'seed' to populate the database with initial data).",
    )

    args = parser.parse_args()

    if args.command == "seed":
        seed_database()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()
