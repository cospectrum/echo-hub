CREATE TYPE task_status AS ENUM ('completed', 'failed', 'in_progress');

CREATE TABLE IF NOT EXISTS transcribe_task(
    audio_key UUID PRIMARY KEY,
    status task_status NOT NULL,
    data jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
