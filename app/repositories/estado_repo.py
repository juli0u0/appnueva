from fastapi import HTTPException
from app.core.database import Database
from app.models.estado import Estado


class EstadoRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estado
                ORDER BY id_estado ASC;
            """)

            estados = cursor.fetchall()
            conn.close()

            return estados

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener los estados"
            )

    def obtener_por_id(self, estado_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estado
                WHERE id_estado = %s;
            """, (estado_id,))

            estado = cursor.fetchone()
            conn.close()

            if not estado:
                raise HTTPException(
                    status_code=404,
                    detail="Estado no encontrado"
                )

            return estado

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al obtener el estado"
            )

    def crear(self, estado: Estado):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO estado
                (nombre, categoria, descripcion)
                VALUES (%s, %s, %s)
                RETURNING id_estado;
            """

            cursor.execute(
                query,
                (
                    estado.nombre,
                    estado.categoria,
                    estado.descripcion
                )
            )

            nuevo_id = cursor.fetchone()["id_estado"]

            conn.commit()
            conn.close()

            return nuevo_id

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el estado"
            )

    def eliminar(self, estado_id: int):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM estado
                WHERE id_estado = %s
                RETURNING id_estado;
            """, (estado_id,))

            eliminado = cursor.fetchone()

            conn.commit()
            conn.close()

            if eliminado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Estado no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el estado"
            )

    def actualizar(self, estado_id: int, estado: Estado):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE estado
                SET nombre = %s,
                    categoria = %s,
                    descripcion = %s
                WHERE id_estado = %s
                RETURNING id_estado;
            """

            cursor.execute(
                query,
                (
                    estado.nombre,
                    estado.categoria,
                    estado.descripcion,
                    estado_id
                )
            )

            actualizado = cursor.fetchone()

            conn.commit()
            conn.close()

            if actualizado is None:
                raise HTTPException(
                    status_code=404,
                    detail="Estado no encontrado"
                )

            return True

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el estado"
            )