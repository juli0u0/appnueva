from fastapi import APIRouter
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"]
)

repo = UsuarioRepository()


@router.get("/")
def listar_usuarios():
    return repo.obtener_todos()


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return repo.obtener_por_id(usuario_id)


@router.post("/")
def crear_usuario(usuario: Usuario):
    nuevo_id = repo.crear(usuario)

    return {
        "mensaje": "Usuario registrado exitosamente",
        "id": nuevo_id
    }


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    repo.eliminar(usuario_id)

    return {
        "mensaje": "Usuario eliminado correctamente"
    }


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario):
    repo.actualizar(usuario_id, usuario)

    return {
        "mensaje": "Usuario actualizado correctamente"
    }