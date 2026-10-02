from fastapi import HTTPException
from app.core.database import Database
from app.models.miembro_semillero import MiembroSemillero


class MiembroSemilleroRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM miembro_semillero ORDER BY id_miembro ASC;"
            )

            miembros = cursor.fetchall()
            conn.close()

            return miembros

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los miembros"
            )

    def obtener_por_id(self, miembro_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM miembro_semillero WHERE id_miembro = %s;",
                (miembro_id,)
            )

            miembro = cursor.fetchone()
            conn.close()

            if not miembro:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro no encontrado"
                )

            return miembro

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el miembro"
            )

    def crear(self, miembro: MiembroSemillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO miembro_semillero
                (id_usuario, id_semillero, fecha_ingreso, cargo, estado)
                VALUES (%s, %s, COALESCE(%s, CURRENT_DATE), %s, %s)
                RETURNING id_miembro;
            """

            cursor.execute(
                query,
                (
                    miembro.id_usuario,
                    miembro.id_semillero,
                    miembro.fecha_ingreso,
                    miembro.cargo,
                    miembro.estado
                )
            )

            nuevo_id = cursor.fetchone()["id_miembro"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el miembro"
            )

    def eliminar(self, miembro_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM miembro_semillero
                WHERE id_miembro = %s
                RETURNING id_miembro;
                """,
                (miembro_id,)
            )

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el miembro"
            )

    def actualizar(self, miembro_id: int, miembro: MiembroSemillero):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE miembro_semillero
                SET id_usuario = %s,
                    id_semillero = %s,
                    fecha_ingreso = %s,
                    cargo = %s,
                    estado = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_miembro = %s
                RETURNING id_miembro;
            """

            cursor.execute(
                query,
                (
                    miembro.id_usuario,
                    miembro.id_semillero,
                    miembro.fecha_ingreso,
                    miembro.cargo,
                    miembro.estado,
                    miembro_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Miembro no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el miembro"
            )