from PyPDF2 import PdfFileMerger, PdfFileReader
import httplib2
import os
from pprint import pprint
from apiclient import discovery
from google.oauth2 import service_account
from search_results import googleSearch, search_queries, build_results_pdf, search_url
from PyPDF2 import PdfFileMerger, PdfFileReader


def parse_response(res):
    for i in list(res.values())[2]:
        queries.append(i[0])


def write_lines(results, query):
    with open("results.txt", "a") as openFile:
        openFile.write(f'<< {query} >>\n')
        openFile.write('\n'.join(results))
        openFile.write('\n\n')


queries = []

try:
    scopes = ["https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), 'client_secret.json')

    spreadsheet_id = '11PwH1-wAszNzwPYfRvxKvoOhOgyp2FD_eyUamsmZBls'
    range_name = 'Sheet1!A:A'

    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=scopes)
    service = discovery.build('sheets', 'v4', credentials=credentials)

    # values = [
    #     ['a1', 'b1', 'c1', 123],
    #     ['a2', 'b2', 'c2', 456],
    # ]

    # data = {
    #     'values': values
    # }

    # service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name)
    response = request.execute()
    parse_response(response)


except OSError as e:
    print(e)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


query_groups = chunker(sorted(queries), 20)
filepath_list = []

for index, group in enumerate(query_groups):
    try:
        build_results_pdf(group, index)
        filepath_list.append(f'out{index}.pdf')
    except:
        continue


pprint(filepath_list)

if filepath_list:
    merger = PdfFileMerger()
    for f in filepath_list:
        merger.append(PdfFileReader(f), 'rb', import_bookmarks=False)
    with open('merged_results.pdf', 'wb') as new_file:
        merger.write(new_file)
    os.remove(f)
