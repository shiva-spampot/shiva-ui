from flask import current_app
from psycopg2.extras import RealDictCursor


def get_email_details(email_id: int):
    query = """SELECT
        EMAILS.ID,
        CAMPAIGNS.SUBJECT,
        SENDERS.EMAIL,
        EMAILS.SENDER_IP,
        EMAILS.SEND_AT,
        CAMPAIGNS.EMAIL_BODY
    FROM
        EMAILS
        JOIN SENDERS ON SENDERS.ID = EMAILS.SENDER_ID
        JOIN CAMPAIGNS ON CAMPAIGNS.ID = EMAILS.CAMPAIGN_ID
    WHERE
        EMAILS.ID = %s
    """

    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(query, (email_id,))

    result = cursor.fetchone()

    return result


def get_recipients_for_email(email_id: int):
    query = """SELECT
        ARRAY_AGG(DISTINCT RECIPIENTS.EMAIL) AS UNIQUE_RECIPIENTS
    FROM
        RECIPIENTS_MAPPING
        JOIN RECIPIENTS ON RECIPIENTS.ID = RECIPIENTS_MAPPING.RECIPIENT_ID
    WHERE
        EMAIL_ID = %s"""
    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(query, (email_id,))

    result = cursor.fetchone()

    return result


def get_attachments_for_email(email_id: int):
    query = """SELECT
        ATTACHMENTS.*,
        COALESCE(
            (
                SELECT
                    JSONB_AGG(ATTACHMENT_RESULT)
            ),
            '[]'::JSONB
        ) AS ATTACHMENTS_DETAILS
    FROM
        ATTACHMENTS
        LEFT OUTER JOIN ATTACHMENT_RESULT ON ATTACHMENT_RESULT.ATTACHMENT_ID = ATTACHMENTS.ID
    WHERE
        ATTACHMENTS.ID IN (
            SELECT
                ATTACHMENT_ID
            FROM
                ATTACHMENT_MAPPING
            WHERE
                ATTACHMENT_MAPPING.EMAIL_ID = %s
        )
    GROUP BY
        ATTACHMENTS.ID"""
    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(query, (email_id,))

    result = cursor.fetchmany()

    return result


def get_urls_for_email(email_id: int):
    query = """SELECT
        COALESCE(
            (
                SELECT
                    JSONB_AGG(URLS)
            ),
            '[]'::JSONB
        ) AS URLS_DETAILS
    FROM
        URL_MAPPING
        JOIN URLS ON URLS.ID = URL_MAPPING.URL_ID
    WHERE URL_MAPPING.EMAIL_ID = %s"""
    conn = current_app.db
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(query, (email_id,))

    result = cursor.fetchone()

    return result
