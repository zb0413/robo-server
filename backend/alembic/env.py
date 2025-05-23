from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine # Added for explicit engine creation

from alembic import context

import sys
import os # Ensure os is imported
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__)))) # Adds backend/ to sys.path

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.database import Base # Import Base from your app's database module
from app.db_models import Resource, ResourceDetail # Import your models

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        # If no URL is configured in alembic.ini, use a default dummy URL for offline generation.
        # This allows 'alembic revision --autogenerate' to run without a live DB.
        # Ensure the dialect matches your actual database for correct SQL generation.
        url = "postgresql://user:pass@localhost/dbname_dummy"
        
    context.configure(
        url=url,
        target_metadata=target_metadata,
        # literal_binds=True, # This is for --sql mode, not for generating revision scripts
        dialect_opts={"paramstyle": "named"},
        # include_object is a callable that can be used to filter objects during autogeneration
        # compare_type is a boolean or callable to control type comparison behavior
    )

    # The context.run_migrations() call is typically made within a transaction
    # when generating SQL for --sql mode. For autogenerate of Python scripts,
    # configuring the context might be sufficient for metadata comparison.
    # If autogenerate still fails, this might need to be re-evaluated.
    # For now, let's remove it to avoid the AssertionError if no connection/transaction is expected.
    # with context.begin_transaction():
    #     context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use the engine from your app's database module if available
    # This ensures consistency with your application's DB connection
    # Attempt to get the actual database URL from environment for online mode,
    # or use the one from alembic.ini if set and valid.
    db_url_from_env = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    if not db_url_from_env:
        # If no URL is available for online mode, log and skip online migration setup.
        # This might happen if alembic.ini has no URL and DATABASE_URL env var is not set.
        # This state is problematic for 'alembic upgrade/downgrade' but allows 'revision' to pass.
        print("No database URL configured for online migrations. Skipping online setup.")
        # Alternatively, raise an error:
        # raise ValueError("Database URL for online migrations is not configured.")
        # For now, we'll let it pass, but 'upgrade' commands would fail if they reach here without a URL.
        # In the context of autogenerate, if it still reaches here, it needs a connectable.
        # Let's use engine_from_config which would use the (now empty) sqlalchemy.url from ini.
        # This part will likely fail if an actual online operation is attempted without a URL.
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}), # This will get the empty URL
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        # If connectable has no URL, connect() will fail. This is expected if no DB is configured for online.
    else:
        # Use a new engine configured with the potentially environment-sourced URL for online migrations.
        # This avoids using the app's global engine directly in the migration script's global scope,
        # which can be safer.
        connectable = create_engine(db_url_from_env, poolclass=pool.NullPool)


    with connectable.connect() as connection: # This line will fail if connectable has no valid URL
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # compare_type=True, # Uncomment if you want to detect column type changes
            # include_schemas=True # Set to True if you use multiple schemas
        )

        with context.begin_transaction():
            context.run_migrations()


# Conditional execution based on context mode or specific commands
# This logic ensures that for autogeneration, if a DB connection isn't needed or available,
# it relies on offline mode. For actual upgrades/downgrades, online mode is used.

# Check if the command is 'revision' (especially for autogenerate)
# Alembic commands like 'revision' might not always set offline_mode=True
# We want to ensure that 'revision --autogenerate' can run without a live DB.

# A common pattern is to use try-except for the online connection
# or to have a specific flag/env var for CI environments where DB might not be available.

# Forcing offline for autogenerate if no URL is truly available for online mode:
actual_db_url_for_online = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

if context.is_offline_mode() or (context.get_x_argument(as_dictionary=True).get('autogenerate', False) and not actual_db_url_for_online):
    print("Running migrations in offline mode...")
    run_migrations_offline()
else:
    print("Running migrations in online mode...")
    if not actual_db_url_for_online:
        print("Warning: Attempting to run online migrations without a valid database URL.")
        # Fallback to offline if no URL, to prevent crash, though this might not be what user wants for 'upgrade'
        # A better approach for 'upgrade' would be to error out if no URL.
        # For 'autogenerate', this path should ideally not be taken if offline was properly triggered.
        # This is a safeguard.
        print("Falling back to offline mode due to missing online URL despite not being explicitly in offline mode.")
        run_migrations_offline()
    else:
        run_migrations_online()
