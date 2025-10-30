from typing import Optional
from datetime import date, datetime # Import date and datetime
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.dtos.mahasiswa_dto import CreateMahasiswaDto, UpdateMahasiswaDto, MahasiswaDto
from src.application.usecases.mahasiswa import MahasiswaService
from src.ports.mahasiswa import GetMahasiswaPort
from src.dependencies import get_mahasiswa_service  # Import the dependency from new dependencies file
from src.application.exceptions import (
    NotFoundException,
    DuplicateEntryException,
    InvalidInputException,
    ApplicationException,
    DatabaseException,
    RepositoryException,
)

mahasiswa_router = APIRouter()


@mahasiswa_router.post("/", response_model=MahasiswaDto, status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except (DatabaseException, RepositoryException) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="A database error occurred.")
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@mahasiswa_router.get("/", response_model=list[MahasiswaDto])
def read_mahasiswa(
    id: Optional[int] = None,
    nim: Optional[str] = None,
    nama: Optional[str] = None,
    kelas: Optional[str] = None,
    tempat_lahir: Optional[str] = None,
    tanggal_lahir: Optional[str] = None, # Use str for query param, convert here if needed
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
                detail="Invalid date format for tanggal_lahir. Expected YYYY-MM-DD."
            )

    get_mahasiswa_port = GetMahasiswaPort(
        id=id,
        nim=nim,
        nama=nama,
        kelas=kelas,
        tempat_lahir=tempat_lahir,
        tanggal_lahir=parsed_tanggal_lahir, # Pass the converted date object
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
    mahasiswa_dto: CreateMahasiswaDto,  # Re-using CreateDTO for update input for now, consider a specific UpdateInputDTO
    mahasiswa_service: MahasiswaService = Depends(get_mahasiswa_service),
):
    update_data = UpdateMahasiswaDto(
        id=mahasiswa_id,
        nim=mahasiswa_dto.nim,
        nama=mahasiswa_dto.nama,
        kelas=mahasiswa_dto.kelas,
        tempat_lahir=mahasiswa_dto.tempat_lahir,
        tanggal_lahir=mahasiswa_dto.tanggal_lahir,
    )
    try:
        updated_mahasiswa = mahasiswa_service.update(update_data)
        return updated_mahasiswa
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidInputException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except (DatabaseException, RepositoryException) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="A database error occurred.")
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@mahasiswa_router.delete("/{mahasiswa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mahasiswa(
    mahasiswa_id: int,
    mahasiswa_service: MahasiswaService = Depends(get_mahasiswa_service),
):
    try:
        success = mahasiswa_service.delete(mahasiswa_id)
        if not success: # This branch might not be hit if NotFoundException is always raised
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mahasiswa with id {mahasiswa_id} not found")
        return
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except (DatabaseException, RepositoryException) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="A database error occurred.")
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
