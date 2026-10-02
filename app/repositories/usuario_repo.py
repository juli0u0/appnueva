from fastapi import HTTPException
from app.core.database import Database
from app.models.usuario import Usuario


class UsuarioRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                ORDER BY id_usuario ASC;
            """)

            usuarios = cursor.fetchall()
            conn.close()

            return usuarios

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los usuarios"
            )

    def obtener_por_id(self, usuario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE id_usuario = %s;
            """, (usuario_id,))

            usuario = cursor.fetchone()
            conn.close()

            if not usuario:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            return usuario

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el usuario"
            )

    def crear(self, usuario: Usuario):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO usuario
                (
                    id_rol,
                    id_semillero,
                    nombre_usuario,
                    correo,
                    documento,
                    telefono,
                    fecha_registro,
                    id_estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario;
            """

            cursor.execute(
                query,
                (
                    usuario.id_rol,
                    usuario.id_semillero,
                    usuario.nombre_usuario,
                    usuario.correo,
                    usuario.documento,
                    usuario.telefono,
                    usuario.fecha_registro,
                    usuario.id_estado
                )
            )

            nuevo_id = cursor.fetchone()["id_usuario"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el usuario"
            )

    def eliminar(self, usuario_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM usuario
                WHERE id_usuario = %s
                RETURNING id_usuario;
            """, (usuario_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el usuario"
            )

    def actualizar(self, usuario_id: int, usuario: Usuario):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE usuario
                SET id_rol = %s,
                    id_semillero = %s,
                    nombre_usuario = %s,
                    correo = %s,
                    documento = %s,
                    telefono = %s,
                    fecha_registro = %s,
                    id_estado = %s
                WHERE id_usuario = %s
                RETURNING id_usuario;
            """

            cursor.execute(
                query,
                (
                    usuario.id_rol,
                    usuario.id_semillero,
                    usuario.nombre_usuario,
                    usuario.correo,
                    usuario.documento,
                    usuario.telefono,
                    usuario.fecha_registro,
                    usuario.id_estado,
                    usuario_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el usuario"
            )