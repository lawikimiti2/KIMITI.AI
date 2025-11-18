#!/usr/bin/env sh
set -e

wait_for_host() {
  HOST="$1"; PORT="$2"; TIMEOUT="${3:-60}"
  echo "Waiting for $HOST:$PORT (timeout ${TIMEOUT}s)..."
  HOST="$HOST" PORT="$PORT" TIMEOUT="$TIMEOUT" python - <<'PY'
import os, socket, sys, time
host=os.environ.get('HOST')
port=int(os.environ.get('PORT','0') or '0')
timeout=int(os.environ.get('TIMEOUT','60') or '60')
end=time.time()+timeout
while time.time()<end:
    s=socket.socket(); s.settimeout(2)
    try:
        s.connect((host, port)); s.close(); sys.exit(0)
    except Exception:
        time.sleep(1)
print(f'Timeout waiting for {host}:{port}')
sys.exit(1)
PY
}

# Wait for Postgres if DATABASE_URL points to db service
DB_HOST="${DATABASE_HOST:-db}"
DB_PORT="${DATABASE_PORT:-5432}"
wait_for_host "$DB_HOST" "$DB_PORT" 90

# Apply migrations (best-effort)
if command -v alembic >/dev/null 2>&1; then
  echo "Running alembic upgrade head..."
  alembic upgrade head || echo "Alembic failed (continuing)."
fi

# Start API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
