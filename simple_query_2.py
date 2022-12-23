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
As a viewer, I want to view my video history so I can re-watch the videos I watched before.

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
def view_history_menu():
    heading('As a viewer, I want to view my video history so I can re-watch the videos I watched before. \n Enter the viewer\'s name to view the names of video they have watched.')
    view_name = input('Viewer name: ')
    view_history(view_name)

def view_history(view_name):
    query = '''
        SELECT i.name
          FROM Viewer as e
          JOIN Viewing as v on e.user_id = v.user_id
          JOIN Video as i ON v.video_id = i.video_id
         WHERE e.name = %s
         ORDER BY i.name
    '''
    cmd = cur.mogrify(query, (view_name,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    # print_rows(rows)
    print()
    for row in rows:
        name = row
        print("%s" % (name))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1: view_history_menu}

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