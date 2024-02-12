import pandas as pd

def extract_columns(file):
    """
    Reads the CSV File and extracts the specific columns:  username, content, and timestamp. 
    Turns the extracted data to a dataframe.
    """
    df = pd.read_csv(file)
    
    cols = ['author.username','content','timestamp']

    extracted_df = df[cols]

    return extracted_df

def extract_content(file):
    """
    Reads the CSV file and extracts the messages starting with "Day".
    Extracts the relevant information into a nice table format.
    """
    extracted_df = extract_columns(file)
      
    days = []
    repo_urls = []
    lang_techs = []

    for message in extracted_df['content']:
        if message.startswith('Day'):
            day = int(message.split(':')[0].split()[-1])
            days.append(day)

            repo_url = None
            if 'GitHub Repository Link' in message:
                link_index = message.find('GitHub Repository Link: ')
                if link_index != -1:
                    link_start = link_index + len('GitHub Repository Link: ')
                    link_end = message.find('\n', link_start)
                    repo_url = message[link_start:link_end].strip()
                else:
                    repo_url = 'N/A'
            else:
                repo_url = 'N/A'
            repo_urls.append(repo_url)

            lang_tech = None
            if 'Languages/Technologies Used' in message:
                lang_tech_start_index = message.find('Languages/Technologies Used')
                lang_tech_end_index = message.find('Blockers:')
                if lang_tech_start_index != -1 and lang_tech_end_index != -1:
                    lang_tech_part = message[lang_tech_start_index:lang_tech_end_index]
                    lang_tech = lang_tech_part.split(': ')[1].strip().split(', ')
            lang_techs.append(lang_tech)

        else:
            days.append('N/A')
            repo_urls.append('N/A')
            lang_techs.append('N/A')

    extracted_df['Day'] = days
    extracted_df['Repo_URL'] = repo_urls
    extracted_df['Lang_Tech'] = lang_techs
    extracted_df['timestamp'] = pd.to_datetime(extracted_df['timestamp']).dt.strftime('%m-%d-%Y')

    return extracted_df

def to_csv(file, output_file):
    extracted_data = extract_content(file)
    extracted_data.to_csv(output_file, index=False)
    print(f"Data printed to {output_file} successfully.")


file = 'February-12.csv' #Replace with File Path
output_file = 'February-12-V1.csv' #Replace with File Name
to_csv(file, output_file)