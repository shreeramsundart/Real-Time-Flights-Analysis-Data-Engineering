import pandas as pd
import snowflake.connector
from airflow.hooks.base import BaseHook
from pathlib import Path

def load_gold_to_snowflake(**context):
    ti = context["ti"]

    gold_file = ti.xcom_pull(
        key="gold_file",
        task_ids="gold_aggregate"
    )

    if not gold_file or not Path(gold_file).exists():
        raise ValueError("Gold file not found in XCom or does not exist")

    execution_date = context["data_interval_start"].strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(gold_file)

    # Fix NaNs and types
    df = df.fillna(0)
    df["on_ground"] = df["on_ground"].astype(int)
    df["total_flights"] = df["total_flights"].astype(int)
    df["avg_velocity"] = df["avg_velocity"].astype(float)

    # Connect to Snowflake
    conn = BaseHook.get_connection("flight_snowflake")
    sf_conn = snowflake.connector.connect(
        user=conn.login,
        password=conn.password,
        account=conn.extra_dejson["account"],
        warehouse=conn.extra_dejson["warehouse"],
        database=conn.extra_dejson["database"],
        schema=conn.schema,
        role=conn.extra_dejson["role"],
        autocommit=False   # important
    )

    merge_sql = """
        MERGE INTO FLIGHT_KPIS tgt
        USING (
            SELECT
                TO_TIMESTAMP(%s) AS WINDOW_START,
                %s AS ORIGIN_COUNTRY,
                %s AS TOTAL_FLIGHTS,
                %s AS AVG_VELOCITY,
                %s AS ON_GROUND
        ) src
        ON tgt.WINDOW_START = src.WINDOW_START
           AND tgt.ORIGIN_COUNTRY = src.ORIGIN_COUNTRY
        WHEN MATCHED THEN UPDATE SET
            TOTAL_FLIGHTS = src.TOTAL_FLIGHTS,
            AVG_VELOCITY = src.AVG_VELOCITY,
            ON_GROUND = src.ON_GROUND,
            LOAD_TIME = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN INSERT
        (WINDOW_START, ORIGIN_COUNTRY, TOTAL_FLIGHTS, AVG_VELOCITY, ON_GROUND)
        VALUES
        (src.WINDOW_START, src.ORIGIN_COUNTRY, src.TOTAL_FLIGHTS, src.AVG_VELOCITY, src.ON_GROUND);
    """

    cursor = sf_conn.cursor()
    try:
        for _, row in df.iterrows():
            cursor.execute(
                merge_sql,
                (
                    execution_date,
                    row["origin_country"],
                    row["total_flights"],
                    row["avg_velocity"],
                    row["on_ground"],
                )
            )
        sf_conn.commit()   # 🔥 Critical fix
    finally:
        cursor.close()
        sf_conn.close()
