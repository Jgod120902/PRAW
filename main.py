import creds
import praw
import re
from os.path import exists

submission_ids = ['pw8c2u', 'pbfkn1']
replace_more_limit = 10 # Set to None for max amount of trainer codes

reddit = praw.Reddit(
  client_id = creds.my_client_id, 
  client_secret = creds.my_client_secret, 
  user_agent = creds.my_user_agent,
  username = creds.my_username,
  password = creds.my_password)

reg = re.compile('(\d{4}\s\d{4}\s\d{4})') # Uses re for finding the pattern of '#### #### ####', aka the trainer codes

trainer_codes = []

def load_trainer_codes(): # Loads the trainer codes file if it exists
  if exists('trainer_codes.txt'):
    with open('trainer_codes.txt') as f:
      for trainer_code in f:
        trainer_codes.append(trainer_code.strip())
    print(f'Loaded {len(trainer_codes)} Trainer Code(s)')
  else:
    print('"trainer_codes.txt" Not Found')

def find_trainer_codes(submission_ids): # Scrapes the submission ids for comments that contain the re '#### #### ####'
  i = 0
  for submission_id in submission_ids:
    submission = reddit.submission(submission_id)
    submission.comment_sort = 'new'
    submission.comments.replace_more(limit=replace_more_limit)

    for comment in submission.comments:
      trainer_code_match = reg.search(comment.body)
      if trainer_code_match:
        trainer_code = trainer_code_match.group(1)
        if trainer_code not in trainer_codes: # If the trainer code is already logged it ignores it, otherwise it adds it to the list
          trainer_codes.append(trainer_code)
          i += 1
  print(f'Found {i} New Trainer Code(s)')

def export_trainer_codes(): # Exports all the trainer codes to the file 'trainer_codes.txt'
  with open('trainer_codes.txt', 'w') as f:
    for trainer_code in trainer_codes:
      f.write(f'{trainer_code}\n')
  print('Exported Trainer Code(s)')

load_trainer_codes()
find_trainer_codes(submission_ids)
export_trainer_codes()
