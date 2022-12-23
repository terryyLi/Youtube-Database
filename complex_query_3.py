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
1. As an advertiser, I want to see how many people have viewed my advertisement so I can make better decisions about where to put advertisements next time.::

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
def view_advertisement_demographics_menu():
    heading('As an advertiser, I want to see how many people have viewed my advertisement so I can make better decisions about where to put advertisements next time. \n Enter the advertisement id to view the number of the views that advertisement recieved.')
    advertisements_id = input('Advertisement id (1~30): ')
    view_advertisement_demographics(advertisements_id)

def  view_advertisement_demographics(advertisements_id):
    query = '''
    SELECT sum(v.views) as sum
    FROM Video as v JOIN Advertisement as a on v.advertisement_id = a.advertisement_id
    WHERE a.advertisement_id = %s
    ORDER BY sum
    '''
    cmd = cur.mogrify(query, (advertisements_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    # print_rows(rows)
    print()
    for row in rows:
        sum = row
        print("%s" % (sum))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:  view_advertisement_demographics_menu}

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