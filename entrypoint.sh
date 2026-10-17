#!/bin/sh
set -e

echo "Waiting for database..."
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
    sleep 1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Copy Django admin static files to staticfiles for nginx
echo "Copying Django admin static files..."
mkdir -p /app/staticfiles/admin
cp -r /usr/local/lib/python3.12/site-packages/django/contrib/admin/static/admin /app/staticfiles/admin 2>/dev/null || true

# Fix nested admin/admin structure if it exists
if [ -d "/app/staticfiles/admin/admin" ]; then
    cp -r /app/staticfiles/admin/admin/* /app/staticfiles/admin/ 2>/dev/null || true
    rm -rf /app/staticfiles/admin/admin
fi

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
"

echo "Starting server..."
exec "$@"