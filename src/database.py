from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def serialize_incident(row: dict) -> dict:
    return dict(row)


async def create_incident(
    db,
    *,
    title: str,
    description: str,
    requester: str,
    area: str,
    category: str | None = None,
    priority: str = "media",
    impact_users: int = 1,
    urgency: str = "media",
) -> dict:
    now = utc_now()

    statement = db.prepare(
        """
        INSERT INTO incidents (
            title,
            description,
            requester,
            area,
            category,
            status,
            priority,
            impact_users,
            urgency,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'aberto', ?, ?, ?, ?, ?)
        RETURNING *
        """
    ).bind(
        title,
        description,
        requester,
        area,
        category,
        priority,
        impact_users,
        urgency,
        now,
        now,
    )

    row = await statement.first()

    if row is None:
        raise RuntimeError("Não foi possível criar o incidente.")

    return serialize_incident(row)


async def list_incidents(
    db,
    *,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    statement = db.prepare(
        """
        SELECT *
        FROM incidents
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
    ).bind(limit, offset)

    result = await statement.run()

    return [serialize_incident(row) for row in result.results]


async def get_incident(db, incident_id: int) -> dict | None:
    statement = db.prepare(
        """
        SELECT *
        FROM incidents
        WHERE id = ?
        LIMIT 1
        """
    ).bind(incident_id)

    row = await statement.first()

    if row is None:
        return None

    return serialize_incident(row)


async def update_incident(
    db,
    incident_id: int,
    *,
    status: str | None = None,
    priority: str | None = None,
) -> dict | None:
    current = await get_incident(db, incident_id)

    if current is None:
        return None

    new_status = status if status is not None else current["status"]
    new_priority = priority if priority is not None else current["priority"]
    now = utc_now()

    statement = db.prepare(
        """
        UPDATE incidents
        SET
            status = ?,
            priority = ?,
            updated_at = ?
        WHERE id = ?
        RETURNING *
        """
    ).bind(
        new_status,
        new_priority,
        now,
        incident_id,
    )

    row = await statement.first()

    if row is None:
        raise RuntimeError("Não foi possível atualizar o incidente.")

    return serialize_incident(row)
