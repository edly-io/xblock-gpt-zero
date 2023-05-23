from voluptuous import Schema, Optional

CONFIG_SCHEMA = Schema({
    Optional('gptzero_display_name'): str,
})
