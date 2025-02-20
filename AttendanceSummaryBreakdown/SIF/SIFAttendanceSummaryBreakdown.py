import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta

# Helper function to split marks into calendar weeks based on actual days
def split_marks_into_calendar_weeks(marks, start_date, end_date):
    weeks = []
    days_per_week = 7
    sessions_per_day = 2

    # Calculate the start of the week for the provided start_date (does not alter input data)
    days_to_monday = start_date.weekday()  # Days since last Monday
    week_start_date = start_date - timedelta(days=days_to_monday)

    current_date = week_start_date
    current_mark_index = 0

    while current_date <= end_date or current_mark_index < len(marks):
        week_marks = []
        week_dates = [(current_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_per_week)]

        for i in range(days_per_week):
            for session in range(sessions_per_day):
                current_day = current_date + timedelta(days=i)
                if start_date <= current_day <= end_date and current_mark_index < len(marks):
                    # Use the mark if within the date range and marks available
                    week_marks.append(marks[current_mark_index])
                    current_mark_index += 1
                else:
                    # Empty mark for days outside the range or beyond available marks
                    week_marks.append("")

        weeks.append((week_dates, week_marks))
        current_date += timedelta(days=days_per_week)

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

    # Split marks into weekly chunks based on calendar weeks
    weeks = split_marks_into_calendar_weeks(marks, start_date, end_date)

    # Write weekly attendance data to CSV
    with open(csv_output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Week Start Date', 'Mon AM', 'Mon PM', 'Tue AM', 'Tue PM', 
                  'Wed AM', 'Wed PM', 'Thu AM', 'Thu PM', 'Fri AM', 'Fri PM', 
                  'Sat AM', 'Sat PM', 'Sun AM', 'Sun PM']
        writer.writerow(header)

        for week_dates, week_marks in weeks:
            week_start_date = week_dates[0]
            row = [week_start_date] + week_marks
            writer.writerow(row)

# File paths
xml_path = 'AttendanceSummaryBreakdown\\SIF\\LearnerAttendanceSummary.xml'
csv_output_path = 'AttendanceSummaryBreakdown\\SIF\\SIFWeeklyAttendanceBreakdown1.csv'

# Run the script
process_attendance_summary(xml_path, csv_output_path)
