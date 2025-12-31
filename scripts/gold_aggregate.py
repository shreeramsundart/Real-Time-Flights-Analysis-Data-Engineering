import pandas as pd
from pathlib import Path

def run_gold_aggregate(**context):
    ti = context["ti"]
    silver_file = ti.xcom_pull(
        key="silver_file",
        task_ids="silver_transform"
    )

    if not silver_file:
        raise ValueError("silver_file not found in XCom")

    df = pd.read_csv(silver_file)

    # Safety cleaning (idempotent)
    df = df.dropna(subset=["origin_country"])
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce")
    df["on_ground"] = df["on_ground"].fillna(0).astype(int)

    agg = (
        df.groupby("origin_country")
        .agg(
            total_flights=("icao24", "count"),
            avg_velocity=("velocity", "mean"),
            on_ground=("on_ground", "sum")
        )
        .reset_index()
    )

    gold_dir = Path("/opt/airflow/data/gold")
    gold_dir.mkdir(parents=True, exist_ok=True)

    gold_path = gold_dir / Path(silver_file).name.replace("silver", "gold")
    agg.to_csv(gold_path, index=False)

    ti.xcom_push(
        key="gold_file",
        value=str(gold_path)
    )
