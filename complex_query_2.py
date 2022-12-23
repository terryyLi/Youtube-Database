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
As a creator I want to see the number of videos that fall under each genre in my channel so I can analyze the focus and main themes of my content. 


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
def display_statistics_menu():
    heading('As a creator I want to see the number of videos that fall under each genre in my channel so I can analyze the focus and main themes of my content. \n Enter the creator name to view the number of videos per genre in their channel.')
    creator_name = input('Creator name: ')
    display_statistics(creator_name)

def display_statistics(creator_name):
    query = '''
    SELECT COUNT(v.video_id) as count, v.genre
      FROM Creator as r 
      JOIN Channel as c on r.user_id = c.user_id
      JOIN Video as v on c.channel_id = v.channel_id
     WHERE r.name = %s 
     GROUP BY v.genre
     ORDER BY count, v.genre
    '''
    cmd = cur.mogrify(query, (creator_name,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    # print_rows(rows)
    print()
    for row in rows:
        count, genre = row
        print("(%s), %s" % (count, genre))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1: display_statistics_menu}

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