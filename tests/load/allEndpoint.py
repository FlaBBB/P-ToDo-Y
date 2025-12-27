from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # DOSEN
    @task
    def get_dosen(self):
        self.client.get("/dosen")

    @task
    def create_dosen(self):
        payload = {
            "nama": "Dosen Test",
            "nidn": "9876543210",
            "prodi": "Teknik Informatika"
        }
        self.client.post("/dosen", json=payload)

    # MAHASISWA
    @task
    def get_mahasiswa(self):
        self.client.get("/mahasiswa")

    @task
    def create_mahasiswa(self):
        payload = {
            "nama": "Mahasiswa Test",
            "nim": "12345678",
            "jurusan": "Teknik Informatika"
        }
        self.client.post("/mahasiswa", json=payload)

    # JADWAL
    @task
    def get_jadwal(self):
        self.client.get("/jadwal")

    @task
    def create_jadwal(self):
        payload = {
            "hari": "Senin",
            "jam": "08:00-10:00",
            "mata_kuliah_id": 1,
            "dosen_id": 1
        }
        self.client.post("/jadwal", json=payload)

    # MATA KULIAH
    @task
    def get_mata_kuliah(self):
        self.client.get("/mata_kuliah")

    @task
    def create_mata_kuliah(self):
        payload = {
            "nama": "Matematika Diskrit",
            "kode": "MK001",
            "sks": 3
        }
        self.client.post("/mata_kuliah", json=payload)

    # TUGAS
    @task
    def get_tugas(self):
        self.client.get("/tugas")

    @task
    def create_tugas(self):
        payload = {
            "judul": "Tugas 1",
            "deskripsi": "Deskripsi tugas 1",
            "mahasiswa_id": 1,
            "mata_kuliah_id": 1
        }
        self.client.post("/tugas", json=payload)