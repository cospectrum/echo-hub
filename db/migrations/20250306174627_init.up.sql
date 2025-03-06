CREATE TABLE IF NOT EXISTS speech_to_text_task_result(
    audio_key UUID PRIMARY KEY,
    data jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
