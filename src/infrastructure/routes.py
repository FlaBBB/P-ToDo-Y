from datetime import date, datetime, time  # Import date, datetime, and time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos.mahasiswa_dto import (
    CreateMahasiswaDto,
    MahasiswaDto,
    UpdateMahasiswaDto,
)
from src.application.dtos.mata_kuliah_dto import (
    CreateMataKuliahDto,
    MataKuliahDto,
    UpdateMataKuliahDto,
)
from src.application.exceptions import (
    ApplicationException,
    DatabaseException,
    DuplicateEntryException,
    InvalidInputException,
    NotFoundException,
    RepositoryException,
)
from src.application.usecases.mahasiswa import MahasiswaService
from src.application.usecases.mata_kuliah import MataKuliahService
from src.dependencies import (  # Import the dependency from new dependencies file
    get_mahasiswa_service,
    get_mata_kuliah_service,
)
from src.ports.mahasiswa import GetMahasiswaPort
from src.ports.mata_kuliah import GetMataKuliahPort

mahasiswa_router = APIRouter()
mata_kuliah_router = APIRouter()


@mahasiswa_router.post(
    "/", response_model=MahasiswaDto, status_code=status.HTTP_201_CREATED
)
def create_mahasiswa(
    mahasiswa_dto: CreateMahasiswaDto,
    mahasiswa_service: MahasiswaService = Depends(get_mahasiswa_service),
):
    try:
        new_mahasiswa = mahasiswa_service.create(mahasiswa_dto)
        return new_mahasiswa
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except (DatabaseException, RepositoryException):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred.",
        )
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@mahasiswa_router.get("/", response_model=list[MahasiswaDto])
def read_mahasiswa(
    id: Optional[int] = None,
    nim: Optional[str] = None,
    nama: Optional[str] = None,
    kelas: Optional[str] = None,
    tempat_lahir: Optional[str] = None,
    tanggal_lahir: Optional[
        str
    ] = None,  # Use str for query param, convert here if needed
    order_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    mahasiswa_service: MahasiswaService = Depends(get_mahasiswa_service),
):
    parsed_tanggal_lahir: Optional[date] = None
    if tanggal_lahir:
        try:
            parsed_tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format for tanggal_lahir. Expected YYYY-MM-DD.",
            )

    get_mahasiswa_port = GetMahasiswaPort(
        id=id,
        nim=nim,
        nama=nama,
        kelas=kelas,
        tempat_lahir=tempat_lahir,
        tanggal_lahir=parsed_tanggal_lahir,  # Pass the converted date object
        order_by=order_by,
        order=order,
        limit=limit,
        page=page,
    )
    mahasiswa_list = mahasiswa_service.read(get_mahasiswa_port)
    return mahasiswa_list


@mahasiswa_router.put("/{mahasiswa_id}", response_model=MahasiswaDto)
def update_mahasiswa(
    mahasiswa_id: int,
    mahasiswa_dto: CreateMahasiswaDto,
    mahasiswa_service: MahasiswaService = Depends(get_mahasiswa_service),
):
    update_data = UpdateMahasiswaDto(
        id=mahasiswa_id,
        nim=mahasiswa_dto.nim,
        nama=mahasiswa_dto.nama,
        kelas=mahasiswa_dto.kelas,
        tempat_lahir=mahasiswa_dto.tempat_lahir,
        tanggal_lahir=mahasiswa_dto.tanggal_lahir,
        status=mahasiswa_dto.status,
    )
    try:
        updated_mahasiswa = mahasiswa_service.update(update_data)
        return updated_mahasiswa
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except (DatabaseException, RepositoryException):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred.",
        )
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# DELETE endpoint removed


# Mata Kuliah Routes


@mata_kuliah_router.post(
    "/", response_model=MataKuliahDto, status_code=status.HTTP_201_CREATED
)
def create_mata_kuliah(
    mata_kuliah_dto: CreateMataKuliahDto,
    mata_kuliah_service: MataKuliahService = Depends(get_mata_kuliah_service),
):
    try:
        new_mk = mata_kuliah_service.create(mata_kuliah_dto)
        return new_mk
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@mata_kuliah_router.get("/", response_model=list[MataKuliahDto])
def read_mata_kuliah(
    id: Optional[int] = None,
    kode_mk: Optional[str] = None,
    nama_mk: Optional[str] = None,
    sks: Optional[int] = None,
    order_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    mata_kuliah_service: MataKuliahService = Depends(get_mata_kuliah_service),
):
    get_mk_port = GetMataKuliahPort(
        id=id,
        kode_mk=kode_mk,
        nama_mk=nama_mk,
        sks=sks,
        order_by=order_by,
        order=order,
        limit=limit,
        page=page,
    )
    return mata_kuliah_service.read(get_mk_port)


@mata_kuliah_router.put("/{mata_kuliah_id}", response_model=MataKuliahDto)
def update_mata_kuliah(
    mata_kuliah_id: int,
    mata_kuliah_dto: CreateMataKuliahDto,
    mata_kuliah_service: MataKuliahService = Depends(get_mata_kuliah_service),
):
    update_data = UpdateMataKuliahDto(
        id=mata_kuliah_id,
        kode_mk=mata_kuliah_dto.kode_mk,
        nama_mk=mata_kuliah_dto.nama_mk,
        sks=mata_kuliah_dto.sks,
        is_active=mata_kuliah_dto.is_active,
    )
    try:
        return mata_kuliah_service.update(update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# DELETE endpoint removed


# Dosen Routes

from src.application.dtos.dosen_dto import (
    CreateDosenDto,
    DosenDto,
    UpdateDosenDto,
)
from src.application.usecases.dosen import DosenService
from src.dependencies import get_dosen_service
from src.ports.dosen import GetDosenPort

dosen_router = APIRouter()


@dosen_router.post("/", response_model=DosenDto, status_code=status.HTTP_201_CREATED)
def create_dosen(
    dosen_dto: CreateDosenDto,
    dosen_service: DosenService = Depends(get_dosen_service),
):
    try:
        new_dosen = dosen_service.create(dosen_dto)
        return new_dosen
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@dosen_router.get("/", response_model=list[DosenDto])
def read_dosen(
    id: Optional[int] = None,
    nidn: Optional[str] = None,
    nama: Optional[str] = None,
    email: Optional[str] = None,
    order_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    dosen_service: DosenService = Depends(get_dosen_service),
):
    get_dosen_port = GetDosenPort(
        id=id,
        nidn=nidn,
        nama=nama,
        email=email,
        order_by=order_by,
        order=order,
        limit=limit,
        page=page,
    )
    return dosen_service.read(get_dosen_port)


@dosen_router.put("/{dosen_id}", response_model=DosenDto)
def update_dosen(
    dosen_id: int,
    dosen_dto: CreateDosenDto,
    dosen_service: DosenService = Depends(get_dosen_service),
):
    update_data = UpdateDosenDto(
        id=dosen_id,
        nidn=dosen_dto.nidn,
        nama=dosen_dto.nama,
        email=dosen_dto.email,
        status=dosen_dto.status,
    )
    try:
        return dosen_service.update(update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# DELETE endpoint removed


# Jadwal Routes

from src.application.dtos.jadwal_dto import (
    CreateJadwalDto,
    JadwalDto,
    UpdateJadwalDto,
)
from src.application.usecases.jadwal import JadwalService
from src.dependencies import get_jadwal_service
from src.ports.jadwal import GetJadwalPort

jadwal_router = APIRouter()


@jadwal_router.post("/", response_model=JadwalDto, status_code=status.HTTP_201_CREATED)
def create_jadwal(
    jadwal_dto: CreateJadwalDto,
    jadwal_service: JadwalService = Depends(get_jadwal_service),
):
    try:
        new_jadwal = jadwal_service.create(jadwal_dto)
        return new_jadwal
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@jadwal_router.get("/", response_model=list[JadwalDto])
def read_jadwal(
    id: Optional[int] = None,
    hari: Optional[str] = None,
    jam_mulai: Optional[time] = None,
    jam_selesai: Optional[time] = None,
    ruangan: Optional[str] = None,
    mata_kuliah_id: Optional[int] = None,
    dosen_id: Optional[int] = None,
    order_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    jadwal_service: JadwalService = Depends(get_jadwal_service),
):
    get_jadwal_port = GetJadwalPort(
        id=id,
        hari=hari,
        jam_mulai=jam_mulai,
        jam_selesai=jam_selesai,
        ruangan=ruangan,
        mata_kuliah_id=mata_kuliah_id,
        dosen_id=dosen_id,
        order_by=order_by,
        order=order,
        limit=limit,
        page=page,
    )
    return jadwal_service.read(get_jadwal_port)


@jadwal_router.put("/{jadwal_id}", response_model=JadwalDto)
def update_jadwal(
    jadwal_id: int,
    jadwal_dto: CreateJadwalDto,
    jadwal_service: JadwalService = Depends(get_jadwal_service),
):
    update_data = UpdateJadwalDto(
        id=jadwal_id,
        hari=jadwal_dto.hari,
        jam_mulai=jadwal_dto.jam_mulai,
        jam_selesai=jadwal_dto.jam_selesai,
        ruangan=jadwal_dto.ruangan,
        mata_kuliah_id=jadwal_dto.mata_kuliah_id,
        dosen_id=jadwal_dto.dosen_id,
        is_active=jadwal_dto.is_active,
    )
    try:
        return jadwal_service.update(update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@jadwal_router.delete("/{jadwal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jadwal(
    jadwal_id: int,
    jadwal_service: JadwalService = Depends(get_jadwal_service),
):
    try:
        jadwal_service.delete(jadwal_id)
        return
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# Tugas Routes

from src.application.dtos.tugas_dto import (
    CreateTugasDto,
    StatusTugas,
    TugasDto,
    UpdateTugasDto,
)
from src.application.usecases.tugas import TugasService
from src.dependencies import get_tugas_service
from src.ports.tugas import GetTugasPort

tugas_router = APIRouter()


@tugas_router.post("/", response_model=TugasDto, status_code=status.HTTP_201_CREATED)
def create_tugas(
    tugas_dto: CreateTugasDto,
    tugas_service: TugasService = Depends(get_tugas_service),
):
    try:
        new_tugas = tugas_service.create(tugas_dto)
        return new_tugas
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@tugas_router.get("/", response_model=list[TugasDto])
def read_tugas(
    id: Optional[int] = None,
    judul: Optional[str] = None,
    status: Optional[StatusTugas] = None,
    mata_kuliah_id: Optional[int] = None,
    mahasiswa_id: Optional[int] = None,
    deadline_from: Optional[str] = None,
    deadline_to: Optional[str] = None,
    order_by: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    tugas_service: TugasService = Depends(get_tugas_service),
):
    parsed_deadline_from: Optional[datetime] = None
    if deadline_from:
        try:
            parsed_deadline_from = datetime.fromisoformat(deadline_from)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format for deadline_from. Expected ISO format.",
            )

    parsed_deadline_to: Optional[datetime] = None
    if deadline_to:
        try:
            parsed_deadline_to = datetime.fromisoformat(deadline_to)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format for deadline_to. Expected ISO format.",
            )

    get_tugas_port = GetTugasPort(
        id=id,
        judul=judul,
        status=status,
        mata_kuliah_id=mata_kuliah_id,
        mahasiswa_id=mahasiswa_id,
        deadline_from=parsed_deadline_from,
        deadline_to=parsed_deadline_to,
        order_by=order_by,
        order=order,
        limit=limit,
        page=page,
    )
    return tugas_service.read(get_tugas_port)


@tugas_router.put("/{tugas_id}", response_model=TugasDto)
def update_tugas(
    tugas_id: int,
    tugas_dto: CreateTugasDto,
    tugas_service: TugasService = Depends(get_tugas_service),
):
    update_data = UpdateTugasDto(
        id=tugas_id,
        judul=tugas_dto.judul,
        deskripsi=tugas_dto.deskripsi,
        deadline=tugas_dto.deadline,
        status=tugas_dto.status,
        mata_kuliah_id=tugas_dto.mata_kuliah_id,
        mahasiswa_id=tugas_dto.mahasiswa_id,
    )
    try:
        return tugas_service.update(update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@tugas_router.delete("/{tugas_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tugas(
    tugas_id: int,
    tugas_service: TugasService = Depends(get_tugas_service),
):
    try:
        tugas_service.delete(tugas_id)
        return
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
