from fastapi import APIRouter, HTTPException

from app.models.modulo_x_rol import ModuloXRol
from app.repositories.modulo_x_rol_repo import ModuloXRolRepository


router = APIRouter(
    prefix="/modulos-x-rol",
    tags=["Gestión de Módulos por Rol"]
)

repo = ModuloXRolRepository()


@router.get("/")
def listar_modulos_x_rol():
    return repo.obtener_todos()


@router.get("/{moduloxrol_id}")
def obtener_modulo_x_rol(moduloxrol_id: int):
    registro = repo.obtener_por_id(moduloxrol_id)

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return registro


@router.post("/")
def crear_modulo_x_rol(moduloxrol: ModuloXRol):
    nuevo_id = repo.crear(moduloxrol)

    return {
        "mensaje": "Módulo asignado al rol exitosamente",
        "id": nuevo_id
    }


@router.delete("/{moduloxrol_id}")
def eliminar_modulo_x_rol(moduloxrol_id: int):
    exito = repo.eliminar(moduloxrol_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Asignación eliminada correctamente"
    }


@router.put("/{moduloxrol_id}")
def actualizar_modulo_x_rol(
    moduloxrol_id: int,
    moduloxrol: ModuloXRol
):
    exito = repo.actualizar(moduloxrol_id, moduloxrol)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return {
        "mensaje": "Asignación actualizada correctamente"
    }