
from pathlib import Path
from datetime import datetime
import uuid

import pandas as pd
from pandas.errors import EmptyDataError


ROOT = Path(
    r"C:\Users\LENOVO\Desktop\test1"
)


PROTOTYPE_DIR = (
    ROOT
    / "prototype"
)


DEMO_PATH = (
    PROTOTYPE_DIR
    / "manager_10_camera_demo.csv"
)


DECISIONS_PATH = (
    PROTOTYPE_DIR
    / "admin_alert_decisions.csv"
)


TICKETS_PATH = (
    PROTOTYPE_DIR
    / "incident_tickets.csv"
)


ACTION_LOG_PATH = (
    PROTOTYPE_DIR
    / "admin_action_log.csv"
)


DECISION_COLUMNS = [
    "neutral_uid",
    "camera_number",
    "camera_name",
    "location_name",
    "decision",
    "ticket_id",
    "reviewer",
    "admin_notes",
    "updated_at",
]


TICKET_COLUMNS = [
    "ticket_id",
    "created_at",
    "updated_at",
    "status",
    "priority",
    "camera_number",
    "camera_name",
    "location_name",
    "neutral_uid",
    "alert_type",
    "motion_gate_score",
    "v3a_probability",
    "trigger_frame",
    "reviewer",
    "admin_notes",
    "assigned_team",
    "assigned_to",
    "response_notes",
    "resolution_notes",
    "resolved_at",
]


ACTION_LOG_COLUMNS = [
    "action_id",
    "action_at",
    "neutral_uid",
    "camera_number",
    "camera_name",
    "location_name",
    "action",
    "ticket_id",
    "reviewer",
    "admin_notes",
    "old_status",
    "new_status",
]


def timestamp_now():

    return (
        datetime.now()
        .astimezone()
        .isoformat(
            timespec="seconds"
        )
    )


def load_table(
    path,
    columns,
):

    if not path.exists():

        return pd.DataFrame(
            columns=columns
        )


    try:

        df = pd.read_csv(
            path,
            dtype=str,
        )


    except EmptyDataError:

        return pd.DataFrame(
            columns=columns
        )


    for column in columns:

        if column not in df.columns:

            df[
                column
            ] = ""


    return (
        df[
            columns
        ]
        .fillna("")
        .copy()
    )


def save_table(
    df,
    path,
    columns,
):

    df = df.copy()


    for column in columns:

        if column not in df.columns:

            df[
                column
            ] = ""


    df[
        columns
    ].to_csv(
        path,
        index=False,
        lineterminator="\n",
    )


def to_bool(
    series,
):

    if pd.api.types.is_bool_dtype(
        series
    ):

        return series.astype(
            bool
        )


    return (
        series
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(
            [
                "true",
                "1",
                "yes",
            ]
        )
    )


def safe_float(
    value,
    digits=3,
):

    try:

        if pd.isna(
            value
        ):

            return "—"


        return (
            f"{float(value):.{digits}f}"
        )


    except Exception:

        return "—"


def safe_int(
    value,
):

    try:

        if pd.isna(
            value
        ):

            return "—"


        return str(
            int(
                float(
                    value
                )
            )
        )


    except Exception:

        return "—"


def load_demo():

    df = pd.read_csv(
        DEMO_PATH
    )


    for column in [
        "motion_gate_triggered",
        "spatial_positive",
        "final_alert",
    ]:

        df[
            column
        ] = to_bool(
            df[
                column
            ]
        )


    return df


def get_decisions():

    return load_table(
        DECISIONS_PATH,
        DECISION_COLUMNS,
    )


def get_tickets():

    return load_table(
        TICKETS_PATH,
        TICKET_COLUMNS,
    )


def get_action_log():

    return load_table(
        ACTION_LOG_PATH,
        ACTION_LOG_COLUMNS,
    )


def get_current_decision(
    neutral_uid,
):

    decisions = get_decisions()


    matches = decisions[
        decisions[
            "neutral_uid"
        ]
        ==
        str(
            neutral_uid
        )
    ]


    if len(
        matches
    ) == 0:

        return None


    return (
        matches.iloc[
            -1
        ]
        .to_dict()
    )


def save_decision(
    camera,
    decision,
    reviewer,
    notes,
    ticket_id="",
):

    decisions = get_decisions()


    neutral_uid = str(
        camera[
            "neutral_uid"
        ]
    )


    decisions = decisions[
        decisions[
            "neutral_uid"
        ]
        !=
        neutral_uid
    ].copy()


    new_row = {

        "neutral_uid":
            neutral_uid,

        "camera_number":
            str(
                int(
                    camera[
                        "camera_number"
                    ]
                )
            ),

        "camera_name":
            str(
                camera[
                    "camera_name"
                ]
            ),

        "location_name":
            str(
                camera[
                    "location_name"
                ]
            ),

        "decision":
            decision,

        "ticket_id":
            str(
                ticket_id
            ),

        "reviewer":
            str(
                reviewer
            ),

        "admin_notes":
            str(
                notes
            ),

        "updated_at":
            timestamp_now(),
    }


    decisions = pd.concat(
        [
            decisions,
            pd.DataFrame(
                [
                    new_row
                ]
            ),
        ],
        ignore_index=True,
    )


    save_table(
        decisions,
        DECISIONS_PATH,
        DECISION_COLUMNS,
    )


def log_action(
    camera,
    action,
    reviewer,
    notes="",
    ticket_id="",
    old_status="",
    new_status="",
):

    log_df = get_action_log()


    new_row = {

        "action_id":
            (
                "ACT-"
                +
                uuid.uuid4()
                .hex[
                    :10
                ]
                .upper()
            ),

        "action_at":
            timestamp_now(),

        "neutral_uid":
            str(
                camera[
                    "neutral_uid"
                ]
            ),

        "camera_number":
            str(
                int(
                    camera[
                        "camera_number"
                    ]
                )
            ),

        "camera_name":
            str(
                camera[
                    "camera_name"
                ]
            ),

        "location_name":
            str(
                camera[
                    "location_name"
                ]
            ),

        "action":
            str(
                action
            ),

        "ticket_id":
            str(
                ticket_id
            ),

        "reviewer":
            str(
                reviewer
            ),

        "admin_notes":
            str(
                notes
            ),

        "old_status":
            str(
                old_status
            ),

        "new_status":
            str(
                new_status
            ),
    }


    log_df = pd.concat(
        [
            log_df,
            pd.DataFrame(
                [
                    new_row
                ]
            ),
        ],
        ignore_index=True,
    )


    save_table(
        log_df,
        ACTION_LOG_PATH,
        ACTION_LOG_COLUMNS,
    )


def create_ticket(
    camera,
    reviewer,
    notes,
    alert_type="AI Accident Alert",
):

    tickets = get_tickets()


    neutral_uid = str(
        camera[
            "neutral_uid"
        ]
    )


    active = tickets[
        (
            tickets[
                "neutral_uid"
            ]
            ==
            neutral_uid
        )
        &
        (
            tickets[
                "status"
            ]
            .isin(
                [
                    "Open",
                    "In Progress",
                ]
            )
        )
    ]


    if len(
        active
    ) > 0:

        return str(
            active.iloc[
                0
            ][
                "ticket_id"
            ]
        )


    now = timestamp_now()


    camera_number = int(
        camera[
            "camera_number"
        ]
    )


    ticket_id = (
        "TKT-"
        +
        datetime.now()
        .strftime(
            "%Y%m%d-%H%M%S"
        )
        +
        f"-C{camera_number:02d}-"
        +
        uuid.uuid4()
        .hex[
            :4
        ]
        .upper()
    )


    ticket = {

        "ticket_id":
            ticket_id,

        "created_at":
            now,

        "updated_at":
            now,

        "status":
            "Open",

        "priority":
            "High",

        "camera_number":
            str(
                camera_number
            ),

        "camera_name":
            str(
                camera[
                    "camera_name"
                ]
            ),

        "location_name":
            str(
                camera[
                    "location_name"
                ]
            ),

        "neutral_uid":
            neutral_uid,

        "alert_type":
            str(
                alert_type
            ),

        "motion_gate_score":
            safe_float(
                camera[
                    "motion_gate_sequence_score"
                ],
                6,
            ),

        "v3a_probability":
            safe_float(
                camera[
                    "spatial_probability"
                ],
                6,
            ),

        "trigger_frame":
            safe_int(
                camera[
                    "first_trigger_actual_frame"
                ]
            ),

        "reviewer":
            reviewer,

        "admin_notes":
            notes,

        "assigned_team":
            "",

        "assigned_to":
            "",

        "response_notes":
            "",

        "resolution_notes":
            "",

        "resolved_at":
            "",
    }


    tickets = pd.concat(
        [
            tickets,
            pd.DataFrame(
                [
                    ticket
                ]
            ),
        ],
        ignore_index=True,
    )


    save_table(
        tickets,
        TICKETS_PATH,
        TICKET_COLUMNS,
    )


    return ticket_id


def cancel_active_ticket(
    neutral_uid,
):

    tickets = get_tickets()


    mask = (
        (
            tickets[
                "neutral_uid"
            ]
            ==
            str(
                neutral_uid
            )
        )
        &
        (
            tickets[
                "status"
            ]
            .isin(
                [
                    "Open",
                    "In Progress",
                ]
            )
        )
    )


    if mask.any():

        tickets.loc[
            mask,
            "status"
        ] = (
            "Cancelled - False Alert"
        )


        tickets.loc[
            mask,
            "updated_at"
        ] = timestamp_now()


        save_table(
            tickets,
            TICKETS_PATH,
            TICKET_COLUMNS,
        )


def update_ticket(
    ticket_id,
    status,
    priority,
    assigned_team,
    assigned_to,
    response_notes,
    resolution_notes,
    reviewer,
    demo_df,
):

    tickets = get_tickets()


    mask = (
        tickets[
            "ticket_id"
        ]
        ==
        str(
            ticket_id
        )
    )


    if mask.sum() != 1:

        raise RuntimeError(
            "Ticket could not be uniquely resolved."
        )


    old_status = str(
        tickets.loc[
            mask,
            "status"
        ].iloc[
            0
        ]
    )


    tickets.loc[
        mask,
        "status"
    ] = status


    tickets.loc[
        mask,
        "priority"
    ] = priority


    tickets.loc[
        mask,
        "assigned_team"
    ] = assigned_team


    tickets.loc[
        mask,
        "assigned_to"
    ] = assigned_to


    tickets.loc[
        mask,
        "response_notes"
    ] = response_notes


    tickets.loc[
        mask,
        "resolution_notes"
    ] = resolution_notes


    tickets.loc[
        mask,
        "updated_at"
    ] = timestamp_now()


    if status in [
        "Resolved",
        "Closed",
    ]:

        current = str(
            tickets.loc[
                mask,
                "resolved_at"
            ].iloc[
                0
            ]
        )


        if current.strip() == "":

            tickets.loc[
                mask,
                "resolved_at"
            ] = timestamp_now()


    save_table(
        tickets,
        TICKETS_PATH,
        TICKET_COLUMNS,
    )


    ticket_row = tickets[
        mask
    ].iloc[
        0
    ]


    matches = demo_df[
        demo_df[
            "neutral_uid"
        ]
        ==
        str(
            ticket_row[
                "neutral_uid"
            ]
        )
    ]


    if len(
        matches
    ) == 1:

        camera = matches.iloc[
            0
        ]


        log_action(
            camera=camera,
            action="UPDATE_TICKET",
            reviewer=reviewer,
            notes=(
                f"Priority={priority}; "
                f"Team={assigned_team}; "
                f"AssignedTo={assigned_to}; "
                f"ResponseNotes={response_notes}; "
                f"ResolutionNotes={resolution_notes}"
            ),
            ticket_id=ticket_id,
            old_status=old_status,
            new_status=status,
        )
