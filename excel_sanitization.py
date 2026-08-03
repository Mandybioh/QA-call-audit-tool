import re
import pandas as pd

_FORMULA_PREFIX_PATTERN = re.compile(r"^\s*[=+\-@]")


def sanitize_excel_cell(value):
    """Prevent Excel formula injection for string-like cell values."""
    if value is None:
        return value
    if isinstance(value, str) and _FORMULA_PREFIX_PATTERN.match(value):
        return value if value.startswith("'") else f"'{value}"
    return value


def sanitize_dataframe_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with string/object columns sanitized for safe Excel export."""
    if df is None or df.empty:
        return df

    sanitized = df.copy()
    object_columns = sanitized.select_dtypes(include=["object", "string"]).columns

    for column in object_columns:
        sanitized[column] = sanitized[column].map(sanitize_excel_cell)

    return sanitized
