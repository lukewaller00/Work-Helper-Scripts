import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta

# Helper function to split marks into weekly chunks
def split_marks_into_weeks(marks, start_date, end_date):
    weeks = []
    current_date = start_date
    days_per_week = 5
    sessions_per_day = 2
    marks_per_week = days_per_week * sessions_per_day

    for i in range(0, len(marks), marks_per_week):
        week_marks = marks[i:i + marks_per_week]
        week_dates = [(current_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, days_per_week)]
        weeks.append((week_dates, week_marks))
        current_date += timedelta(days=7)  # Move to the next week

    return weeks

# Main function to process the XML and generate the CSV
def process_attendance_summary(xml_path, csv_output_path):
    # Parse XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract necessary data
    start_date = datetime.strptime(root.find('StartDate').text, '%Y-%m-%d')
    end_date = datetime.strptime(root.find('EndDate').text, '%Y-%m-%d')
    mark_string = root.find(".//SIF_ExtendedElement[@Name='Marks']").text
    marks = mark_string.split(',')

    # Split marks into weekly chunks
    weeks = split_marks_into_weeks(marks, start_date, end_date)

    # Write weekly attendance data to CSV
    with open(csv_output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Week Start Date', 'Mon AM', 'Mon PM', 'Tue AM', 'Tue PM', 
                  'Wed AM', 'Wed PM', 'Thu AM', 'Thu PM', 'Fri AM', 'Fri PM']
        writer.writerow(header)

        for week_dates, week_marks in weeks:
            week_start_date = week_dates[0]
            row = [week_start_date] + week_marks
            writer.writerow(row)

# File paths
xml_path = 'AttendanceSummaryBreakdown\\LearnerAttendanceSummary.xml'
csv_output_path = 'AttendanceSummaryBreakdown\\SIFWeeklyAttendanceBreakdown.csv'

# Run the script
process_attendance_summary(xml_path, csv_output_path)
