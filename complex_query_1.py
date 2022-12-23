#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

#------------------------------------------------------------
# show_menu
#------------------------------------------------------------

def show_menu():
    menu = '''

--------------------------------------------------
As a creator, I want to list demography of who viewed my videos so that I can determine my target audience. 

Choose (1, 0 to quit): '''

    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice in range(1,1+1):
            print()
            actions[choice]()
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close() 

#------------------------------------------------------------
# List demography of who viewed my videos
#------------------------------------------------------------
def list_demo_viewed_my_videos_menu():
    heading('\nAs a creator, I want to list demography of who viewed my videos so that I can determine my target audience. \n Enter your creator username to view the age and gender of your subscribers.')
    creator_name = input('Creator name: ')
    list_demo_viewed_my_videos(creator_name)

def list_demo_viewed_my_videos(creator_name):
    query = '''
    SELECT v.gender, v.age
      FROM Creator as c
      JOIN Video as i ON c.user_id = i.user_id
      JOIN Viewing as t ON i.video_id = t.video_id
      JOIN Viewer as v ON t.user_id = v.user_id 
     WHERE c.name = %s
     ORDER BY v.gender, v.age
    '''
    cmd = cur.mogrify(query, (creator_name,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    # print_rows(rows)
    print()
    for row in rows:
        gender, age = row
        print("%s, %s" % (gender, age))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_demo_viewed_my_videos_menu}

if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'youtube', 'isdb'
        # you may have to adjust the user 
        # python a4-socnet-sraja.py a4_socnet postgres
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))