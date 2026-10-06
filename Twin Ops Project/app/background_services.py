import time
import threading
import streamlit as st

from app.database import init_db
from app.mqtt.publisher import run_publisher
from app.mqtt.subscriber import run_subscriber


@st.cache_resource
def start_background_services():
    """
    Start TwinOps MQTT subscriber and publisher once
    for the Streamlit application process.
    """

    # Make sure SQLite tables exist
    init_db()

    # Start subscriber first
    subscriber_thread = threading.Thread(
        target=run_subscriber,
        daemon=True,
        name="TwinOps-MQTT-Subscriber"
    )
    subscriber_thread.start()

    # Give subscriber a moment to connect to MQTT broker
    time.sleep(1)

    # Start telemetry publisher
    publisher_thread = threading.Thread(
        target=run_publisher,
        daemon=True,
        name="TwinOps-MQTT-Publisher"
    )
    publisher_thread.start()

    return {
        "subscriber": subscriber_thread,
        "publisher": publisher_thread
    }
