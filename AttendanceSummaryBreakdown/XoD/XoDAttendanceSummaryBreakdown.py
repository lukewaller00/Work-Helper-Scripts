import csv
from datetime import datetime, timedelta

# Input JSON data
data = {
    "Id": "xI80KRDWZ",
    "XID": "xI80KRDWZ",
    "MIS_ID": "13718",
    "IdaasId": "PL-13718",
    "AttStatsStartDate": "2024-08-25",
    "AttStatsEndDate": "2024-11-29",
    "NumPossMarks": 0,
    "NumPresMarks": 0,
    "NumAEAMarks": 0,
    "NumAuthAbsMarks": 0,
    "NumUnauthAbsMarks": 0,
    "NumMissMarks": 0,
    "NumLateMarks": 0,
    "NumLateBeforeRegMarks": 0,
    "Marks": "##################################################################################################################################################################################################",
    "MarksCSV": "#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#,#"
}

# Parse dates and marks
start_date = datetime.strptime(data["AttStatsStartDate"], "%Y-%m-%d")
end_date = datetime.strptime(data["AttStatsEndDate"], "%Y-%m-%d")
marks = data["Marks"]

# Function to split marks into weekly structure
def split_marks_into_weekly_sessions(start_date, end_date, marks):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    sessions = ["AM", "PM"]
    weekly_data = []
    mark_index = 0

    # Start iterating from the first Monday in the range
    current_date = start_date - timedelta(days=start_date.weekday())
    
    while current_date <= end_date:
        week_start = current_date.strftime("%Y-%m-%d")
        week_row = {"Week Start Date": week_start}
        
        for day in days_of_week:
            for session in sessions:
                if start_date <= current_date <= end_date and mark_index < len(marks):
                    week_row[f"{day} {session}"] = marks[mark_index]
                    mark_index += 1
                else:
                    week_row[f"{day} {session}"] = ""
            current_date += timedelta(days=1)
        
        weekly_data.append(week_row)
        # Move to the next week
        current_date += timedelta(days=2)  # Skip the weekend
    
    return weekly_data

# Split marks into weekly sessions
weekly_sessions = split_marks_into_weekly_sessions(start_date, end_date, marks)

# Write the weekly data to a CSV file
output_file = "AttendanceSummaryBreakdown\\XODWeeklyAttendanceBreakdown.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Define the header row
    header = ["Week Start Date"] + [f"{day} {session}" for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for session in ["AM", "PM"]]
    writer.writerow(header)
    # Write the data rows
    for week in weekly_sessions:
        writer.writerow([week.get(column, "") for column in header])

print(f"Weekly attendance has been written to {output_file}")
