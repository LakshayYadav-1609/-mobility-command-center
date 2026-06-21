import sqlite3
import random
from datetime import datetime, timedelta
from config import DB_PATH

FULL_NAMES = [
    "Rahul Sharma", "Priya Patel", "Amit Verma", "Sneha Gupta",
    "Vikram Mehta", "Ananya Singh", "Rohan Kumar", "Neha Joshi",
    "Arjun Nair", "Pooja Agarwal", "Karan Malhotra", "Divya Reddy",
    "Siddharth Bose", "Meera Iyer", "Varun Chopra", "Ishaan Kapoor",
    "James Smith", "Sarah Johnson", "Michael Brown", "Emma Wilson",
    "David Taylor", "Lisa Anderson", "John Davis", "Anna Thomas",
    "Robert Martinez", "Jennifer White", "William Harris", "Emily Clark",
    "Liu Yang", "Wei Chen", "Yuki Tanaka", "Kenji Sato",
    "Min-Jun Kim", "Ji-Young Park", "Hiroshi Yamamoto", "Sakura Ito",
    "Aisha Khan", "Omar Hassan", "Fatima Ali", "Ahmed Malik",
    "Elena Petrov", "Ivan Sokolov", "Sophie Martin", "Pierre Dubois",
    "Carlos Garcia", "Ana Lopez", "Maria Santos", "Roberto Silva",
    "Liam O Brien", "Aoife Murphy", "Sean Gallagher", "Niamh Ryan",
    "Mohammed Al Rashid", "Layla Al Farsi", "Tariq Hussain", "Nadia Abbas"
]

COMPANIES = [
    "TechGlobal Inc", "MegaCorp Ltd", "InnovateCo",
    "FutureTech", "GlobalServ Ltd", "SmartBiz Inc",
    "ProCorp", "NextGen Solutions", "AlphaGroup",
    "BetaIndustries", "GammaTech", "DeltaCorp",
    "OmegaServices", "ZenithGroup", "ApexSolutions"
]

ROUTES = [
    ("Delhi",     "London",        "UK"),
    ("Mumbai",    "Singapore",     "Singapore"),
    ("Bangalore", "Dubai",         "UAE"),
    ("Chennai",   "New York",      "USA"),
    ("Pune",      "Toronto",       "Canada"),
    ("Hyderabad", "Sydney",        "Australia"),
    ("Kolkata",   "Berlin",        "Germany"),
    ("Delhi",     "San Francisco", "USA"),
    ("Mumbai",    "Amsterdam",     "Netherlands"),
    ("Bangalore", "Tokyo",         "Japan"),
    ("Chennai",   "Dublin",        "Ireland"),
    ("Hyderabad", "Paris",         "France"),
    ("Pune",      "Melbourne",     "Australia"),
    ("Delhi",     "Frankfurt",     "Germany"),
    ("Mumbai",    "Toronto",       "Canada"),
]

SERVICE_TYPES = [
    "Moving/HHG",
    "Temporary Housing",
    "Immigration/Visa",
    "Destination Services",
    "Tax Assistance",
    "School Search"
]

SERVICE_SLA = {
    "Moving/HHG":           45,
    "Temporary Housing":    7,
    "Immigration/Visa":     60,
    "Destination Services": 30,
    "Tax Assistance":       90,
    "School Search":        21
}

POLICY_TIERS = ["Basic", "Standard", "Premium", "Executive"]

COMPLIANCE_TYPES = [
    "Work Permit",
    "Business Visa",
    "Dependent Visa",
    "Tax Filing Deadline",
    "Work Authorization",
    "Social Security Registration"
]

DELAY_REASONS = [
    "Documentation incomplete",
    "Vendor capacity issue",
    "Customs delay",
    "Assignee unavailable",
    "Housing market shortage",
    "Immigration backlog",
    "Budget approval pending",
    "Public holiday delay"
]

VENDOR_NAMES = {
    "Moving/HHG": [
        "SwiftMove Global", "SafeShip Co",
        "QuickRelo Agents", "GlobalMove Ltd"
    ],
    "Temporary Housing": [
        "HomeFirst Hotels", "StayEasy Corp",
        "ComfortStay Ltd", "TempHome Inc"
    ],
    "Immigration/Visa": [
        "VisaFast Partners", "ImmigrationPro",
        "GlobalVisa Ltd", "QuickPermit Co"
    ],
    "Destination Services": [
        "DestServ Pro", "ArrivalAssist Co",
        "SettleIn Ltd", "LocalGuide Inc"
    ],
    "Tax Assistance": [
        "TaxGlobal Inc", "FiscalPro Ltd",
        "TaxEase Corp", "GlobalFiscal Co"
    ],
    "School Search": [
        "EduFind Co", "SchoolMatch Ltd",
        "AcademyLink Inc", "StudyAssist Corp"
    ]
}

BASE_COSTS = {
    "Moving/HHG": {
        "Basic": 8000, "Standard": 15000,
        "Premium": 25000, "Executive": 50000
    },
    "Temporary Housing": {
        "Basic": 3000, "Standard": 6000,
        "Premium": 10000, "Executive": 20000
    },
    "Immigration/Visa": {
        "Basic": 2000, "Standard": 3500,
        "Premium": 5000, "Executive": 8000
    },
    "Destination Services": {
        "Basic": 1500, "Standard": 2500,
        "Premium": 4000, "Executive": 8000
    },
    "Tax Assistance": {
        "Basic": 1500, "Standard": 3000,
        "Premium": 5000, "Executive": 10000
    },
    "School Search": {
        "Basic": 1000, "Standard": 2000,
        "Premium": 3000, "Executive": 6000
    },
}


def create_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT,
            service_type      TEXT,
            country           TEXT,
            performance_score REAL,
            on_time_rate      REAL,
            risk_level        TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assignees (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT,
            company       TEXT,
            origin_city   TEXT,
            dest_city     TEXT,
            dest_country  TEXT,
            policy_tier   TEXT,
            start_date    TEXT,
            target_date   TEXT,
            status        TEXT,
            risk_score    REAL,
            family_size   INTEGER,
            dual_career   INTEGER,
            has_children  INTEGER,
            coordinator   TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            assignee_id    INTEGER,
            service_type   TEXT,
            vendor_id      INTEGER,
            status         TEXT,
            sla_days       INTEGER,
            start_date     TEXT,
            target_date    TEXT,
            delay_days     INTEGER,
            delay_reason   TEXT,
            cost_budgeted  REAL,
            cost_actual    REAL,
            FOREIGN KEY (assignee_id) REFERENCES assignees(id),
            FOREIGN KEY (vendor_id)   REFERENCES vendors(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS compliance (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            assignee_id      INTEGER,
            compliance_type  TEXT,
            expiry_date      TEXT,
            days_remaining   INTEGER,
            status           TEXT,
            FOREIGN KEY (assignee_id) REFERENCES assignees(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS costs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            assignee_id  INTEGER,
            service_type TEXT,
            budgeted     REAL,
            actual       REAL,
            variance     REAL,
            exception    INTEGER DEFAULT 0,
            FOREIGN KEY (assignee_id) REFERENCES assignees(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id   INTEGER,
            name         TEXT,
            planned_date TEXT,
            actual_date  TEXT,
            status       TEXT,
            FOREIGN KEY (service_id) REFERENCES services(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            assignee_id  INTEGER,
            alert_type   TEXT,
            message      TEXT,
            severity     TEXT,
            created_at   TEXT,
            acknowledged INTEGER DEFAULT 0,
            FOREIGN KEY (assignee_id) REFERENCES assignees(id)
        )
    """)
    print("✅ 7 tables created!")


def generate_vendors(cur):
    vendor_ids = {}
    for service_type, names in VENDOR_NAMES.items():
        vendor_ids[service_type] = []
        for name in names:
            score_type = random.choices(
                ["high", "avg", "poor"], weights=[30, 50, 20]
            )[0]
            if score_type == "high":
                score  = round(random.uniform(85, 98), 1)
                ontime = round(random.uniform(90, 98), 1)
                risk   = "LOW"
            elif score_type == "avg":
                score  = round(random.uniform(70, 84), 1)
                ontime = round(random.uniform(75, 89), 1)
                risk   = "MEDIUM"
            else:
                score  = round(random.uniform(45, 69), 1)
                ontime = round(random.uniform(60, 74), 1)
                risk   = "HIGH"
            cur.execute("""
                INSERT INTO vendors
                (name, service_type, country,
                 performance_score, on_time_rate, risk_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, service_type,
                random.choice(["India", "UK", "USA", "Singapore", "UAE"]),
                score, ontime, risk
            ))
            vendor_ids[service_type].append(cur.lastrowid)
    total = sum(len(v) for v in vendor_ids.values())
    print(f"✅ {total} vendors created!")
    return vendor_ids


def generate_services(cur, assignee_id, vendor_ids,
                      start_date, has_children, policy_tier):
    service_list = list(SERVICE_TYPES)
    if not has_children:
        service_list.remove("School Search")
    for stype in service_list:
        sla        = SERVICE_SLA[stype]
        vendor_id  = random.choice(vendor_ids[stype])
        svc_start  = start_date + timedelta(days=random.randint(0, 10))
        svc_target = svc_start + timedelta(days=sla)
        delay = random.choices(
            [0, random.randint(1, 5), random.randint(6, 15)],
            weights=[60, 25, 15]
        )[0]
        status = random.choices(
            ["Not Started", "In Progress", "Completed", "Delayed", "At Risk"],
            weights=[10, 35, 35, 12, 8]
        )[0]
        budgeted = BASE_COSTS[stype][policy_tier]
        budgeted = round(budgeted * random.uniform(0.9, 1.1), 2)
        actual   = round(budgeted * random.uniform(0.85, 1.25), 2)
        cur.execute("""
            INSERT INTO services
            (assignee_id, service_type, vendor_id, status,
             sla_days, start_date, target_date, delay_days,
             delay_reason, cost_budgeted, cost_actual)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assignee_id, stype, vendor_id, status, sla,
            svc_start.strftime("%Y-%m-%d"),
            svc_target.strftime("%Y-%m-%d"),
            delay,
            random.choice(DELAY_REASONS) if delay > 0 else None,
            budgeted, actual
        ))


def generate_compliance(cur, assignee_id, today):
    for _ in range(random.randint(1, 3)):
        days_ahead  = random.randint(-10, 365)
        expiry_date = today + timedelta(days=days_ahead)
        if days_ahead < 0:
            status = "EXPIRED"
        elif days_ahead <= 30:
            status = "CRITICAL"
        elif days_ahead <= 90:
            status = "WARNING"
        else:
            status = "SAFE"
        cur.execute("""
            INSERT INTO compliance
            (assignee_id, compliance_type,
             expiry_date, days_remaining, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            assignee_id,
            random.choice(COMPLIANCE_TYPES),
            expiry_date.strftime("%Y-%m-%d"),
            days_ahead, status
        ))


def generate_costs(cur, assignee_id, policy_tier):
    for stype in SERVICE_TYPES:
        budgeted  = BASE_COSTS[stype][policy_tier]
        budgeted  = round(budgeted * random.uniform(0.9, 1.1), 2)
        actual    = round(budgeted * random.uniform(0.85, 1.25), 2)
        variance  = round(actual - budgeted, 2)
        exception = 1 if variance > budgeted * 0.15 else 0
        cur.execute("""
            INSERT INTO costs
            (assignee_id, service_type, budgeted,
             actual, variance, exception)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (assignee_id, stype, budgeted, actual, variance, exception))


def generate_assignees(cur, vendor_ids, n=300):
    today = datetime.now()
    coordinators = [
        "Priya Sharma", "Raj Kumar",
        "Sneha Patel", "Amit Singh", "Neha Verma"
    ]
    names_pool = FULL_NAMES.copy()
    for i in range(n):
        if len(names_pool) == 0:
            names_pool = FULL_NAMES.copy()
        name = names_pool.pop(random.randint(0, len(names_pool) - 1))

        route        = random.choice(ROUTES)
        origin_city  = route[0]
        dest_city    = route[1]
        dest_country = route[2]

        family_size  = random.choices([1,2,3,4,5], weights=[20,30,25,15,10])[0]
        dual_career  = 1 if family_size > 1 and random.random() < 0.4 else 0
        has_children = 1 if family_size > 2 and random.random() < 0.6 else 0
        policy_tier  = random.choices(POLICY_TIERS, weights=[20,40,30,10])[0]

        start_date   = today - timedelta(days=random.randint(0, 90))
        target_date  = start_date + timedelta(days=random.randint(45, 120))

        risk = 20
        if dual_career:                                  risk += 20
        if has_children:                                 risk += 10
        if dest_country in ["Japan", "Germany", "France"]: risk += 15
        if policy_tier == "Basic":                       risk += 10
        risk = min(95, risk + random.randint(0, 25))

        if risk > 75:
            status = random.choices(
                ["At Risk", "Delayed", "In Progress"], weights=[40, 30, 30]
            )[0]
        elif risk > 50:
            status = random.choices(
                ["In Progress", "At Risk", "On Track"], weights=[50, 30, 20]
            )[0]
        else:
            status = random.choices(
                ["On Track", "In Progress", "Completed"], weights=[50, 35, 15]
            )[0]

        cur.execute("""
            INSERT INTO assignees
            (name, company, origin_city, dest_city,
             dest_country, policy_tier, start_date,
             target_date, status, risk_score,
             family_size, dual_career, has_children, coordinator)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, random.choice(COMPANIES),
            origin_city, dest_city, dest_country,
            policy_tier,
            start_date.strftime("%Y-%m-%d"),
            target_date.strftime("%Y-%m-%d"),
            status, round(risk, 1),
            family_size, dual_career, has_children,
            random.choice(coordinators)
        ))
        assignee_id = cur.lastrowid
        generate_services(cur, assignee_id, vendor_ids, start_date, has_children, policy_tier)
        generate_compliance(cur, assignee_id, today)
        generate_costs(cur, assignee_id, policy_tier)
    print(f"✅ {n} fictional assignees created!")


def generate_alerts(cur):
    alert_types = [
        "Compliance Due", "SLA Breach",
        "Cost Overrun", "Vendor Risk", "Assignment At Risk"
    ]
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    today = datetime.now()
    for _ in range(50):
        cur.execute("""
            INSERT INTO alerts
            (assignee_id, alert_type, message, severity, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 100),
            random.choice(alert_types),
            "This assignment requires immediate attention",
            random.choices(severities, weights=[20, 30, 35, 15])[0],
            (today - timedelta(hours=random.randint(0, 72))).strftime("%Y-%m-%d %H:%M:%S")
        ))
    print("✅ 50 alerts created!")


if __name__ == "__main__":
    print("\n" + "=" * 45)
    print("  Mobility Command Center — DB Setup")
    print("=" * 45)
    print("  NOTE: All data is 100% fictional!")
    print("=" * 45 + "\n")

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    create_tables(cur)
    vendor_ids = generate_vendors(cur)
    generate_assignees(cur, vendor_ids, n=300)
    generate_alerts(cur)

    conn.commit()
    conn.close()

    print("\n" + "=" * 45)
    print("  Database ready!")
    print(f"  File     : {DB_PATH}")
    print("  Tables   : 7")
    print("  Assignees: 300")
    print("  Next     : streamlit run app.py")
    print("=" * 45)
