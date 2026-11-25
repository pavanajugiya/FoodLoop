# Compatibility for XAMPP MariaDB with modern Django
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# Bypass version check (Django expects MariaDB 10.11+)
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# MariaDB 10.4 does not support INSERT ... RETURNING
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
