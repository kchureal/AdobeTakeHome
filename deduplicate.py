#!/usr/bin/env python3
import json
from datetime import datetime
import argparse


def parse_date(date_str):  # convert string timestamp into datetime object for easier sorting and comparision
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S+00:00")


def deduplicate_leads(leads):
    unique_by_id = {}  # Dict to store unique leads based on id
    unique_by_email = {}  # Dict to store unique leads based on email
    change_log = []  # log to track changes when a lead is replaced by a newer one.

    for lead in leads:  # process each lead in the json file
        lead_id = lead['_id']  # Extract id
        email = lead['email']  # Extract email
        entry_date = parse_date(lead['entryDate'])  # Convert the string timestamp into datetime

        if lead_id in unique_by_id:  # Check for duplicate ID in dict, if true
            existing_lead = unique_by_id[lead_id]  # retrieve existing lead under this id from the dict
            existing_date = parse_date(existing_lead['entryDate'])  # Extract the associated date
            if entry_date > existing_date or (entry_date == existing_date and leads.index(lead) > leads.index(existing_lead)):  # If entry_date is later, new lead replaces existing, if same the later entry is kept
                log_changes(change_log, existing_lead, lead)  # log change before replacing the exisitng lead
                unique_by_id[lead_id] = lead  # replace existing lead
                if existing_lead['email'] in unique_by_email:  # remove old lead from the dict if it exists
                    del unique_by_email[existing_lead['email']]
                unique_by_email[email] = lead  # update the dict with new preferred lead
        else:  # id doesn't exist in dict yet
            unique_by_id[lead_id] = lead  # add to dict

        if email in unique_by_email:  # Check for duplicate email in dict if true
            existing_lead = unique_by_email[email]  # retrieve existing lead under this email from the dict
            existing_date = parse_date(existing_lead['entryDate'])  # extract the associated date
            if entry_date > existing_date or (entry_date == existing_date and leads.index(lead) > leads.index(existing_lead)): #If entry date is later, new lead replaces existing, if same the later entry is kept
                log_changes(change_log, existing_lead, lead)  # log change before replacing the existing lead
                unique_by_email[email] = lead  # replace existing lead
                if existing_lead['_id'] in unique_by_id:  # remove old lead from the ID_dict if it exists (ID prio)
                    del unique_by_id[existing_lead['_id']]  # update the ID_dict with new preferred lead
                unique_by_id[lead_id] = lead  # update the ID_dict wit new preferred lead
        else:  # email doesn't exist in dict yet
            unique_by_email[email] = lead  # add to dict

    unique_leads = list(unique_by_id.values())  # converts unique id dict values into list anf combine the unique records
    return unique_leads, change_log  # return the unique leads and change_log


def log_changes(change_log, old_lead, new_lead):  # helper func for logging changes for old and new leads
    changes = {}   # keep track of changes in each record
    for key in old_lead:  # Loop through each key in old_lead compariing values, if value has changes, trakc in dict
        if old_lead[key] != new_lead[key]:
            changes[key] = {'from': old_lead[key], 'to': new_lead[key]}
    if changes:  # Append log entry with source, output, and the change
        change_log.append({
            'source_record': old_lead,
            'output_record': new_lead,
            'changes': changes
        })


def main():  # Handling CLI I/O
    parser = argparse.ArgumentParser(description="Deduplicate JSON leads based on ID and email.")
    parser.add_argument('input_file', type=str, help="Path to the input JSON file.")
    parser.add_argument('output_file', type=str, help="Path to save the deduplicated JSON file.")
    parser.add_argument('--log_file', type=str, default="change_log.json",
                        help="Path to save the change log JSON file.")
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:  # Load JSON data
        data = json.load(file)

    leads = data['leads']  # extract leads list
    unique_leads, change_log = deduplicate_leads(leads)  # Dedup json logic called

    output = {'leads': unique_leads}  # Output the deduplicated leads
    with open(args.output_file, 'w') as file:
        json.dump(output, file, indent=4)

    with open(args.log_file, 'w') as file:  # Output the change log
        json.dump(change_log, file, indent=4)


if __name__ == "__main__": #main func for execution
    main()
