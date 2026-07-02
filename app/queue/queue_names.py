
ALL_QUEUES = [

    # Document Pipeline
    "file.uploads",
    "rag.bulk_ingest",
    "embedding.processing",

    # Notification Pipeline
    "email.process",
    "sms.process",
    "push.process",
    "notify.bulk_email",
    "notify.bulk_sms",


    # AI Pipeline
    "ai.orchestration",
    "memory.processing",

    # Analytics
    "analytics.events",
]